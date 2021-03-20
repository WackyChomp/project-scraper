
from bs4 import BeautifulSoup
import requests
import urllib.request

#Google images of monkeys
url = "https://www.google.com/search?q=monkey&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjp182qrrvvAhXMmeAKHXYwBU4Q_AUoAXoECAIQAw"

response = requests.get(url)         #requesting permission to take contents from url

soup = BeautifulSoup(response.content, "html.parser")     #instantiate web scraper / parser that iterates over HTML

image = soup.find_all("img" , attrs = {"class" : "rg_i Q4LulWd"})    #extract tags inside the string and stores them inside a list as a dictionary



#print(soup.prettify())         #prints out HTML file from URL