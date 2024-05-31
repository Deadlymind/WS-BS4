import os
import logging
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import argparse
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"Error fetching URL {url}: {e}")
        return None

def parse_html(html):
    soup = bs(html, "html.parser")
    containers = soup.find_all("div", {"class": "css-1gatmva e1v1l3u10"})
    return containers

def extract_job_data(container):
    job_title = container.find("h2", {"class": "css-m604qf"})
    company_name = container.find("a", {"class": "css-17s97q8"})
    job_type = container.find("div", {"class": "css-1lh32fc"})

    if job_title and company_name and job_type:
        job_title_text = job_title.text.replace('-', ' ').replace(',', ' ').strip()
        company_name_text = company_name.text.replace('-', ' ').replace(',', ' ').strip()
        job_type_text = job_type.text.replace('-', ' ').replace(',', ' ').strip()
        return job_title_text, company_name_text, job_type_text
    else:
        return None, None, None

def scrape_jobs(base_url, num_pages):
    all_jobs = []
    for page in tqdm(range(num_pages), desc="Scraping pages"):
        url = f"{base_url}&start={page}"
        html = get_html(url)
        if html:
            containers = parse_html(html)
            for container in containers:
                job_title, company_name, job_type = extract_job_data(container)
                if job_title and company_name and job_type:
                    all_jobs.append((job_title, company_name, job_type))
    return all_jobs

def save_to_csv(data, file_path):
    df = pd.DataFrame(data, columns=["job_title", "company_name", "job_type"])
    df.to_csv(file_path, index=False, encoding='utf-8')

def main(base_url, num_pages, output_file):
    logging.info(f"Starting web scraping for {num_pages} pages...")
    job_data = scrape_jobs(base_url, num_pages)
    if job_data:
        save_to_csv(job_data, output_file)
        logging.info(f"Scraping completed. Data saved to {output_file}.")
    else:
        logging.warning("No job data scraped.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape job listings from Wuzzuf.")
    parser.add_argument("--pages", type=int, default=5, help="Number of pages to scrape")
    parser.add_argument("--output", type=str, default="wuzzuf-illustrator.csv", help="Output CSV file")
    args = parser.parse_args()

    BASE_URL = "https://wuzzuf.net/search/jobs/?a=spbg&q=illustrator"

    main(BASE_URL, args.pages, args.output)
