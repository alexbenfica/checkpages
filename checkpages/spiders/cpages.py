import os.path
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from checkpages.items import Page



class CPages(CrawlSpider):
    
    name = "cpages"

    countPages = {'internal':0, 'external': 0}

    # Allow all http status code ( maybe there exists a constant to to that )
    handle_httpstatus_list = range(100,506)
    

    
    def __init__(self, 
            start_url = '', 
            output_html_filename = '', 
            forbidden_words_file = '',  
            *args, **kwargs ):
            
        super(CPages, self).__init__(*args, **kwargs)
        
        self.start_urls = [start_url]                
        self.start_url_domain = start_url.split('//')[-1].replace('www.','').strip('/')

        
        regex_to_internal = "((\/\/)|(http\:\/\/)|(www.))+"+self.start_url_domain+"[^.][^?&]*"
        
        # The URL is processed by the first rules that matches!
        # So ay other URLs are considered external and will not be followed, but will have the header requested to see if they are available, find 404 and so on.
        regex_to_external = ".*"

        #print regex_to_external
        #print regex_to_internal         
        #exit()
        

        self.rules = (
            # Rule to get internal links
            Rule(
                SgmlLinkExtractor(
                    allow = (regex_to_internal),
                ) , 
                follow=True, 
                callback='parse_internal', 
                process_links='process_links'
            ),            
                
            # Rule to get external links (process but not follow them )
            Rule(
                SgmlLinkExtractor(
                    allow = (regex_to_external)
                ), 
                callback='parse_external',
                follow=False, 
                process_links='process_links'
            ),
        )        
        
        
        # Apply the new rules...
        CrawlSpider._compile_rules(self)
        
        
        # Load the file with the forbidden words
        self.forbiddenWords = []
        if forbidden_words_file:
            if os.path.exists(forbidden_words_file):                
                self.forbiddenWords = open(forbidden_words_file,'r').read().split("\n")
                print 'Forbidden seccessfully words loaded from file: %s' % forbidden_words_file
                #print self.forbiddenWords
        

        # Load the output file name inside the class variable to be used in a pipeline
        self.output_html_filename = output_html_filename
        





    def process_links(self,links):
        for link in links:            
            if self.is_external(link.url):
                # Do nothing... :)
                #print link.url            
                pass
        return links




    def parse_external(self, response):                
        # Allow to parse using the same function, but do not follow!
        return self.parse_internal(response)



    # Return if a url is external, given the start_url domain
    def is_external(self, url):        
        if 'http://' + self.start_url_domain + '/' in url:
            return False
        if 'http://www.' + self.start_url_domain + '/' in url:
            return False        
        return True
    

    def parse_internal(self, response):
        
        sel = Selector(response)
        page = Page()
        
        page['http_status'] = response.status
        page['url'] = response.url        
        page['referer'] = response.request.headers['referer']      
        
        page['title'] = sel.xpath('//title/text()').extract()
        if page['title']: 
            page['title'] = page['title'][0].encode('utf-8')            
        else:
            page['title'] = '(no title)'
        
        page['html'] = response.body
        #page['html'] = ''       
        
        
        page['external'] =  self.is_external(page['url'])        
        if page['external']:
            self.countPages['external'] += 1
        else:
            self.countPages['internal'] += 1
             
        
        # Output on screen
        print "\n"*2      
        print '# Ext.: %04d   |  Int.: %04d   |  TOTAL: %04d' % ( self.countPages['external'], self.countPages['internal'], self.countPages['external'] + self.countPages['internal'])
        print 'Parsed URL: [%s]' % page['url']
        print 'HTTP Status Code: %d' % page['http_status']        
        print 'Referer: %s' % page['referer']        
        print 'External: %s' %  page['external']
        
        
        return page
        



        
        
