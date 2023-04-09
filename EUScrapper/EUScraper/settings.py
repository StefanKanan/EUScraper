BOT_NAME = 'EUScraper'

SPIDER_MODULES = ['EUScraper.spiders']
NEWSPIDER_MODULE = 'EUScraper.spiders'

FEED_URI = './results.json'
FEED_FORMAT = 'jsonlines'
FEED_EXPORTERS = {'json': 'scrapy.exporters.JsonLinesItemExporter'}
FEED_EXPORT_ENCODING = 'utf-8'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'EUScraper.pipelines.FileItemPipeline': 1,
    'EUScraper.pipelines.ImageItemPipeline': 1,
    # 'scrapy.pipelines.images.ImagesPipeline': 1,
    # 'scrapy.pipelines.files.FilesPipeline': 1
   # 'EUScraper.pipelines.EuscraperPipeline': 300,
}

FILES_STORE = './attachments'
IMAGES_STORE = './images'

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'

LOG_STDOUT = True
LOG_FILE = 'C:/Users/Kanan/Desktop/EUScrapper/EUScraper/logs/log.txt'