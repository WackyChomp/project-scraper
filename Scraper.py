
from bs4 import BeautifulSoup
import requests
import urllib.request         #download from the sources attribute link

#Google images of monkeys
url = "https://www.google.com/search?q=monkey&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjp182qrrvvAhXMmeAKHXYwBU4Q_AUoAXoECAIQAw"

response = requests.get(url)         #requesting permission to take contents from url

soup = BeautifulSoup(response.content, "html.parser")     #instantiate web scraper / parser that iterates over HTML

images = soup.find_all("img" , attrs = {"class" : "rg_i Q4LulWd"})    #extract tags inside the string and stores them inside a list as a dictionary

number = 0

for image in images:
    image_src = image["src"]       #grab source URL for image inside the source attribute of the tag 
    urllib.request.urlretrieve(image_src , str(number))      #2nd parameter is the name of the file. Using number as an example 
    print(image_src)
    number += 1

#print(soup.prettify())         #prints out HTML file from URL