import scrapy
import json


class MainSpider(scrapy.Spider):
    name = 'main-spider'

    start_urls = ['https://br.op.gg/champion/statistics']

    list_completed = []

    def parse(self, response):
        links = response.css('div[class=champion-index__champion-list] a::attr("href")').getall()
        for link in links:
            yield scrapy.Request(
                'https://br.op.gg' + link,
                callback=self.parse_champion
            )

    def parse_champion(self, response):
        champ = {
            'name': response.css('h1::text').getall(),
            'rune': response.xpath('//div[@class="perk-page__item perk-page__item--keystone perk-page__item--active"]//img/@alt').getall()[:1],
            'primaria': response.xpath('//div[@class="perk-page__item  perk-page__item--active"]//img/@alt').getall()[:3],
            'secundaria': response.xpath('//div[@class="perk-page__item perk-page__item--active"]//img/@alt').getall()[:2],
            'fragmento': response.xpath('//img[re:test(@class, "active")]/@alt').getall()[:3]
        }
        self.list_completed.append(champ)

    def close(self, spider, reason):
        with open('champions.json', 'w') as f:
            self.list_completed = sorted(self.list_completed, key=lambda k: k['name'])
            f.write(json.dumps(self.list_completed))
            f.close()
