import scrapy
from bs4 import BeautifulSoup
import re
from amzproduct.items import ReviewItem
from scrapy.spiders import CSVFeedSpider
from scrapy.http import Request
from scrapy.utils.project import get_project_settings
# CSVFeedSpider
class ReviewSpider(CSVFeedSpider):
    name = 'reviewSpider'
    allowed_domains = ["amazon.com"]
    custom_settings = {
        'LOG_LEVEL': 'ERROR',
        'LOG_ENABLED': True,
        'LOG_STDOUT': True
    }
    # start from the first page of search result
    start_urls = ['https://www.amazon.ca/s?k=table+lamp&qid=1584766372&ref=sr_pg_1']

    def __init__(self):
        self.declare_path()
        # self.asin = ''
        self.baseUrl = 'https://www.amazon.ca'

    
    def declare_path(self):
        """Set the XPath of our target items"""
        self.review_urlXpath = '//*[@id="reviews-medley-footer"]/div[2]/a/@href'
        self.dataCSS = '#cm_cr-review_list'
        self.reviewerCSS = '.a-profile-name'
        self.contentCSS = '.review-text'
        self.titleCSS = '.review-title'
        self.dateCSS = '.review-date'
        self.rateCSS = '.review-rating'
        self.asinXpath = '//*[@id="prodDetails"]/div/div[2]/div[1]/div[2]/div/div/table/tbody/tr/td[starts-with(text(),"ASIN")]/../descendant::text()'
        self.asinXpath2 = '//*[@id="detail_bullets_id"]/table/tr/td/div/ul/li/b[starts-with(text(),"ASIN")]/../descendant::text()'
        

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
        """scrape the asin and review link"""
        if response.xpath(self.asinXpath).extract()!=[]:
            Asin = response.xpath(self.asinXpath).extract()
        else:
            Asin = response.xpath(self.asinXpath2).extract()
        self.asin = self.cleanText(self.parseText(self.listToStr(Asin)))
        reviewUrl = response.xpath(self.review_urlXpath)[0].extract()
        url = self.baseUrl + reviewUrl
        yield Request(url=url,callback=self.parse_review, dont_filter=True,meta = {'dont_redirect': True, "handle_httpstatus_list" : [301, 302, 303]})


    def parse_review(self,response):
        """Parse each review"""
        #Get the Review List
        data = response.css(self.dataCSS)
        #Get the Name
        reviewers = data.css(self.reviewerCSS)
        #Get the Review Title
        titles = data.css(self.titleCSS)
        # Get the Ratings
        ratings = data.css(self.rateCSS)
        # Get the dates
        dates = data.css(self.dateCSS)
        # Get the users Comments
        comments = data.css('.review-text')

        count = 0
        #length = len(title)

        for title in titles:
            item = ReviewItem()

            Reviewer = reviewers[count].xpath(".//text()").extract()
            Reviewer = self.cleanText(self.parseText(self.listToStr(Reviewer)))

            Rate = ratings[count].xpath(".//text()").extract()
            Rate = self.cleanText(self.parseText(self.listToStr(Rate)))

            Date = dates[count].xpath(".//text()").extract()
            Date = self.cleanText(self.parseText(self.listToStr(Date)))

            Title = titles[count].xpath(".//text()").extract()
            Title = self.cleanText(self.parseText(self.listToStr(Title)))

            Content = comments[count].xpath(".//text()").extract()
            Content = self.cleanText(self.parseText(self.listToStr(Content)))

            item['asin'] = self.asin
            item['reviewer'] = Reviewer
            item['rate'] = Rate
            item['date'] = Date
            item['title'] = Title
            item['content'] = Content

            yield item
            count +=1

        #if count>=length:
        # after finishing the last review, go to the next page
        pagination_link = response.xpath('//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a/@href')[0].extract()
        pagination_url = self.baseUrl + pagination_link
        yield Request(url=pagination_url,callback=self.parse_review, dont_filter=True)

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
