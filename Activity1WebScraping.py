import requests
from bs4 import BeautifulSoup
import codecs

url = "https://en.wikipedia.org/wiki/Pennsylvania_State_University"

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')
infoBox = soup.find("table", class_="infobox vcard")

webScrape = {"Univeristy": "The Pennsylvania State University"}
wantedInfo = ["Motto", "Type", "Established", "Academic affiliations",
            "Endowment", "Budget", "President", "Provost", 
            "Academic staff", "Students", "Undergraduates", 
            "Postgraduates", "Location", "Campus", "Newspaper", 
            "Colors", "Nickname", "Sporting affiliations", "Mascot", "Website"]
    
#Get all of the data inside info box
for tr in infoBox.find_all("tr"):
    if len(tr.findChildren("th", recursive=False)) > 0 and \
        len(tr.findChildren("td", recursive=False)) > 0:
            
        #Grab table header and table data
        header = tr.findChildren("th", recursive=False)[0]
        data = tr.findChildren("td", recursive=False)[0]

        #Add to dictionary if not in it already
        if header.get_text() not in webScrape and header.get_text() in wantedInfo:
            #Decompose unwanted tags
            while data("sup"):
                data.find("sup").decompose()
            while data("span") and header.get_text() != "Website":
                data.find("span").decompose()
            webScrape[header.get_text()] = data.get_text()
    
#Writing to file
with codecs.open("webScrape.txt", "w", encoding="utf-8") as output_data:
    for key in webScrape.keys():
        output_data.write("{}: {}\n".format(key, webScrape[key]))