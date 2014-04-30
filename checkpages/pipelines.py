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

            
    def open_spider(self, spider):
        if not self.html_file: return
        self.itens = []
        # Well... nothing here yet.        

        
            

    def close_spider(self, spider):
        if not self.html_file: return        

        # sort itens alphabetically by title
        from operator import itemgetter        
        self.itens = sorted(self.itens, key=itemgetter('title', 'external'))



        
        def html_page_header(title, subtitle, content): 
            return '''
            <div class="page-header">
              <h1>%s <small> %s </small></h1>
              %s
            </div>
        ''' % (title , subtitle, content)
        
        
        html_errors = ''
        html_ok = ''

        for item in self.itens:            
            
            http_status = int(item.get('http_status', 999))                        
            # Set colors for each HTTP erros (aprox.)
            item_class = 'danger';            
            if http_status < 400: item_class = 'primary';
            if http_status < 300: item_class = 'success';                
                
            item_has_errors = False
            if item.get('forbidden_words',[]): item_has_errors = True
            if http_status >= 400: item_has_errors = True
            
            
            if item_has_errors:
                html_referer = '<small><a href="%s"><span class="btn btn-mini btn-danger"><span class="glyphicon glyphicon-wrench"></span> Visit and Fix</span></a></small>' % item.get('referer','(no referer)')
            else:
                html_referer = '<small><a href="%s"><span class="btn btn-mini btn-success">Visit</span></a></small>' % item.get('referer','(no referer)')
                
            
            icon_external = ''
            if item['external']:
                icon_external = '<span class="glyphicon glyphicon-share" title="This is an external link"></span>'
            
            html_item = '''            
              <tr class="%s">                
                <td>%s %s
                    <br>                    
                    <small><a href="%s">%s</a></small>                    
                    <span class="pull-right">(<strong>%s</strong>)</span>
                </td>                
                <td>%s</td>                
                <td><small>%s</small></td>                
            </tr>
              
            ''' % ( item_class,                   
                  icon_external,
                  item.get('title','(no title)'), 
                  item.get('url','(no url)'),                  
                  item.get('url','(no url)'),                  
                  http_status, 
                  html_referer,                  
                  ', '.join(item.get('forbidden_words',[])),
                )
        
            if item_has_errors:
                html_errors += html_item
            else:
                html_ok += html_item
                
               
        


        
        html_table_open = '''   
            <table class="table table-bordered thumbnail">
                <thead>
                  <tr>                    
                    <th>HTTP Status + Page title + URL</th>
                    <th>Referer</th>
                    <th>Forb. words</th>
                  </tr>
                </thead>
                <tbody>
            '''
        
        
        html_table_close = '''        
                </tbody>
            </table>
            '''

        
        self.html_container << html_page_header('Links with problems', 'You must check and fix each one', html_table_open + html_errors + html_table_close )        
        
        self.html_container << html_page_header('Links  apparently ok', 'You can visit each one here', html_table_open + html_ok + html_table_close  )        

            
        # Write HTML to disk!        
        self.html_file.write(self.html.render())            




    def process_item(self, item, spider):
        # Initialize HTML file if it exists (done here to use the parameter from spider )
        self.initializeFile(spider)        
        self.itens.append(item)
        return item
    
    
    