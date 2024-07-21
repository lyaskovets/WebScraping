from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json


def parse_selenium():
    driver = webdriver.Chrome()

    max_page = 3
    result = []

    for page in range(1, max_page):
        driver.get(f'https://jobs.marksandspencer.com/job-search?page={page}')
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ais-Hits-item')))

        jobs = driver.find_elements(By.CLASS_NAME, 'ais-Hits-item')
        for job in jobs:
            title = job.find_element(By.XPATH, './/h3[@class="text-2xl bold mb-16"]').text
            url = job.find_element(By.XPATH, './/a[contains(@class,"c-btn c-btn--primary")]').get_attribute('href')
            result.append({
                'title': title,
                'url': url
            })

    with open('jobs.json', 'w') as f:
        json.dump(result, f, indent=4)


if __name__ == '__main__':
    parse_selenium()
