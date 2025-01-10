import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import uuid
import os
from dotenv import load_dotenv
from db.save_to_mongo import add_trends
from datetime import datetime

load_dotenv()

X_USERNAME = os.getenv('X_USERNAME')
X_PASSWORD = os.getenv('X_PASSWORD')
X_EMAIL = os.getenv('X_EMAIL')
PROXYMESH_URL = os.getenv('PROXYMESH_URL')

def get_trending_topics():
    options = Options()
    # options.add_argument('--headless')  
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # if PROXYMESH_URL:
    #     options.add_argument(f'--proxy-server={PROXYMESH_URL}')

    driver = webdriver.Chrome(options=options)

    try:
        
        driver.get('https://x.com/login')
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'text')))
        time.sleep(random.uniform(2, 5))  

        username = driver.find_element(By.NAME, 'text')
        username.send_keys(X_USERNAME)
        username.send_keys(Keys.RETURN)
        time.sleep(random.uniform(3, 6))
        
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, 'password')))
        password = driver.find_element(By.NAME, 'password')
        password.send_keys(X_PASSWORD)
        password.send_keys(Keys.RETURN)
        time.sleep(random.uniform(4, 8)) 

        try:
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.NAME, 'email')))
            email = driver.find_element(By.NAME, 'email')
            email.send_keys(X_EMAIL)
            email.send_keys(Keys.RETURN)
            time.sleep(random.uniform(4, 8))
            print("Email step completed.")
        except Exception:
            print("Email step not required.")


        driver.get('https://x.com/explore/tabs/trending')
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span[dir="ltr"]')))
        time.sleep(random.uniform(2, 5))  

        trends = driver.find_elements(By.CSS_SELECTOR, 'span[dir="ltr"]')
        top_trends = [trend.text for trend in trends[:5]]

        driver.get('https://whatismyipaddress.com')
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ipv4')))
        time.sleep(random.uniform(2, 5))
        ip_address = driver.find_element(By.CSS_SELECTOR, '#ipv4').text

        _id = str(uuid.uuid4())
        data = {
            "_id": _id,
            "nameOfTrend1": top_trends[0] if len(top_trends) > 0 else None,
            "nameOfTrend2": top_trends[1] if len(top_trends) > 1 else None,
            "nameOfTrend3": top_trends[2] if len(top_trends) > 2 else None,
            "nameOfTrend4": top_trends[3] if len(top_trends) > 3 else None,
            "nameOfTrend5": top_trends[4] if len(top_trends) > 4 else None,
            "ip_address": ip_address,
            "run_at": datetime.now()
        }

        add_trends(data)
        return data

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    finally:
        driver.quit()
