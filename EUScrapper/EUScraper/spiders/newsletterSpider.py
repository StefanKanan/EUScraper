import scrapy

from EUScraper.items import *


class NewsletterSpider(scrapy.Spider):
    name = "newsletter"
    start_urls = ['http://www.nalas.eu/Press-Centre/press-releases',
                  'http://www.nalas.eu/Publications/Books',
                  'http://www.nalas.eu/Publications/Newsletter',
                  'http://www.nalas.eu/News',
                  'http://nalas.eu/Announcements',
                  'http://nalas.eu/knowledge-center/Policy-positions',
                  'http://nalas.eu/services/quick-responces']

    attachment_type = {}

    def parse(self, response, **kwargs):
        page = response.url

        index = response.meta['article_index'] if 'article_index' in response.meta.keys() else 0
        links = response.xpath('//ul//li[contains(@class, "media")]//a[contains(., "Read more")]/@href').getall()
        dates = response.xpath('//ul//li[contains(@class, "media")]//h4//span[contains(@class, "media-date")]/text()').getall()
        for date, link in zip(dates, links):
            yield response.follow(link, callback=self.parse_pressRelease, meta={'parent_url': page, 'article_index': index, 'published_on': date})
            index += 1

        next_page = response.xpath('//ul//li//a[contains(., "Next")]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse, meta={'article_index': index})
        else:
            response.meta['article_index'] = 0

    def parse_pressRelease(self, response):
        page = response.url
        main_class = '//div[contains(@class, "post")]'
        title = response.xpath(f'{main_class}//h2/text()').get()

        images = response.xpath(f'{main_class}//img/@src').getall()
        imageItem = ImageItem()
        imageItem['image_urls'] = []
        for image in images:
            imageItem['image_urls'].append(response.urljoin(image))
        # yield imageItem

        body = response.xpath('//div[contains(@class, "description")]').get()

        # TODO
        # Experimental
        # attachments = response.xpath(f'{main_class}//a/@href').getall()
        # attachmentItem = FileItem()
        # attachmentItem['file_urls'] = []
        # from urllib.parse import urlparse
        # for attachment in attachments:
        #     if bool(urlparse(attachment).netloc) and not [x for x in self.start_urls if urlparse(attachment).netloc in x or 'www.nalas.eu' in x]:
        #         continue
        #     import requests
        #     if 'mailto' in attachment:
        #         continue
        #     file_response = requests.get(response.urljoin(attachment)) if not bool(urplarse(attachment).netloc) else requests.get(attachment)
        #     if file_response.status_code == 200 and self.parse_attachment_experimental(file_response):
        #     # if response.follow(attachment, callback = self.parse_attachment_experimental):
        #         if bool(urlparse(attachment).netloc):
        #             import logging
        #             logger = logging.getLogger('logger')
        #             logger.warning(f'CUSTOM LOG: absolute path {attachment}')
        #         attachmentItem['file_urls'].append(response.urljoin(attachment))

        attachments = response.xpath(f'{main_class}//a[count(img)>0]/@href').getall()
        attachments_types = response.xpath(f'{main_class}//a[count(img)>0]//img/@src').getall()
        attachmentItem = FileItem()
        attachmentItem['file_urls'] = []
        for attachment, type in zip(attachments, attachments_types):
            self.attachment_type[attachment] = type.split('/')[-1].split('.')[0]
            attachmentItem['file_urls'].append(response.urljoin(attachment))
        # yield attachmentItem

        exportItem = Item()
        exportItem['parent_url'] = response.meta['parent_url']
        exportItem['url'] = page
        exportItem['title'] = title
        exportItem['article_index'] = response.meta['article_index']
        exportItem['published_on'] = response.meta['published_on']
        exportItem['body'] = body
        exportItem['image_urls'] = imageItem['image_urls']
        exportItem['file_urls'] = attachmentItem['file_urls']

        yield exportItem

    def parse_attachment_experimental(self, response):
        content_type = str(response.headers['Content-Type'])
        return not ('text' in content_type or 'mailto' in content_type)

    # def parse_attachment(self, response):
    #     page = response.url
    #     content_type = response.headers['content-type']
    #
    #     if 'allowed' in content_type:
    #         #download
    #         pass