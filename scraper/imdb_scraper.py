import time
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import calendar

def get_driver():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.set_page_load_timeout(120)
    return driver

def scrape_month(year, month):
    driver = get_driver()
    wait = WebDriverWait(driver, 20)

    # compute start and end date for the month
    start_date = f"{year}-{month:02d}-01"
    end_day = calendar.monthrange(year, month)[1]
    end_date = f"{year}-{month:02d}-{end_day}"

    url = f"https://www.imdb.com/search/title/?title_type=feature&release_date={start_date},{end_date}"
    driver.get(url)

    names, plots = [], []

    while True:
        movies = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")
        for m in movies[len(names):]:
            try:
                name = m.find_element(By.CSS_SELECTOR,"h3.ipc-title__text").text
            except:
                name = ""
            try:
                plot = m.find_element(By.CSS_SELECTOR,".title-description-plot-container .ipc-html-content-inner-div").text
            except:
                try:
                    plot = m.find_element(By.CSS_SELECTOR,'[data-testid="plot"]').text
                except:
                    plot = ""
            names.append(name)
            plots.append(plot)

        try:
            load_more = wait.until(
                EC.element_to_be_clickable((By.XPATH,"//button//span[contains(text(),'50 more')]"))
            )
            driver.execute_script("arguments[0].click();", load_more)
            time.sleep(2)
        except TimeoutException:
            break
        except:
            break

    driver.quit()

    df = pd.DataFrame({"Movie_Name": names, "Storyline": plots})
    os.makedirs("data", exist_ok=True)
    df.to_csv(f"data/imdb_{year}_{month:02d}.csv", index=False)
    print(f"Scraping completed for {year}-{month:02d}: {len(names)} movies")

if __name__ == "__main__":
    for m in range(1, 13):
        scrape_month(2024, m)
