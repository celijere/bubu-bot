import re
import undetected_chromedriver as uc
import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from seleniumwire import webdriver

print("Welcome to the BuBuBot version 0.1\n \nFollow the input prompts below, if you need help refer to README.md\n")

box_mode = input('Enable Box Shaking Only Mode? (Yes/No) ')
if box_mode.lower() == 'yes':
    box_mode = True
else:
    box_mode = False
user_data_dir = input('Base Path:')
profile_directory = input("Chrome Profile Directory:")
desired_URL = input("PopMart URL:")


def increment_url():
    print("Button not found, incrementing URL and trying again...")

    current_url = driver.current_url

    match = re.search(r'(\d{5})(\d{5})$', current_url)
    if match:
        part_to_increment = match.group(1)

        incremented_part = str(int(part_to_increment) + 5).zfill(5)
        new_url = re.sub(r'\d{5}(\d{5})$', f'{incremented_part}\\1', current_url)

        print(f"Navigating to new URL: {new_url}")
        driver.get(new_url)

    else:
        print("URL format invalid, cannot increment.")


def shake_single_bubu():
    while True:
        try:
            shake_bubu = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.index_chooseRandomlyBtn__upKXA"))
            )
            shake_bubu.click()
            add_to_bag = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.index_btn__77cLz"))
            )
            add_to_bag.click()
            success_message = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.ant-notification-notice-message"))
            )
            if success_message:
                time.sleep(5)
                break

        except TimeoutException:
            increment_url()
            time.sleep(5)


seleniumwire_options = {
}

options = uc.ChromeOptions()
options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument(f"--profile-directory={profile_directory}")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--new-window")

# driver = uc.Chrome(options=options)

undetected_driver = uc.Chrome(options=options, use_subprocess=True)

driver = webdriver.Chrome(
    seleniumwire_options=seleniumwire_options,
    options=options,
)

driver.session_id = undetected_driver.session_id
driver.command_executor = undetected_driver.command_executor
print("Page loaded, looking for button...")

try:
    driver.get(desired_URL)

    wait = WebDriverWait(driver, 10)

    wait.until(EC.presence_of_element_located((By.ID, "topBoxContainer")))

    if not box_mode:
        buy_multiple = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.index_chooseMulitityBtn__n0MoA"))
        )

        print("Button found. Clicking it.")
        buy_multiple.click()

        # checkbox_label = wait.until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, "label.index_selectAll__W_Obs"))
        # )

        print(len(driver.requests))
        for request in driver.requests:
            print("test.")
            if request.response and "/preview" in request.url:
                print(f"Request URL: {request.url}")
                print(f"Status code: {request.response.status_code}")

                if 'application/json' in request.response.headers.get('Content-Type', ''):
                    body = request.response.body.decode('utf-8')
                    data = json.loads(body)

                    box_list = data.get('data', {}).get('box_list', [])

                    if all(box['box_info']['state'] == 0 for box in box_list):
                        checkbox_label = wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "label.index_selectAll__W_Obs"))
                        )
                        checkbox_label.click()
                        print("Checkbox clicked, full set found.")
                        time.sleep(10)
                        waitFourth = WebDriverWait(driver, 10)
                        button = waitFourth.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ant-btn-primary.index_btn__Y5dKo"))
                        )
                        button.click()
                    else:
                        print("A full set wasn't found")

    else:
        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.index_chooseRandomlyBtn__upKXA"))
        )
        shake_single_bubu()

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()
