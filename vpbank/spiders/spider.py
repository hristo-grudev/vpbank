import scrapy

from scrapy.loader import ItemLoader
from ..items import VpbankItem
from itemloaders.processors import TakeFirst


class VpbankSpider(scrapy.Spider):
	name = 'vpbank'
	start_urls = ['https://www.vpbank.com/en/media/media-releases']

	def parse(self, response):
		post_links = response.xpath('//article/div/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="text-box -big -nopadding"]//text()|//section//div[@id][position()<last()]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="text-box -small _text-uppercase"]/time/text()').get()

		item = ItemLoader(item=VpbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
