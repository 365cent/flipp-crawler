from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import requests
import json

productList = []

class Product:
    def __init__(self, name, price, image):
        self.name = name
        self.price = price
        self.image = image

# Set the path to your Chromedriver
chromedriver_path = "chromedriver-mac-arm64/chromedriver"

# Setting up the webdriver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

# Target URL
# url = 'https://flipp.com/en-ca/waterloo-on/flyer/6100182-food-basics-flyer?postal_code=N2J1A1'  # Replace with your target URL

# url = 'https://flipp.com/en-ca/waterloo-on/flyer/6100776-farm-boy-weekly?postal_code=N2J1A1'

url = 'https://flipp.com'
ip = '129.100.255.34'
key = '87EC23E8E747F2A23B0D702B35920F01'


# get domain name from url
protocol = url.split('/')[0]
domain = url.split('/')[2]

res = requests.get('https://geoip.mxtrans.net/json')

ip = json.loads(res.text)['ip']

res = requests.get('https://api.ip2location.io/?key=' + key + '&ip=' + ip)

postalCode = json.loads(res.text)['zip_code']
postalCode = postalCode.replace(' ', '')
print(postalCode)

geoUrl = 'https://flipp.com/flyers?postal_code=' + postalCode

driver.get(geoUrl)

# Wait for the page to load
driver.implicitly_wait(10)

cate = driver.find_element(By.XPATH, '//div[contains(@class, "categories")]')
gro = cate.find_element(By.XPATH, '//span[contains(text(), "Groceries")]')
groLink = gro.find_element(By.XPATH, '..').get_attribute('href')

groLink = protocol + '//' + domain + groLink

driver.get(groLink)
driver.implicitly_wait(10)

storeSection = driver.find_elements(By.TAG_NAME, 'flipp-flyer-listing-item')
for store in storeSection:
    storeLink = store.find_element(By.TAG_NAME, 'a').get_attribute('href')
    storeLink = protocol + '//' + domain + storeLink
    driver.get(storeLink)
    driver.implicitly_wait(10)

    storeName = driver.find_element(By.XPATH, '//h1/span').text
    print(storeName)
    print('-------------------')

    # select canvas tag from page
    canvas = driver.find_element(By.XPATH, '//canvas')

    # get links from canvas tag
    links = canvas.find_elements(By.TAG_NAME, 'a')

    for link in links:
        productLink = link.get_attribute('href')
        if productLink is not None:
            productLink = protocol + '//' + domain + productLink
            productList.append(productLink)



    for product in productList:
        productPrice = ''
        driver.get(product)
        driver.implicitly_wait(10)
        productName = driver.find_element(By.XPATH, '//h2/span').text
        priceElement = driver.find_elements(By.XPATH, '//flipp-price/span')
        productPrice = priceElement[0].text + '.' + priceElement[1].text
        imageElement = driver.find_element(By.XPATH, '//div[contains(@class, "item-info-image")]')
        productImage = imageElement.find_element(By.TAG_NAME, 'img').get_attribute('src')
        productObj = Product(productName, productPrice, productImage)
        productList.append(productObj)
        print("[" + productName + "]" + " $" + productPrice + " (" + productImage + ")")

# Close the browser
driver.quit()
