# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
import hashlib
import json

from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from scrapy.utils.python import to_bytes
from .spiders.newsletterSpider import NewsletterSpider
import os
from urllib.parse import urlparse
import logging

same_files_set = set()
same_files_hash = {}
same_images_hash = {}
logger = logging.getLogger('logger')

class FileItemPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        path = os.path.basename(urlparse(request.url).path)
        if path in same_files_set:
            logger.warning(f'LOG: duplicate name {path}')

        same_files_set.add(path)

        hashed_path = hashlib.sha1(to_bytes(request.url.strip())).hexdigest()
        if path in same_files_hash.keys() and same_files_hash[path][0] != hashed_path:
            same_files_hash[path].append(request.url)
            logger.warning(f'LOG: different file with same filename found {path} from url: {request.url} and in {same_files_hash[path][1]}')
        else:
            same_files_hash[path] = [hashed_path, request.url]

        ext = ''
        file_path = urlparse(request.url).path
        if file_path in NewsletterSpider.attachment_type.keys():
            ext = f'.{NewsletterSpider.attachment_type[file_path]}'
        elif request.url in NewsletterSpider.attachment_type.keys():
            ext = f'.{NewsletterSpider.attachment_type[request.url]}'

        file_path = '/'.join(file_path.split('/')[:-1])

        # logger.warning(f'FILE PATH: {file_path}')
        # os.makedirs(f'{os.getcwd()}/attachments/{file_path}')

        return f'{urlparse(request.url).path}{ext}'
        # return f'{os.path.basename(urlparse(request.url).path)}{ext}'

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        logger.warning(f'LOG RESULTS {results}')
        for index, result in enumerate(results):
            try:
                isOk, result_dict = result
                result_dict['relative'] = urlparse(result_dict['url']).path
                if result_dict['relative'] in NewsletterSpider.attachment_type.keys(): # Not used in experimental mode TODO Delete
                    result_dict['type'] = NewsletterSpider.attachment_type[result_dict['relative']]
                elif result_dict['url'] in NewsletterSpider.attachment_type.keys():
                    result_dict['type'] = NewsletterSpider.attachment_type[result_dict['url']]
                else:
                    logger.warning(f'No such file type for {result_dict["relative"]} - {result_dict["url"]}')
                    logger.warning(f'Attachment Type {NewsletterSpider.attachment_type.items()}')
                results[index] = (isOk, result_dict)
            except Exception as exc:
                logger.error(f'CUSTOM ERROR')
                logger.error(f'Results: {results}')
                logger.error(f'result_dict: {result}')
                logger.error(f'item: {item}')
                logger.error(exc)
        return super(FileItemPipeline, self).item_completed(results, item, info)

class ImageItemPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        path = os.path.basename(urlparse(request.url).path)
        if path in same_files_set:
            logger.warning(f'LOG: duplicate name {path}')

        same_files_set.add(path)

        hashed_path = hashlib.sha1(to_bytes(request.url.strip())).hexdigest()
        if path in same_images_hash.keys() and same_images_hash[path] != hashed_path:
            logger.warning(f'LOG: different image with same filename found {path}')
        same_images_hash[path] = hashed_path

        return os.path.basename(urlparse(request.url).path)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        logger.warning(f'LOG {results}')
        for index, result in enumerate(results):
            try:
                isOk, result_dict = result
                result_dict['relative'] = urlparse(result_dict['url']).path
                results[index] = (isOk, result_dict)
            except Exception as exc:
                logger.error(f'CUSTOM ERROR')
                logger.error(f'Results: {results}')
                logger.error(f'result_dict: {result}')
                logger.error(exc)

        return super(ImageItemPipeline, self).item_completed(results, item, info)

class EuscraperPipeline:
    def process_item(self, item, spider):
        return item
