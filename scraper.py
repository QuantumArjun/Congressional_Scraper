import pandas as pd
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import argparse
 
def main(search_term):
    BASE_URL = "https://www.congress.gov/search?q=%7B%22source%22%3A%22legislation%22%2C%22search"
    
    #contruct string
    search_term = '"' + search_term + '"'
    search_term = search_term.replace(" ", "%20")
    search_term = search_term.replace('"', '%22')
    search_term = search_term.replace('{', '%7B')
    search_term += '%7D'
    BASE_URL += search_term
    print(BASE_URL)
    options = Options()
    options.add_argument('--headless=new')
    # options.add_argument('--headless')
    options.add_argument("no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, timeout=60, poll_frequency=5)
        wait.until(EC.presence_of_element_located((By.ID, 'main')))
 
        search_container = driver.find_element(By.ID, 'main')
        search_results = search_container.find_elements(By.XPATH, 
        "//li[@class='expanded']//span[@class='result-heading']")
 
        print(f"Number of titles found: {len(search_results)}")
        titles = {'Titles': [search_result.text for search_result in search_results]}
        df = pd.DataFrame.from_dict(titles)
        print(df)
 
    except TimeoutException:
        print("Timed out waiting for data")
    except NoSuchElementException as e:
        print(e.msg)
    finally:
        driver.close()
 
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', type=str,
                        help='Return congressional records containing this term. '
                             'For multi-word search terms, surround them in double quotation marks.')
    args = parser.parse_args()
    main(search_term=args.s)