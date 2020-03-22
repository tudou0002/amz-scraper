# Amazon product scraper

## Install
Type the following code in your shell.
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