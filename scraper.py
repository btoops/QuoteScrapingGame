# http://quotes.toscrape.com
import requests
from bs4 import BeautifulSoup
from csv import DictWriter
from time import sleep

original_url = "http://quotes.toscrape.com"
next_page = "/page/1/"

with open("title_author_bio-link.csv", "w", encoding="utf-8") as csv_file:
    headers = ("text", "author", "bio-link")
    csv_writer = DictWriter(csv_file, fieldnames=headers)
    csv_writer.writeheader()
    while next_page:
        res = requests.get(f"{original_url}{next_page}")
        soup = BeautifulSoup(res.text, "html.parser")
        quotes = soup.find_all(class_="quote")
        for quote in quotes:
            all_quotes = ({
                "text": quote.find(class_='text').get_text(),
                "author": quote.find(class_='author').get_text(),
                "bio-link": quote.find("a")["href"]
            })
            csv_writer.writerow(all_quotes)
        next_button = soup.find(class_="next")
        next_page = next_button.find("a")["href"] if next_button else None
        sleep(2)
