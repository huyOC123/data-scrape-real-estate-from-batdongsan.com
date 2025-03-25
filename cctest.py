import sys
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor
import threading


sys.stdout.reconfigure(encoding='utf-8')


log_lock = threading.Lock()


def safe_log(message):
    with log_lock:
        print(message)

#scrape pages
def scrape_pages(start_page, end_page, thread_id):
    real_estate = []

    # Browser setup
    cOptions = Options()
    cOptions.add_experimental_option("detach", True)
    cService = ChromeService(executable_path="C:\\Program Files (x86)\\chromedriver.exe")
    driver = webdriver.Chrome(service=cService, options=cOptions)

    url = f"https://batdongsan.com.vn/ban-can-ho-chung-cu-ha-noi?cIds=650,362,41,325,163,575,361,40,283,44,562,45,48&p={start_page}"
    driver.get(url)

    try:
        for i in range(start_page, 3):#end_page +1 
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.re__main"))
                )
            except Exception as e:
                safe_log(f"Thread {thread_id} - Page {i}: Content load timeout. Error: {e}")
                break


            soup = BeautifulSoup(driver.page_source, "html.parser")
            
            for item in soup.find_all('div', class_='js__card'):
                try:
                    real_estate_name = item.find('span', class_='pr-title js__card-title').text.strip()
                    real_estate_size = item.find('span', class_='re__card-config-area js__card-config-item').text.replace('m²', '')
                    real_estate_location = item.find('div', class_='re__card-location').text.replace('·', '').strip()
                    real_estate_price_per_m_square = item.find('span', class_='re__card-config-price_per_m2 js__card-config-item').text.replace('tr/m²', '')
                    real_estate_total_price = item.find('span', class_='re__card-config-price js__card-config-item').text.replace(',', '.').replace('tỷ', '')

                    if "Hà Nội" not in real_estate_location:
                        continue

                    match = re.search(r'\d+(\.\d+)?', real_estate_total_price)
                    real_estate_total_price = float(match.group()) if match else None

                    real_estate.append(
                        (real_estate_name, real_estate_size, real_estate_location, real_estate_price_per_m_square, real_estate_total_price)
                    )
                except AttributeError:
                    continue

            #Log
            safe_log(f"Thread {thread_id} - Page {i}: Scraped {len(real_estate)} items so far.")

            #pagination
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "(//a[@class='re__pagination-icon'])[1]"))
                )
                try:
                    next_button.click()
                except Exception:
                    driver.execute_script("arguments[0].click();", next_button)
                safe_log(f"Thread {thread_id} - Navigated to page {i + 1}")
            except Exception as e:
                safe_log(f"Thread {thread_id} - Pagination failed on page {i}. Error: {e}")
                break

            time.sleep(1)
    finally:
        driver.quit()

    return real_estate

def main():
    total_pages = 1496
    threads = 5
    pages_per_thread = total_pages // threads

    #thread pool
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for thread_id in range(threads):
            start_page = thread_id * pages_per_thread + 1
            end_page = (thread_id + 1) * pages_per_thread
            futures.append(executor.submit(scrape_pages, start_page, end_page, thread_id + 1))
        
        all_data = []
        for future in futures:
            all_data.extend(future.result())
    
    df = pd.DataFrame(all_data, columns=['Real estate info', 'Real Estate Size(M^2)', 'Real estate location', 'Price per M^2(mill)', 'Total Price(bill)'])
    print(df)
    df.to_excel('real_estate_multithreaded.xlsx', index=False)
    safe_log("Scraping complete. Data saved to 'real_estate_multithreaded.xlsx'.")

if __name__ == "__main__":
    main()
