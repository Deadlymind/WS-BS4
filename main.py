from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import pandas as pd



url = "https://wuzzuf.net/search/jobs/?a=spbg&q=illustrator"
client = urlopen(url)

# reading the html
html = client.read()

# closing the request
client.close()

# creating an HTML parser Using BeautifulSoup
soup = bs(html, "html.parser")

# creating a container for the needed data
containers = soup.find_all("div", {"class": "css-1gatmva e1v1l3u10"})

# accessing page elemnts from the containers
print(containers[0].div.h2.text)

job_title = containers[0].findAll("h2", {"class": "css-m604qf"})

company_name = containers[0].findAll("a", {"class": "css-17s97q8"})
job_type = containers[0].findAll("div", {"class": "css-1lh32fc"})

# bringing the data to the screen

f = open("wuzzuf-illustrator.csv", "w")
header = "job_title,company_name,job_type\n"
f.write(header)

for container in containers:
    job_title = container.findAll("h2", {"class": "css-m604qf"})
    company_name = container.findAll("a", {"class": "css-17s97q8"})
    job_type = container.findAll("div", {"class": "css-1lh32fc"})

    f.write(job_title[0].text.replace(",", " ") + "," + company_name[0].text.replace(",", " ") + "," + job_type[0].text + "\n")

f.close()


# inputting the file into Pandas

data = pd.read_csv("wuzzuf-illustrator.csv")

data.info()