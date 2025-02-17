import scrapy
from scrapy.http import FormRequest

class CbrIndicesSpider(scrapy.Spider):
    name = 'cbr_indices'
    allowed_domains = ['www.cbrvaldivia.cl']
    start_urls = ['http://www.cbrvaldivia.cl/indices']

    def start_requests(self):
        # Enviar solicitud POST con los parámetros de año
        return [FormRequest(url=self.start_urls[0],
                            formdata={'anio_desde': '2020', 'anio_hasta': '2025'},
                            callback=self.parse)]

    def parse(self, response):
        # Imprimir el HTML para depuración
        self.logger.debug(response.text)
        
        # Extraer datos de la ventana modal
        modal = response.css('#modal-miventana')
        indices = modal.css('table.indices')
        
        for indice in indices.css('tr'):
            yield {
                'foja': indice.css('td:nth-child(1)::text').get(),
                'numero': indice.css('td:nth-child(2)::text').get(),
                'bis': indice.css('td:nth-child(3)::text').get(),
                'anio': indice.css('td:nth-child(4)::text').get(),
                'fecha': indice.css('td:nth-child(5)::text').get(),
                'acto_contrato': indice.css('td:nth-child(6)::text').get(),
                'numero_solicitud': indice.css('td:nth-child(7)::text').get()
            }