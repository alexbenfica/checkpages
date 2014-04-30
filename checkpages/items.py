from scrapy.item import Item, Field


class Page(Item):    
    url = Field()
    referer = Field()
    title = Field()
    status = Field()
    html = Field()
    external = Field()
    forbidden_words = Field()
    
