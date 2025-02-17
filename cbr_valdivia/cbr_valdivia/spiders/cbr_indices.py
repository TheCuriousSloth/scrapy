import scrapy

class CbrIndicesSpider(scrapy.Spider):
    name = 'cbr_indices'
    allowed_domains = ['www.cbrvaldivia.cl']
    start_urls = ['http://www.cbrvaldivia.cl/indices']

    def parse(self, response):
        # Extraer datos usando selectores
        indices = response.css('table.indices')
        
        for indice in indices.css('tr'):
            yield {
                'nombre': indice.css('td:nth-child(1)::text').get(),
                'valor': indice.css('td:nth-child(2)::text').get(),
                'fecha': indice.css('td:nth-child(3)::text').get()
            }
        
        # Si hay paginación, seguir los enlaces
        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)