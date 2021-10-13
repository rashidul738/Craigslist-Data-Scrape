import scrapy
from scrapy import Request

class ListSpider(scrapy.Spider):
    name = 'list'
    allowed_domains = ['newyork.craigslist.org']
    start_urls = ['https://newyork.craigslist.org/d/household-services/search/hss']

    def parse(self, response):
        listings = response.xpath('//li[@class="result-row"]')
        for listing in listings:
            date = listing.xpath('.//time[@class="result-date"]/@datetime').get()
            link = listing.xpath('.//a[@class="result-title hdrlnk"]/@href').get()
            name = listing.xpath('.//a[@class="result-title hdrlnk"]/text()').get()
            yield{
                'Date': date,
                'Link': link,
                'Name': name}
        
        next_page_url = response.xpath('//*[@class="button next"]/@href').get()
        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)

