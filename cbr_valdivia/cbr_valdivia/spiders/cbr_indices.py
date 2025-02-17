import scrapy
from scrapy.http import FormRequest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.selector import Selector

class CbrIndicesSpider(scrapy.Spider):
    name = 'cbr_indices'
    allowed_domains = ['www.cbrvaldivia.cl']
    start_urls = ['http://www.cbrvaldivia.cl/indices']

    def __init__(self, *args, **kwargs):
        super(CbrIndicesSpider, self).__init__(*args, **kwargs)
        self.driver = webdriver.Chrome()  # Asegúrate de tener el controlador de Chrome instalado

    def start_requests(self):
        self.driver.get(self.start_urls[0])
        
        # Enviar solicitud POST con los parámetros de año
        anio_desde = self.driver.find_element(By.ID, 'anio_registro')
        anio_hasta = self.driver.find_element(By.ID, 'anio_registro2')
        anio_desde.send_keys('2020')
        anio_hasta.send_keys('2025')
        
        consultar_button = self.driver.find_element(By.ID, 'consultar_ind')
        consultar_button.click()
        
        # Esperar a que la ventana modal se cargue
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'modal-miventana'))
        )
        
        # Extraer datos de la ventana modal
        self.parse(self.driver.page_source)
        
        self.driver.quit()

    def parse(self, html):
        response = Selector(text=html)
        modal = response.css('#modal-miventana')
        indices = modal.css('div.content > div.table-responsive-sm > table > tbody > tr')
        
        for indice in indices:
            yield {
                'foja': indice.css('td:nth-child(1)::text').get(),
                'numero': indice.css('td:nth-child(2)::text').get(),
                'bis': indice.css('td:nth-child(3)::text').get(),
                'anio': indice.css('td:nth-child(4)::text').get(),
                'fecha': indice.css('td:nth-child(5)::text').get(),
                'acto_contrato': indice.css('td:nth-child(6)::text').get(),
                'numero_solicitud': indice.css('td:nth-child(7)::text').get()
            }