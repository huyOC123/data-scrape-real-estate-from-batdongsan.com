# data-scrape-real-estate-from-batdongsan.com

Overview

This Python script scrapes real estate listings from batdongsan.com.vn, specifically for apartments in Hà Nội. It uses Selenium and BeautifulSoup to extract listing details, including:

Property Name

Size (m²)

Location

Price per m² (million VND)

Total Price (billion VND)

The script utilizes multithreading via ThreadPoolExecutor to speed up data collection across multiple pages.

Features

✅ Web Scraping with Selenium and BeautifulSoup✅ Multithreaded Execution for faster processing✅ Data Export to Excel (.xlsx) using Pandas✅ Logging System for progress tracking

Installation

Ensure you have the following dependencies installed:

pip install selenium beautifulsoup4 pandas openpyxl

ChromeDriver Setup

Download the ChromeDriver matching your Google Chrome version from ChromeDriver.

Update the path in the script:

cService = ChromeService(executable_path="C:\\Program Files (x86)\\chromedriver.exe")

Usage

Run the script with:

cctest.py

The script will scrape 1,496 pages (configurable) using 5 threads and save the extracted data in real_estate_multithreaded.xlsx.

Configuration

You can modify these variables in the script:

# Total number of pages to scrape
total_pages = 1496  

# Number of threads
threads = 5  

Notes

Ensure ChromeDriver is installed and correctly referenced.

Increase wait times (WebDriverWait) if the script fails due to page loading issues.

Modify XPath/CSS selectors if the website structure changes.
