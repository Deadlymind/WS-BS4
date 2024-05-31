from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import pandas as pd
import os

# Define the URL to scrape
url = "https://wuzzuf.net/search/jobs/?a=spbg&q=illustrator"

# Open the URL and read the HTML
client = urlopen(url)
html = client.read()
client.close()

# Parse the HTML using BeautifulSoup
soup = bs(html, "html.parser")

# Find the containers with the desired job information
containers = soup.find_all("div", {"class": "css-1gatmva e1v1l3u10"})

# Print the first job title for verification
if containers:
    print(containers[0].div.h2.text)

# Open a CSV file to write the job data
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'wuzzuf-illustrator.csv')
with open(file_path, "w", encoding='utf-8') as f:
    header = "job_title,company_name,job_type\n"
    f.write(header)

    # Loop through the containers and extract job data
    for container in containers:
        job_title = container.findAll("h2", {"class": "css-m604qf"})
        company_name = container.findAll("a", {"class": "css-17s97q8"})
        job_type = container.findAll("div", {"class": "css-1lh32fc"})

        # Write job data to the CSV file
        if job_title and company_name and job_type:
            f.write(f"{job_title[0].text.replace(',', ' ')},"
                    f"{company_name[0].text.replace('-', ' ')},"
                    f"{job_type[0].text}\n")

# Read the CSV file into a Pandas DataFrame
data = pd.read_csv(file_path)

# Print the first few rows of the DataFrame
print(data.head())
