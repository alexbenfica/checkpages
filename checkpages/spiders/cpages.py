import os.path
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from checkpages.items import Page






class CPages(CrawlSpider):
    
    name = "cpages"

    countPages = {'internal':0, 'external': 0}
    

    handle_httpstatus_list = [404, 503] 
    
    def __init__(self, start_url='', output_file='', forbidden_words_file='',  *args, **kwargs):
        super(CPages, self).__init__(*args, **kwargs)
        
        self.start_urls = [start_url]                
        self.start_url_domain = start_url.split('//')[-1].replace('www.','').strip('/')

        self.rules = (
            Rule(SgmlLinkExtractor(allow = (self.start_url_domain)) , follow=True, callback='parse_internal', process_links='process_links'),            
            Rule(SgmlLinkExtractor(allow = ("[^%s]" % self.start_url_domain)), callback='parse_external',follow=False, process_links='process_links'),
        )        
        
        # Apply the new rules...
        CrawlSpider._compile_rules(self)
        
        
        # Load the file with the forbidden words
        self.forbiddenWords = []
        if forbidden_words_file:
            if os.path.exists(forbidden_words_file):                
                self.forbiddenWords = open(forbidden_words_file,'r').read().lower().split("\n")
                print 'Forbidden words loaded from file: %s' % forbidden_words_file
                print self.forbiddenWords
        
        
        #exit()
        


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
        return not self.start_url_domain in url
    

    def parse_internal(self, response):
        
        sel = Selector(response)
        page = Page()
        
        page['status'] = response.status
        page['url'] = response.url        
        page['referer'] = response.request.headers['referer']      
        page['title'] = sel.xpath('//title/text()').extract()
        
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
        print 'HTTP Status Code: %d' % page['status']        
        print 'External: %s' %  page['external']
        
        
        return page
        

        
        
