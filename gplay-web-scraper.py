from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os


class Product:
    def __init__(self, cp, op, p, n, u):
        self.current_price = cp
        self.old_price = op
        self.percent = p
        self.name = n
        self.url = u


def mainMenu():
    print("For what you would be scraping for: ")
    print("(1) Gaming Keyboard")
    print("(2) Gaming Mouse")
    print("(3) Gaming Mouse Pad")
    print("(4) Gaming Headphones")
    print("(5) QUIT PROGRAM")
    choice = int(input("Enter your choice: "))
    if (choice == 5) : exit(0)

    return {
        1: 'геймърски-клавиатури',
        2: 'геймърски-мишки',
        3: 'геймърски-падове-за-мишки',
        4: 'геймърски-слушалки'
    }.get(choice, 'not available !')


url = "https://gplay.bg/black-wknd-2020/"

options = Options()
driver = webdriver.Chrome(os.getcwd() + "/chromedriver")
ch = mainMenu()
driver.get(url+ch)
products_list = []
index = 0

if ch == "геймърски-мишки":
    pages = driver.find_element_by_xpath("//div/div[2]/div[4]/div[2]/div/ul/li[4]/a").text
else:
    pages = driver.find_element_by_xpath("//div/div[2]/div[4]/div[2]/div/ul/li[3]/a").text

for i in range(int(pages)):
    catalog = driver.find_elements_by_xpath(".//div/div[2]/div[4]/div[1]/div/div[1]")
    for prod in catalog:
        index += 1
        name = prod.find_element_by_xpath('.//a[2]').get_attribute('title')
        url_adr = prod.find_element_by_xpath('.//a[2]').get_attribute('href')
        try:
            old_price_int = prod.find_element_by_xpath('.//div[4]/div/div[1]/div/div[1]').text
            old_price_float = prod.find_element_by_xpath('.//div[4]/div/div[1]/div/div[3]/div[1]').text
            curr_price_int = prod.find_element_by_xpath('.//div[4]/div/div[2]/div/div[1]').text
            curr_price_float = prod.find_element_by_xpath('.//div[4]/div/div[2]/div/div[3]/div[1]').text
        except:
            print("==!!!!!!!!!!!!!==")
            print("Non-Valid Product at index = " + str(index))
            print("==!!!!!!!!!!!!!==")
            continue

        curr_price = curr_price_int + "." + curr_price_float
        old_price = old_price_int + "." + old_price_float
        percentage = float((abs(float(curr_price) - float(old_price)) / float(old_price)) * 100.0)
        products_list.append(Product(curr_price, old_price, percentage, name, url_adr))
        print("=================")
        print("Product Name: " + name)
        print("Old Price: " + old_price)
        print("New Price: " + curr_price)
        print("Percent Discount: " + str(round(percentage, 2)) + " %")
        print("Url: " + url_adr)

    if i+1 < int(pages):
        if len(catalog) == index:
            if ch == "геймърски-мишки":
                driver.find_element_by_xpath("//div/div[2]/div[4]/div[2]/div/ul/li[5]/a").click()
            else:
                driver.find_element_by_xpath("//div/div[2]/div[4]/div[2]/div/ul/li[4]/a").click()
            index = 0


max = products_list[0]

for x in range(len(products_list)):
    if products_list[x].percent > max.percent:
        max = products_list[x]

print("=================")
print("========The Biggest Discount In Percents(%) Is=========")
print("=================")
print("Product Name: " + max.name)
print("Old Price: " + max.old_price)
print("New Price: " + max.current_price)
print("Percent Discount: " + str(round(max.percent, 2)) + " %")
print("Url: " + max.url)
