# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import re
import mysql.connector
from mysql.connector import errorcode

class AmzproductPipeline(object):
    def strip(self, item, spider, attr,remove=''):
        '''remove the noise text in the result'''
        if item.get(attr):
            if not item[attr] == None:
                # remove special chars in the text
                item[attr] = re.sub(r"( +|\\n|\\r|\\t|\\0|\\x\w\w)+", ' ', item[attr])
                # remove the quotation marks at begining and ending
                item[attr] = re.sub(r"(^b'|^\")*('$|\"$)*", '', item[attr])
                # self-defined chars to remove
                item[attr] = re.sub(remove, '', item[attr])
            if item[attr] =='N/A':
                item[attr] = None

    def process_item(self, item, spider):

        self.strip(item,spider,'title')
        self.strip(item,spider,'price',remove='[^0-9.]')
        self.strip(item,spider,'seller')
        self.strip(item,spider,'rating',remove='( out of 5)')
        self.strip(item,spider,'asin',remove='(ASIN|:| |\'b\')*')
        self.strip(item,spider,'rank',remove=',|\'b\'')
        self.strip(item,spider,'img',remove=' *')
        self.strip(item,spider,'firstDate',remove='( *Date *first *available *at *Amazon\. *ca *: *\'b\' |.)')
        self.strip(item,spider,'description')
        print('Scraping item ' + item['title'])
        return item


class ReviewPipeline(object):
    def strip(self, item, spider, attr,remove=''):
        '''remove the noise text in the result'''
        if item.get(attr):
            if not item[attr] == None:
                # remove special chars in the text
                item[attr] = re.sub(r"( +|\\n|\\r|\\t|\\0|\\x\w\w)+", ' ', item[attr])
                # remove the quotation marks at begining and ending
                item[attr] = re.sub(r"(^b'|^\")*('$|\"$)*", '', item[attr])
                item[attr] = re.sub(r"b\'|\"*|\'b|\'$", '', item[attr])
                # self-defined chars to remove
                item[attr] = re.sub(remove, '', item[attr])
            if item[attr] =='N/A':
                item[attr] = None

    def process_item(self, item, spider):
        self.strip(item,spider,'asin',remove='(ASIN|:| |\'b\'|\')*')
        self.strip(item,spider,'content')
        self.strip(item,spider,'date',remove='(\")*')
        self.strip(item,spider,'rate',remove='( out of 5 stars)')
        self.strip(item,spider,'reviewer')
        self.strip(item,spider,'title')
        print('Scraping review ' + item['title'])
        return item
