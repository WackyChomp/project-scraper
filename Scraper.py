
from bs4 import BeautifulSoup
import requests

#Google images of monkeys
url = "https://www.google.com/search?q=monkey&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjp182qrrvvAhXMmeAKHXYwBU4Q_AUoAXoECAIQAw"

response = requests.get(url)         #requesting permission to take contents from url

soup = BeautifulSoup(response.content, "html.parser")     #instantiate web scraper / parser that iterates over HTML

image = soup.find_all("img")          #extract tags inside the string and stores them inside a list
 

#print(soup.prettify())         #prints out HTML file from URL