import scrapy
import json

class RoutesSpider(scrapy.Spider):
    name = 'routes'

    def start_requests(self):
        for i in range(1, 10000):
            url = 'https://flightaware.com/live/flight/BAW' + str(i)

            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        selectors = [selector for selector in response.css('script')
                     if '"friendlyName"' in selector.extract()]

        if not selectors:
            return

        data = selectors[0].extract()

        data = json.loads(data[data.find('=') + 1:data.rfind(';')])

        return { 'route': response.url.rsplit('/', 1)[-1],
                 'data': data }
