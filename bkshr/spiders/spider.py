import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import BkshrItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class BksSpider(scrapy.Spider):
	name = 'bksbank'
	start_urls = ['https://www.bks.hr/o-nama/novosti']

	def parse(self, response):
		post_links = response.xpath('//div[@class="news-item-content"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class=" lfr-icon-item taglib-icon"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)


	def parse_post(self, response):

		date = response.xpath('//h1/following-sibling::p//text()').get()
		title = response.xpath('//div[@class="content-large"]/h1//text()').getall()
		title = ''.join(title).strip()
		content = response.xpath('//div[@class="portlet-content-container"]//div[@class="journal-content-article"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))


		item = ItemLoader(item=BkshrItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		return item.load_item()