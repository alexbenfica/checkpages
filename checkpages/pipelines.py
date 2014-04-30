from scrapy.exceptions import DropItem
from scrapy import signals
from scrapy.contrib.exporter import XmlItemExporter



class FilterForbiddenWordsPipeline(object):
    """A pipeline for filtering out items which contain certain words in their description.
    These words are in a file sent via command line parameter and loaded in the spider __init__ """

    def process_item(self, item, spider):
        item['forbidden_words'] = []
        for word in spider.forbiddenWords:            
            if word in item['html'].lower():
                item['forbidden_words'].append(word)               
                
        print 'Filtering forbidden words : %s ' % ', '.join(item['forbidden_words'])                
        return item







class XmlExportPipeline(object):
    def __init__(self):
        self.files = {}

     
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('%s_products.xml' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = XmlItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item