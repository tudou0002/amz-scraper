# Amazon product scraper
- There are two kinds of spiders, namely the 'ProductSpider' and the 'ReviewSpider'. Their column descriptions are given as follows.
- An improvement would be to add proxies in `setting.py` to avoid getting block
- 'table lamp' is used as a search result(base URL) in this example.

## Features of item
### Product
- title: Title of the product. 商品全称
- price: Price scraped from the buy box, if it's null, fill in with the lowest price among all suppliers(including used product). Buy Box中的商品价格， 若没有buy box， 则爬取所有供应商（包括二手）的最低价
- seller: Seller of the product. 卖家名称
- rating: Rate of a product(out of 5). 商品评分（5分制）
- ranking: Amazon Bestsellers Rank. 亚马逊畅销排行。 为了体现可比性， 只爬取了同一类别下的排行
- asin: Amazon Standard Identification Number. A 10-charcter alphanumeric unique identifier that's assigned by Amazon.com and its partners. Can be used as a foreign key in the database. 亚马逊标准识别码， 每个商品拥有独特的识别码。可被用作数据库中表的外键。
- firstDate: Date first available at Amazon.ca. 初上价日期
- img: Link for the first image in the product page. 第一张展示图的链接
- description: The most outstanding product features. 主要的产品信息
- url: Link to each product's page. 每个商品页面的链接

### Review
- asin: Amazon Standard Identification Number. A 10-charcter alphanumeric unique identifier that's assigned by Amazon.com and its partners. Can be used as a foreign key in the database. 亚马逊标准识别码， 每个商品拥有独特的识别码。可被用作数据库中表的外键。同一商品的评价asin一致
- reviewer: User name of a review. 单条评论的用户名
- rate: Rate of a product(out of 5). 单条评分（5分制）
- date: Date and region of a review. 单条评论的日期与地区
- title: The title of a review(if null, record as N/A). 单条评论的标题
- content: The content of a review. 单条评论的内容

## Install
Type the following code in your shell to start a new project.
```shell
# create a new virtual env
python3 -m venv env 
# activate the env
source env/bin/activate
# install scrapy with pip3
pip3 install -r requirements.txt
# to start a new project
scrapy startproject <project_name>
```

## start to crawl
```shell
# to store the scraped items into a csv
scrapy crawl waitems -t csv -o [filename.csv]
```