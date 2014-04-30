# Scrapy settings for checkpages project

SPIDER_MODULES = ['checkpages.spiders']

NEWSPIDER_MODULE = 'checkpages.spiders'
DEFAULT_ITEM_CLASS = 'checkpages.items.Page'

ITEM_PIPELINES = {'checkpages.pipelines.FilterForbiddenWordsPipeline': 1}
#ITEM_PIPELINES = {'checkpages.pipelines.FilterWordsPipeline': 1}


RETRY_TIMES = 1
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]
DOWNLOAD_TIMEOUT = 10

LOG_FILE = '/tmp/checkpages-crawler.log'