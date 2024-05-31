from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import pandas as pd
import os

# Define the base URL and the number of pages to scrape
base_url = "https://wuzzuf.net/search/jobs/?a=spbg&q=illustrator&start="
num_pages = 15  # Adjust the number of pages as needed

# Open a CSV file to write the job data
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'wuzzuf-illustrator.csv')
with open(file_path, "w", encoding='utf-8') as f:
    header = "job_title,company_name,job_type\n"
    f.write(header)

    # Loop through the specified number of pages
    for page in range(num_pages):
        url = base_url + str(page)
        client = urlopen(url)
        html = client.read()
        client.close()

        # Parse the HTML using BeautifulSoup
        soup = bs(html, "html.parser")

        # Find the containers with the desired job information
        containers = soup.find_all("div", {"class": "css-1gatmva e1v1l3u10"})

        # Extract and write job data to the CSV file
        for container in containers:
            job_title = container.findAll("h2", {"class": "css-m604qf"})
            company_name = container.findAll("a", {"class": "css-17s97q8"})
            job_type = container.findAll("div", {"class": "css-1lh32fc"})

            # Write job data to the CSV file
            if job_title and company_name and job_type:
                job_title_text = job_title[0].text.replace(',', ' ').replace(',', ' ')
                company_name_text = company_name[0].text.replace('-', ' ').replace(',', ' ')
                job_type_text = job_type[0].text.replace(',', ' ').replace(',', ' ')

                f.write(f'"{job_title_text}","{company_name_text}","{job_type_text}"\n')

# Read the CSV file into a Pandas DataFrame
data = pd.read_csv(file_path)

# Print the first few rows of the DataFrame
print(data.head())
