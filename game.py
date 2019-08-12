from random import choice
from csv import DictReader
from bs4 import BeautifulSoup
import requests


def start_game():
    url = "http://quotes.toscrape.com"
    with open("title_author_bio-link.csv", "r", encoding="utf-8") as csv_file:
        csv_reader = DictReader(csv_file)
        quotes = list(csv_reader)
    print("Here's a quote:")
    quote = choice(quotes)
    print(quote["text"])
    guesses_left = 4
    guess = ""
    while guess.lower() != quote["author"].lower() and guesses_left > 0:
        guess = input(f"Who said this quote? Guesses left: {guesses_left}\n")
        guesses_left -= 1
        if guess.lower() == quote["author"].lower():
            print("You got it right!")
            break
        if guesses_left == 3:
            res = requests.get(f"{url}{quote['bio-link']}")
            soup = BeautifulSoup(res.text, "html.parser")
            birth_date = soup.find(class_="author-born-date").get_text()
            birth_place = soup.find(class_="author-born-location").get_text()
            print(
                f"Here's a hint: The author was born on {birth_date} {birth_place}")
        elif guesses_left == 2:
            print(
                f"Here's a hint: The author's first name starts with: {quote['author'][0]}")
        elif guesses_left == 1:
            last_initial = quote['author'].split(" ")[1][0]
            print(
                f"Here's a hint: The author's last name starts with: {last_initial}")
        else:
            print("You ran out of guesses!")
            print(f"The author was {quote['author']}")


play_again = ''
start_game()
while play_again not in ('y', 'yes', 'n', 'no'):
    play_again = input("Would you like to play again (y/n)? ")
    if play_again in ('y', 'yes'):
        start_game()
        play_again = input("Would you like to play again (y/n)?")
    else:
        break
