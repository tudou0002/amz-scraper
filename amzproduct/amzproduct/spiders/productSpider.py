import scrapy
from bs4 import BeautifulSoup
import re
from amzproduct.items import AmzproductItem
from scrapy.spiders import CSVFeedSpider
from scrapy.http import Request
from scrapy.utils.project import get_project_settings
# CSVFeedSpider
class ProductSpider(CSVFeedSpider):
    name = 'productSpider'
    allowed_domains = ["amazon.com"]
    custom_settings = {
        'LOG_LEVEL': 'ERROR',
        'LOG_ENABLED': True,
        'LOG_STDOUT': True
    }
    # start from the first page of search result
    start_urls = ['https://www.amazon.ca/s?k=table+lamp&qid=1584766372&ref=sr_pg_1']


    def __init__(self):
        self.declare_xpath()
        self.baseUrl = 'https://www.amazon.ca'

    
    def declare_xpath(self):
        """Set the XPath of our target items"""
        self.titleXpath = '//*[@id="title"]'
        self.priceXpath = '//*[@id="price_inside_buybox"]'
        self.priceXpath2 = '//*[@id="newBuyBoxPrice"]'
        self.priceXpath3 = '//*[@id="olp-upd-new-used"]/a/span'
        self.rankXpath = '//*[@id="SalesRank"]/td[2]/text()'
        self.rankXpath2 = '//*[@id="SalesRank"]/text()'
        self.sellerXpath = '//*[@id="bylineInfo"]'
        self.descriptionXpath = '//*[@id="feature-bullets"]'
        self.ratingXpath = '//*[@id="reviewsMedley"]/div/div[1]/div[2]/div[1]/div/div[2]/div/span/span'
        self.asinXpath = '//*[@id="prodDetails"]/div/div[2]/div[1]/div[2]/div/div/table/tbody/tr/td[starts-with(text(),"ASIN")]/../descendant::text()'
        self.asinXpath2 = '//*[@id="detail_bullets_id"]/table/tr/td/div/ul/li/b[starts-with(text(),"ASIN")]/../descendant::text()'
        self.imgXpath = '//*[@id="landingImage"]/@src'
        self.firstDateXpath = '//*[@id="prodDetails"]/div/div[2]/div[1]/div[2]/div/div/table/tbody/tr[5]/td[2]'
        self.firstDateXpath2 = '//*[@id="detail_bullets_id"]/table/tr/td/div/ul/li/b[starts-with(text()," Date")]/../descendant::text()'


    def parse(self, response):
        """Iterate every page of a auction and enter every link of the item"""
        # lastUrl = ''
        for item_link in response.xpath('//*[@class="a-link-normal a-text-normal"]/@href').extract():    
            url = self.baseUrl + item_link
            yield Request(url=url,callback=self.parse_item, dont_filter=True,meta = {'dont_redirect': True, "handle_httpstatus_list" : [301, 302, 303]})

        pagination_link = response.css('li.a-last a::attr(href)')[0].extract()
        pagination_url = self.baseUrl + pagination_link
        yield Request(url=pagination_url,callback=self.parse, dont_filter=True)


    def parse_item(self,response):
        item = AmzproductItem()

        # certain item page has different product detail layout
        Title = response.xpath(self.titleXpath).extract()
        Title = self.cleanText(self.parseText(self.listToStr(Title)))

        if response.xpath(self.priceXpath).extract()!=[]:
            Price = response.xpath(self.priceXpath).extract()
        elif response.xpath(self.priceXpath2).extract():
            Price = response.xpath(self.priceXpath2).extract()
        else:
            # cases that the item have multiple prices, fill in with the lowest price(may be used)
            Price = response.xpath(self.priceXpath3).extract()
        Price = self.cleanText(self.parseText(self.listToStr(Price)))

        Seller = response.xpath(self.sellerXpath).extract()
        Seller = self.cleanText(self.parseText(self.listToStr(Seller)))

        if response.xpath(self.firstDateXpath).extract()!=[]:
            Date = response.xpath(self.firstDateXpath).extract()
        else:
            Date = response.xpath(self.firstDateXpath2).extract()
        Date = self.cleanText(self.parseText(self.listToStr(Date)))

        Description = response.xpath(self.descriptionXpath).extract()
        Description = self.cleanText(self.parseText(self.listToStr(Description)))

        if response.xpath(self.asinXpath).extract()!=[]:
            Asin = response.xpath(self.asinXpath).extract()
        else:
            Asin = response.xpath(self.asinXpath2).extract()
        Asin = self.cleanText(self.parseText(self.listToStr(Asin)))

        Img = response.xpath(self.imgXpath).extract()
        Img = self.cleanText(self.parseText(self.listToStr(Img)))

        Rating = response.xpath(self.ratingXpath).extract()
        Rating = self.cleanText(self.parseText(self.listToStr(Rating)))

        if response.xpath(self.rankXpath).extract()!=[]:
            Rank = response.xpath(self.rankXpath).extract()
        else:
            Rank = response.xpath(self.rankXpath2).extract()
        Rank = self.cleanText(self.parseText(self.listToStr(Rank)))

        #Put each element into its item attribute.
        item['url'] = response.url
        item['title'] = Title
        item['price']  = Price
        item['seller']  = Seller
        item['firstDate'] = Date
        item['description'] = Description
        item['asin'] = Asin
        item['img'] = Img
        item['rank'] = Rank
        item['rating'] = Rating
        return item

        #Methods to clean and format text to make it easier to work with later
    def listToStr(self,MyList):
        dumm = ""
        MyList = [i.encode('utf-8') for i in MyList]
        for i in MyList:dumm = "{0}{1}".format(dumm,i)
        return dumm
 
    def parseText(self, str):
        soup = BeautifulSoup(str, 'html.parser')
        return re.sub(" +|\\n|\\r|\\t|\\0|\\x0b|\\xa0",' ',soup.get_text()).strip()
 
    def cleanText(self,text):
        soup = BeautifulSoup(text,'html.parser')
        text = soup.get_text()
        text = re.sub("( +|\\n|\\r|\\t|\\0|\\x0b|\\xa0|\\xbb|\\xab)+",' ',text).strip()
        return text