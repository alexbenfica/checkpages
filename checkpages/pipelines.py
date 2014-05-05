from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import signals
from scrapy.http import Request

import os



# https://code.google.com/p/pyh/
# install it using python setup.py install
from pyh import *





class FilterForbiddenWordsPipeline(object):
    """A pipeline for filtering out items which contain certain words in their description.
    These words are in a file sent via command line parameter and loaded in the spider __init__ """

    def process_item(self, item, spider):
        
        item['forbidden_words'] = []
        
        # Never tries to findo forbidden words on external links.
        # Some links points to foruns or pages that has the words that are forbidden. 
        # As anyone can control external pages, does not make sense alarm this situation!
        if item.get('external'): return item
        
        html_lower = item['html'].lower()
        for word in spider.forbiddenWords:            
            if word.lower() in html_lower:
                item['forbidden_words'].append(word)
                
        #print 'Filtering forbidden words : %s ' % ', '.join(item['forbidden_words'])                
        #print
        return item









class HTMLWriterPipeline(object):
    """ Pipiline to write a HTML file report from the screpped links."""

    def __init__(self):
        self.html_file = None
        self.itens = []
        
        
    def createPath(dirPath):
        path, filename = os.path.split(dirPath)
        if not os.path.isdir(path):
            try:
                os.makedirs(path)
            except:
                print 'Could not create path for file %s. ' % filename
                print 'Path: %s (maybe it already exists or it is locked!)' % (path)
        
        

    def initializeFile(self, spider):
        if spider.output_html_filename:
            if not self.html_file: 
                self.createPath(spider.output_html_filename)
                self.html_file = open(spider.output_html_filename,'w')
                # Initializa HTML with title
                self.html = PyH('CheckPages HTML report for %s !' % spider.start_url_domain)
                # Adds the CSS and JS Bootstrap CDN 
                self.html.addCSS('http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css')
                self.html.addJS('http://netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js')        
                
                self.html.head += '<meta charset="utf8">'
                
                self.html << div('', cl="page-header ") << h1('URLs from ' + a(spider.start_urls[0], href=spider.start_urls[0]).render())
                self.html_container = self.html << div(cl="container-fluid") << div(cl="row")

            
    def open_spider(self, spider):
        self.spider = spider
        if not self.html_file: return
        self.itens = []
        # Well... nothing here yet.        

        
            
    # With all downloade itens available, generate the HTML report!
    def close_spider(self, spider):
        if not self.html_file: return        

        # sort itens alphabetically by title
        from operator import itemgetter        
        self.itens = sorted(self.itens, key=itemgetter('title', 'external'))
        



        
        def get_html_page_header(title, subtitle, content): 
            return '''
            <div class="page-header">
              <h1>%s <small> %s </small></h1>
              %s
            </div>
        ''' % (title , subtitle, content)
        


        def get_html_item(item_class, icon, title, url, http_status, fix_url, forbidden_words = '' ):             
            html_item =  '''            
              <tr class="%s">                
                <td>%s | %s<small> | <a href="%s">%s</a></small>                    
                    <span class="pull-right">(<strong>%s</strong>)</span>
                </td>                
                <td>%s</td>                
                <td><small>%s</small></td>                
            </tr>

            ''' % ( item_class,                   
                  icon,
                  title, 
                  url,                  
                  url,                  
                  http_status, 
                  fix_url,                  
                  ', '.join(forbidden_words),
                )
                
            #html_item = html_item.decode('utf-8', 'ignore')
            #html_item = html_item.encode('utf-8', 'ignore')
                
            return html_item
                
        
        
        
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
                if item.get('forbidden_words',''):
                    fix_url = '<small><a href="%s"><span class="btn btn-mini btn-danger"><span class="glyphicon glyphicon-wrench"></span> Visit to Fix</span></a></small>' % item.get('url','(no url)')
                else:
                    fix_url = '<small><a href="%s"><span class="btn btn-mini btn-danger"><span class="glyphicon glyphicon-wrench"></span> Visit to Fix</span></a></small>' % item.get('referer','(no referer)')                    
            else:
                fix_url = '<small><a href="%s"><span class="btn btn-mini btn-success">Visit</span></a></small>' % item.get('referer','(no referer)')
                
            
            icon = ''
            if item['external']:
                icon = '<span class="glyphicon glyphicon-share" title="This is an external link"></span>'

            html_item = get_html_item(item_class, icon, item.get('title','(no title)'), item.get('url','(no url)'), http_status, fix_url, item.get('forbidden_words',[]))

            if item_has_errors:
                html_errors += html_item
            else:
                html_ok += html_item
                


        for item in self.itens:            
            
            # Each imagens is considered an "item" for this HTML output
            iImage = -1
            for img in item.get('image_urls',[]):                
                iImage += 1
                
                image_item_has_errors = not item['images'][iImage][0]
                
                item_class = 'danger';
                if item['images'][iImage][0] == True:  item_class = 'success';
                
                title = '(image)'
                
                if image_item_has_errors:
                    fix_url = '<small><a href="%s"><span class="btn btn-mini btn-danger"><span class="glyphicon glyphicon-wrench"></span> Visit to Fix</span></a></small>' % item.get('url','(no referer)')
                else:
                    fix_url = '<small><a href="%s"><span class="btn btn-mini btn-success">Visit</span></a></small>' % item.get('url','(no referer)')
                    
                
                url = img
                
                #print url                
                #url = 'url'
                
                
                icon = ''
                if self.spider.is_external(url):
                    icon = '<span class="glyphicon glyphicon-share" title="This is an external link"></span>'
                    
                # Put an extra icon to identify a image
                icon += '<span class="glyphicon glyphicon-picture" title="This is an image link"></span>'
                
                #print img
                #print item['images'][iImage]
                
                if image_item_has_errors:
                    # Forced
                    http_status = 404
                    html_errors += get_html_item(item_class, icon, title, url , http_status, fix_url)
                else:
                    http_status = 200
                    html_ok += get_html_item(item_class, icon, title, url , http_status, fix_url)
                    pass
                    
                
                
                
                
            
        
               
            #print item['images']
        


        
        html_table_open = '''   
            <table class="table table-bordered thumbnail">
                <thead>
                  <tr>                    
                    <th>Page title | URL | HTTP Code</th>
                    <th>Where to fix</th>
                    <th>Forb. words</th>
                  </tr>
                </thead>
                <tbody>
            '''
        
        html_table_close = '''        
                </tbody>
            </table>
            '''

        
        self.html_container << get_html_page_header('Links and images with problems', '', html_table_open + html_errors + html_table_close )        
        
        self.html_container << get_html_page_header('Links and images ok', '', html_table_open + html_ok + html_table_close  )        

            
        # Write HTML to disk!        
        self.html_file.write(self.html.render())            




    def process_item(self, item, spider):
        # Initialize HTML file if it exists (done here to use the parameter from spider )
        self.initializeFile(spider)        
        self.itens.append(item)
        return item
    
    
    
    
    
    
    
    
    
    
    
    
class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            print ' - Adding image url to the download queue: %s' % image_url
            yield Request(image_url)


    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        
        item['images'] += results
        
        if len(results): print ' - Finished downloading of the following images:'
        
        iImage = 0
        for image_result in results:
            download_status = image_result[0]
            if download_status == True:
                print '     Status: %s | Url: %s '  % (download_status , image_result[1].get('url','') )
            else:
                print '     Status: %s | Url: %s '  % (download_status , item['image_urls'][iImage] )
            iImage += 1
                
            #print image_result
        
        if not image_paths:            
            #raise DropItem("Item contains no images")
            return item
        
        #item['image_paths'] = image_paths
        return item    
    
    

    