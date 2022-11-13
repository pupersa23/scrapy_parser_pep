import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        pep_table = response.xpath(
            '//section[@id="numerical-index"]//tbody//tr')
        for row in pep_table:
            pep_link = row.css('a.reference::attr(href)').get()
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        title = 'h1.page-title::text'
        number = int(response.css(title).re_first(r'PEP (\d+)'))
        name = response.css(title).get()
        status = response.css('dt:contains("Status") + dd::text').get()
        data = {
            'number': number,
            'name': name,
            'status': status,
        }
        yield PepParseItem(data)
