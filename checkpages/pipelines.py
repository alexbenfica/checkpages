from scrapy.exceptions import DropItem
from scrapy import signals

# https://code.google.com/p/pyh/
# install it using python setup.py install
from pyh import *







class FilterForbiddenWordsPipeline(object):
    """A pipeline for filtering out items which contain certain words in their description.
    These words are in a file sent via command line parameter and loaded in the spider __init__ """

    def process_item(self, item, spider):
        
        item['forbidden_words'] = []
        html_lower = item['html'].lower()
        for word in spider.forbiddenWords:            
            if word.lower() in html_lower:
                item['forbidden_words'].append(word)               
                
        print 'Filtering forbidden words : %s ' % ', '.join(item['forbidden_words'])                
        print
        return item







class HTMLWriterPipeline(object):
    """ Pipiline to write a HTML file report from the screpped links."""

    def __init__(self):
        self.html_file = None
        self.itens = []
        

    def initializeFile(self, spider):
        if spider.output_html_filename:
            if not self.html_file: 
                self.html_file = open(spider.output_html_filename,'w')
                # Initializa HTML with title
                self.html = PyH('CheckPages HTML report for %s !' % spider.start_url_domain)        
                # Adds the CSS and JS Bootstrap CDN 
                self.html.addCSS('http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css')
                self.html.addJS('http://netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js')        
                
                self.html << div('', cl="page-header ") << h1('URLs from ' + a(spider.start_urls[0], href=spider.start_urls[0]).render())
                self.html_container = self.html << div(cl="container-fluid") << div(cl="row")
                self.html_ok = self.html_container << div(cl="")
                self.html_err = self.html_container << div(cl="")
                

            
    def open_spider(self, spider):
        if not self.html_file: return
        self.itens = []
        # Well... nothing here yet.        

        
            

    def close_spider(self, spider):
        if not self.html_file: return        

        # sort itens alphabetically by title
        from operator import itemgetter        
        self.itens = sorted(self.itens, key=itemgetter('title', 'external'))


        self.html_container << '<table class="table table-bordered">'

        self.html_container << '''
        <thead>
          <tr>
            <th>HTTP</th>
            <th>Title + URL</th>
            <th>Referer</th>
            <th>Forb. words</th>
          </tr>
        </thead>
        <tbody>
        '''
        

        for item in self.itens:            
            http_status = int(item.get('http_status', 999))            
            
            # Set colors for HTTP erros (aprox.)
            item_class = 'danger';            
            if http_status < 400: item_class = 'primary';
            if http_status < 300: 
                item_class = 'success';                
                # do not list success when there were not forbidden words.
                if not item.get('forbidden_words',[]): continue

            
            self.html_container << '''            
              <tr class="%s">
                <td><small>%s</small></td>
                <td><small>
                    %s
                    <br>
                    <a href="%s">%s</a>
                    </small>
                </td>                
                <td><small><a href="%s"><span class="btn btn-mini btn-primary">See & Fix</span></a></small></td>                
                <td><small>%s</small></td>                
            </tr>
              
            ''' % ( item_class, 
                  http_status, 
                  item.get('title','(no title)'), 
                  item.get('url','(no url)'),                  
                  item.get('url','(no url)'),                  
                  item.get('referer','(no referer)'),                  
                  ', '.join(item.get('forbidden_words',[])),
                )
               
        
        
        self.html_container << '''
                </tbody>
            </table>'''
            
            
        # Write HTML to disk!        
        self.html_file.write(self.html.render())            




    def process_item(self, item, spider):
        # Initialize HTML file if it exists (done here to use the parameter from spider )
        self.initializeFile(spider)        
        self.itens.append(item)
        return item
    
    
    