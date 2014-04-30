from scrapy.item import Item, Field


class Page(Item):    
    url = Field()
    referer = Field()
    title = Field()
    http_status = Field()
    html = Field()
    external = Field()
    forbidden_words = Field()
    
