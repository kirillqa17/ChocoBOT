from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import pandas as pd
import json
import time
import warnings
warnings.filterwarnings("ignore", category=ResourceWarning)


accounts = pd.read_csv("accounts.csv")

for index, row in accounts.iterrows():
    login = row['email']
    password = row['password']

    print(f"Вход для аккаунта {index + 1}: {login}")

    driver = None
    try:
        driver = uc.Chrome()
        driver.get("https://deliveroo.ae/login")
        wait = WebDriverWait(driver, 10)

        login_button = wait.until(EC.visibility_of_element_located((By.ID, "continue-with-email")))
        time.sleep(3)
        login_button.click()

        email_field = wait.until(EC.visibility_of_element_located((By.ID, "email-address")))
        email_field.send_keys(login)

        continue_button = wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="__next"]/div/div/div[2]/div/form/div[3]/span[1]/button')))
        continue_button.click()

        password_field = wait.until(EC.visibility_of_element_located((By.ID, "login-password")))
        password_field.send_keys(password)

        driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div/form/div[3]/span[1]/button').click()

        wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="__next"]/div/div/div[2]/div/form/span/button'))).click()

        while driver.current_url != "https://deliveroo.ae/":
            time.sleep(1)

        cookies = driver.get_cookies()
        with open(f"cookies/cookies_{index + 1}.json", "w") as file:
            json.dump(cookies, file)
            print(f"Куки сохранены для аккаунта {index + 1}: {login}")

    except Exception as e:
        print(f"Произошла ошибка для аккаунта {index + 1} ({login}):", e)

    finally:
        if driver:
            try:
                driver.quit()
            except OSError as os_error:
                print(f"Ошибка при завершении драйвера для аккаунта {index + 1} ({login}):", os_error)
            del driver
print("Авторизация завершена")
