from scrapy import log

# Scrapy settings for checkpages project

SPIDER_MODULES = ['checkpages.spiders']

NEWSPIDER_MODULE = 'checkpages.spiders'
DEFAULT_ITEM_CLASS = 'checkpages.items.Page'

ITEM_PIPELINES = {'checkpages.pipelines.FilterForbiddenWordsPipeline': 1}


RETRY_TIMES = 1
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]
DOWNLOAD_TIMEOUT = 10


# Log settings

#LOG_FILE = '/tmp/checkpages-crawler.log'

LOG_LEVEL = log.CRITICAL
LOG_LEVEL = log.ERROR
LOG_LEVEL = log.WARNING
LOG_LEVEL = log.INFO
#LOG_LEVEL = log.DEBUG