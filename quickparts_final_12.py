from bs4 import BeautifulSoup
import requests
import random
import csv
from time import sleep

url = "https://quickparts.se/reservdelar-tillbehor"
html_content = requests.get(url).text
soup = BeautifulSoup(html_content, "lxml")

file = open('homer.csv', 'w')
writer = csv.writer(file)

for link in soup.find_all("ul", {"class": ["menulist", "level1"]}):
    for li in link.select('li a'):
        category_link = "https://quickparts.se" + li.get("href")  # get the absolute link for category
        category = category_link.split('/')[-1]  # Get the text for category from the link
        brand_html_content = requests.get(category_link).text  # call the new link for categoer
        brand_soup = BeautifulSoup(brand_html_content, "lxml")
        for brand_ul in brand_soup.find_all("ul", {"class": ["menulist", "level2"]}):
            for brand_li in brand_ul.select('li a'):
                brand_link = "https://quickparts.se" + brand_li.get("href")
                brand_name = brand_link.split('/')[-1]
                if category in brand_link.casefold() and brand_link.casefold() != category_link.casefold():
                    product_group_html_content = requests.get(brand_link).text  # call the new link for categoer
                    product_group_soup = BeautifulSoup(product_group_html_content, "lxml")
                    for product_group_ul in product_group_soup.find_all("ul", {"class": ["menulist", "level3"]}):
                        for product_group_li in product_group_ul.select('li a'):
                            product_group_link = "https://quickparts.se" + product_group_li.get("href")
                            product_group_name = product_group_link.split('/')[-1]
                            if category in product_group_link.casefold() and \
                                    brand_name in product_group_link.casefold() and \
                                    brand_link.casefold() != category_link.casefold() and \
                                    product_group_link.casefold() != brand_link.casefold():
                                # print(product_group_link)
                                seconds_for_sleeping = random.random()
                                # print("sleeping for " + str(seconds_for_sleeping))
                                sleep(seconds_for_sleeping)
                                product_list_html_content = requests.get(
                                    product_group_link).text  # get all products links
                                product_list_soup = BeautifulSoup(product_list_html_content, "lxml")
                                for product_list_item in product_list_soup.find_all("div", {"class": "productinfo"}):
                                    for product_link_relative in product_list_item.select('a'):
                                        product_link_absolute = "https://quickparts.se" + product_link_relative.get(
                                            "href")
                                        # print(product_link_absolute)
                                        product_html_content = requests.get(product_link_absolute).text
                                        product_soup = BeautifulSoup(product_html_content, "lxml")
                                        for product_ul_fittolist in product_soup.find_all("ul", {"class": "fitToList"}):
                                            for product_li_item in product_ul_fittolist.select('ul li'):
                                                brand = product_li_item.find("a")
                                                for test in product_li_item.select("ul.models li"):
                                                    trimmedText = test.text.replace(brand.text, "").replace(
                                                        "                            ", "").replace(" - ", "|").replace(
                                                        "\n", "").replace("\r", "").strip()

                                                    print(brand.text + "|" + trimmedText)
                                                    writer.writerow([brand.text + "|" + trimmedText])
file.close()
