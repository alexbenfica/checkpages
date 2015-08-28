from scrapy import log
import sys







# Scrapy settings for checkpages project

SPIDER_MODULES = ['checkpages.spiders']

NEWSPIDER_MODULE = 'checkpages.spiders'
DEFAULT_ITEM_CLASS = 'checkpages.items.Page'

ITEM_PIPELINES = {  'checkpages.pipelines.FilterForbiddenWordsPipeline': 3, 
                    'checkpages.pipelines.HTMLWriterPipeline': 2,
                    'checkpages.pipelines.MyImagesPipeline': 1,
                    #'scrapy.contrib.pipeline.images.ImagesPipeline': 1,                    
                }





# Get the parameter which specify image downloading path
#print sys.argv
output_image_folder = ''
for arg in sys.argv:    
    if 'output_image_folder' in arg:
        output_image_folder = arg.split('=')[-1]
        
if output_image_folder:        
    IMAGES_STORE = output_image_folder
else:
    print 'You must specify a folder where images downloaded will be stored!'
    print 'Do it adding the followint to the command line: -a output_image_folder=/path/to/image/dir'
    sys.exit('Check your command line parameters!')






# These are useful when you are actually doing a crawler.
# As I am doing a page check, I intend to download all images I found!
#IMAGES_MIN_HEIGHT = 400
#IMAGES_MIN_WIDTH = 300




# Configurations for page downloads
RETRY_TIMES = 1
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]
DOWNLOAD_TIMEOUT = 10

#Default: 0
#The amount of time (in secs) that the downloader should wait before downloading 
#consecutive pages from the same website. 
#This can be used to throttle the crawling speed to avoid hitting servers too hard.
DOWNLOAD_DELAY = 0.5

# Change the order of downloads, getting first those near the root
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'


# Log settings
#LOG_FILE = '/tmp/checkpages-crawler.log'

LOG_LEVEL = log.CRITICAL
LOG_LEVEL = log.ERROR
#LOG_LEVEL = log.WARNING
#LOG_LEVEL = log.INFO
#LOG_LEVEL = log.DEBUG