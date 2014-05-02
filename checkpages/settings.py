from scrapy import log

# Scrapy settings for checkpages project

SPIDER_MODULES = ['checkpages.spiders']

NEWSPIDER_MODULE = 'checkpages.spiders'
DEFAULT_ITEM_CLASS = 'checkpages.items.Page'

ITEM_PIPELINES = {  'checkpages.pipelines.FilterForbiddenWordsPipeline': 3, 
                    'checkpages.pipelines.HTMLWriterPipeline': 2,
                    'checkpages.pipelines.MyImagesPipeline': 1,
                    #'scrapy.contrib.pipeline.images.ImagesPipeline': 1,                    
                }



# Optional configuration for image downloading.
IMAGES_STORE = '/media/sf_C_DRIVE/Temp/'

# These are useful when you are actually doing a crawler.
# As I am doing a page check, I intend to download all images I found!
#IMAGES_MIN_HEIGHT = 400
#IMAGES_MIN_WIDTH = 300




# Configurations for page downloads
RETRY_TIMES = 1
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]
DOWNLOAD_TIMEOUT = 10




# Log settings
#LOG_FILE = '/tmp/checkpages-crawler.log'

LOG_LEVEL = log.CRITICAL
LOG_LEVEL = log.ERROR
#LOG_LEVEL = log.WARNING
#LOG_LEVEL = log.INFO
#LOG_LEVEL = log.DEBUG