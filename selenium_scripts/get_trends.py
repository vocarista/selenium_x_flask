from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
import uuid
import os
from dotenv import load_dotenv
from db.save_to_mongo import add_trends

load_dotenv()

X_USERNAME = os.getenv('X_USERNAME')
X_PASSWORD = os.getenv('X_PASSWORD')
PROXYMESH_URL = os.getenv('PROXYMESH_URL')

def get_trending_topics():
    options = Options()
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--disable-gpu')
    options.add_argument(f'--proxy-server={PROXYMESH_URL}')

    driver = webdriver.Chrome(options=options)

    try:
        driver.get('https://x.com/login')
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'text')))

        username = driver.find_element(By.NAME, 'text')
        username.send_keys(X_USERNAME)
        username.send_keys(Keys.RETURN)
        time.sleep(3)

        password = driver.find_element(By.NAME, 'password')
        password.send_keys(X_PASSWORD)
        password.send_keys(Keys.RETURN)
        time.sleep(3)

        driver.get('https://x.com/explore/tabs/trending')
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[aria-label="Timeline: Explore"] div span')))

        trends = driver.find_elements(By.CSS_SELECTOR, 'span[dir="ltr"]')
        top_trends = [trend.text for trend in trends[:5]]

        _id = str(uuid.uuid4())
        ip_address = driver.execute_script("return window.location.host")

        data = {
            "_id": _id,
            "nameOfTrend1": top_trends[0] if len(top_trends) > 0 else None,
            "nameOfTrend2": top_trends[1] if len(top_trends) > 1 else None,
            "nameOfTrend3": top_trends[2] if len(top_trends) > 2 else None,
            "nameOfTrend4": top_trends[3] if len(top_trends) > 3 else None,
            "nameOfTrend5": top_trends[4] if len(top_trends) > 4 else None,
            "ip_address": ip_address,
            "run_at": time.time()
        }

        add_trends(data)

        return data
    finally:
        driver.quit()
