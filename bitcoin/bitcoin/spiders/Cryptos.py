import scrapy  
from datetime import datetime


# links = //div[@class="price-liststyles__CardGrid-sc-1adi55e-1 kSWqZP"]/a/@href
# Name = //div[@class='inner-column']/span[@class='typography__StyledTypography-owin6q-0 curhyt']/text()
# Price = //div[@class='field-item even']//p[not(@class)]/text() 

now = datetime.now() 
current_time = now.strftime("%d-%m-%Y")

# Name
XPATH_NAME = "//div[@class='Box-sc-1hpkeeg-0 headerstyles__Wrapper-sc-11sja2z-0 hOYELT']/h1/text()"
# Simbol
XPATH_SIMBOL = "//div[@class='Box-sc-1hpkeeg-0 headerstyles__Wrapper-sc-11sja2z-0 hOYELT']/span[@class='typography__StyledTypography-owin6q-0 ijCvot short-title']/text()"
# Price
XPATH_PRICE = "//div[@class='Box-sc-1hpkeeg-0 imwELA']/span['typography__StyledTypography-owin6q-0 bnYzDk chromexPathFinder'][2]/text()" 
# Links 
XPATH_LINKS = "//div[@class='price-liststyles__CardGrid-sc-1adi55e-1 kSWqZP']/a/@href" 

class SpiderCIA(scrapy.Spider):

    name = 'coin'
    start_urls = [
        'https://www.coindesk.com/data/'
    ]

    custom_settings={
        'FEEDS':{
            'Coins.csv':{
                'format': 'csv',
                'encoding': 'utf-8'
                
                }
                },
    }

 
    def parse(self, response):
        links_declassified = response.xpath(XPATH_LINKS).getall()
        for link in links_declassified:
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url': response.urljoin(link)})

    def parse_link(self, response, **kwargs):
        link = kwargs['url']
        simbol = response.xpath(XPATH_SIMBOL).get() 
        price = response.xpath(XPATH_PRICE).get() 
        name_coin = response.xpath(XPATH_NAME).get()
        

        yield { 
            'Name': name_coin,
            'Simbolo': simbol, 
            'Precio': price, 
            'Fecha': current_time,
            'Link': link
            
            
        }