from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs4

options = Options()
#options.add_argument("--headless")

class ClimaTempo:
    def __init__(self, driver=webdriver.Chrome(chrome_options=options)):
        self.driver = driver
        self.url = 'http://google.com.br'
        self.search_bar = '//*[@id="tsf"]/div[2]/div/div[1]/div/div[1]/input'
        self.btn_lucky = '//*[@id="tsf"]/div[2]/div/div[3]/center/input[2]'
        self.clima = {}
    def navigate(self):
        self.driver.get(self.url)
    def search(self, word='São Paulo'):
        self.navigate()
        self.city = word.upper()
        self.driver.find_element_by_xpath(self.search_bar).send_keys('climatempo climatologia '+word)
        self.driver.find_element_by_xpath(self.btn_lucky).click()
        return self.driver.page_source
    def parser(self, city):
        self.city = city
        page = bs4(self.search(city), 'html.parser')
        tbody = page.find_all('body')
        trs = tbody[0].find_all('ul')
        for tr in range(len(trs)):
            mes = trs[tr].find(
                'li', {'class': 'text-center normal font14 txt-blue'}).text
            outros = trs[tr].find_all(''
                'li', {'class': 'text-center normal font14 txt-black'})
            self.clima[mes] = {
                'Minima (Cº)': outros[0].text,
                'Maxima (Cº)': outros[1].text,
                'Precipitação (mm)': outros[2].text
            }
            self.driver.quit()
            return self.clima
x = ClimaTempo()
x.navigate()
print(x.parser('rio de janeiro'))
