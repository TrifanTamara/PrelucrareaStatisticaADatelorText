from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request
import csv
import json

def cleanPrice(priceValue):
    result = str(priceValue).replace('<sup>', ',').replace('</sup>', '').replace('<span>Lei</span>', '')
    result = result.replace('<p class=\"product-new-price\">', '').replace('</p>', '')
    result = result.replace('Lei', '').strip()
    result = result.replace('.', '').replace(',', '.').replace('<s>', '').replace('</s>','')
    return result.strip()

def cleanString(stringToClean):
    stringToClean = stringToClean.replace("\n", "").strip()
    stringToClean = stringToClean.replace("\n", "").strip()
    return stringToClean.replace("\n", "").strip()

def parseEmagProduct(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')

    laptopname = soup.find('h1', attrs={'class':'page-title'}).text
    new_price = cleanPrice(soup.find('p', attrs={'class':'product-new-price'}))
    old_price = cleanPrice(soup.find('p', attrs={'class':'product-old-price'}).find('s', attrs={'':''}))
    
    import re

    nr_reviews = soup.find('div', attrs={'class', 'product-highlight'}).find_all('a', attrs={'href', re.compile(r'gtm_*')})[0].text
    nr_reviews = nr_reviews.replace("\n", "").strip().split(' ')[0]
    
    rating = soup.find('span', attrs={'class', 'star-rating-text'}).text
    rating = rating.replace("\n", "").strip()
    #available = soup.find('span', attrs={'class':'stocky-txt in-stock'}).text

    #specsTable = soup.find('div', attrs={'class':'spec-table-col'})
    #productSpecs = specsTable.find_all('th', attrs={'class':'label'})
    #productValues = specsTable.find_all('td', attrs={'class':'data'})

    finalResult = {}

    all_tables = soup.find_all('table', attrs={'class', 'product-page-specifications'})
    for table in all_tables:
        trs = table.find_all("tr")
        for tr in trs:
            lst = tr.find_all("td")
            if(len(lst)==2):
                key = cleanString(lst[0].text)
                value = cleanString(lst[1].text)
                finalResult[key] = value

    finalResult["Product name"] = laptopname
    finalResult["New price"] = new_price
    finalResult["Old price"] = old_price
    finalResult["Reviews"] = nr_reviews
    finalResult["Rating"] = rating
    #finalResult["Disponibilitate"] = available
    #for i in range(0, len(productSpecs)):
    #    key = productSpecs[i].text.replace(":", "")
    #    value = productValues[i].text
    #    finalResult[key] = value
    
    return finalResult

def exportToCsv(phoneSpecs):
    productname = phoneSpecs["Product name"]
    with open(productname + '.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file,)
        for key, value in phoneSpecs.items():
            writer.writerow([key, value])

productLinks = ['https://www.emag.ro/laptop-lenovo-v130-15ikb-cu-procesor-intelr-coretm-i5-7200u-pana-la-3-10-ghz-kaby-lake-15-6-4gb-500gb-intelr-hd-graphics-620-free-dos-iron-grey-81hn00guri/pd/DP3KFQBBM/']

# for productLink in productLinks:
#     productSpecs = parseFlancoProduct(productLink)
#     print(productSpecs)
#    exportToCsv(productSpecs)


initialLink = 'https://www.emag.ro/laptopuri/p4/c'
baseUrl = 'https://www.emag.ro/laptopuri/'

def getLinks(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')

    allContainers = soup.find_all("div", attrs={"class", "js-product-data"})
    allurls = []
    for container in allContainers:
        allurls.append(container.find("h2", attrs={'class', 'product-title-zone'}).find("a", attrs={"class", "js-product-url"}).attrs['href'])
    return allurls


def getAllProductsFromCategory(baseUrl):
    allLinks = []
    for i in range(1, 29):
        url = f'{baseUrl}/p{i}/c'
        links = getLinks(url)
        allLinks += links
    return allLinks

def saveToFile(fileName, data):
    with open(fileName + '.json', 'w') as f:
        json.dump(data, f)

def readJsonFromFile(file):
    with open(file) as json_file:
        data = json.load(json_file)
        return data

def getAllLinksAndSave():
    allLinks = getAllProductsFromCategory(baseUrl)
    print(len(allLinks))
    saveToFile("lins", allLinks)

# allLinks = readJsonFromFile("links.json")
# print(len(allLinks))

def generateProductsFromLinks(links):
    products = []
    successParsed = 0
    failedProducts = 0
    for link in links:
        try:
            product = parseEmagProduct(link)
            successParsed += 1
            print(f"Parsed product {successParsed}.")
            products.append(product)
        except Exception as e:
            print(f"Failed. Reason: {str(e)}.")
            failedProducts += 1
    print("Done!")
    print(f"Parsed products: {successParsed}. Failed in parsing: {failedProducts}.")
    saveToFile("allproductsparsed", products)

#generateProductsFromLinks(allLinks)

#data = readJsonFromFile("allproductsparesd.json")


import pandas
pandas.read_json("allproductsparsed copy.json").to_excel("output.xlsx")
