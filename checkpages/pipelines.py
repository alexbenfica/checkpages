from scrapy.exceptions import DropItem
from scrapy import signals


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



