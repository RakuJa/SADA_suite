import os
import sys
from bs4 import BeautifulSoup
import requests_random_user_agent

# This library will randomize user agent, don't delete

import certifi

from src.web_scraper.connection_tools import download_page


requests_random_user_agent
BASE_URL_LIST = ["https://www.amazon.it/s?k="]
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()


def scrape_html(page) -> dict:
    """
    This method will get name, price and currency tag from html
    :param page: the html page to scrape, already downloaded
    :return: return dictionary with item name as a key
    and price and currency in a vector as value
    """
    soup = BeautifulSoup(page.content, "html.parser")  # This will contain the html page

    # gets item name list
    item_found = soup.findAll(
        "span", {"class": "a-size-base-plus a-color-base a-text-normal"}
    )
    # gets item price list
    price_found = soup.findAll("span", {"class": "a-price-whole"})
    # gets item currency list
    currency_found = soup.findAll("span", {"class": "a-price-symbol"})
    item_dictionary = {}
    for (curr_name, curr_price, curr_currency) in zip(
        item_found, price_found, currency_found
    ):
        # gets name, price and currency strings
        name = curr_name.get_text()
        price = curr_price.get_text()
        currency = curr_currency.get_text()
        # put the value in a dictionary, name is a key,
        # [price, currency] a value as a vector
        item_dictionary[name] = [price, currency]
    return item_dictionary


def print_dictionary(dictionary) -> None:
    """
    Prints a dictionary row by row as follows, key : value
    :param dictionary: dictionary to print out
    :return: None
    """
    for item in dictionary:
        tmp_vector = dictionary[item]
        currency = tmp_vector.pop()
        price = tmp_vector.pop()
        print(item + " : " + price + " " + currency)


def start():
    while True:
        name = input("Enter product to search for : ")
        product_list = name.split()
        result_string = product_list[0]
        product_list.remove(product_list[0])
        for substring in product_list:
            result_string += str(str("+") + str(substring))

        full_url = BASE_URL_LIST[0] + result_string

        page = download_page(full_url)
        item_dictionary = scrape_html(page)
        print_dictionary(item_dictionary)

        user_input = input("Search for another product? Y/N : ")
        if user_input.upper() == "N":
            sys.exit()
