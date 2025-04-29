import re
import undetected_chromedriver as uc
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from seleniumwire import webdriver

choose_random_box = "button.index_chooseRandomlyBtn__upKXA"
notification_message = "div.ant-notification-notice-message"

print("Welcome to the BuBuBot version 0.1\n \nFollow the input prompts below, if you need help refer to README.md\n")
default_set_price = "$167.94"
box_mode = input('Enable Box Shaking Only Mode? (Yes/No) ')
if box_mode.lower() == 'yes':
    box_mode = True
else:
    box_mode = False
    total_price_default = input('Custom Set Price? (Yes/No) ')
    if total_price_default.lower() == 'yes':
        default_set_price = "$" + input("Enter Set Price:")
        print(f"\n Using default price of: {default_set_price}")
    else:
        print(f"\n Using default price of: {default_set_price}")
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
                EC.element_to_be_clickable((By.CSS_SELECTOR, choose_random_box))
            )
            shake_bubu.click()
            add_to_bag = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.index_btn__77cLz"))
            )
            add_to_bag.click()
            success_message = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, notification_message))
            )
            if success_message:
                time.sleep(5)
                break

        except TimeoutException:
            increment_url()
            time.sleep(5)


def multiple_boxes():
    while True:
        buy_multiple = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.index_chooseMulitityBtn__n0MoA"))
        )
        print("Button found. Clicking it.")
        buy_multiple.click()

        time.sleep(2)

        checkbox_label = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "label.index_selectAll__W_Obs"))
        )
        checkbox_label.click()

        price_element = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.index_priceText__o0wU6"))
        )
        price_text = price_element.text
        print(f"Found price: {price_text}")

        if default_set_price in price_text:
            print("Price matched! Proceeding to add to cart...")
            add_to_cart = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ant-btn-primary.index_btn__Y5dKo"))
            )
            add_to_cart.click()

            try:
                success_message = WebDriverWait(driver, 10).until(
                    EC.text_to_be_present_in_element(
                        (By.CSS_SELECTOR, notification_message),
                        "Add to bag successfully"
                    )
                )
                if success_message:
                    print("Successfully added to bag!")
                    break
            except Exception as e:
                print("Add to bag failed. Retrying after URL increment:", e)

        else:
            print("Price did not match.")

        print("Incrementing URL and retrying...")
        increment_url()
        time.sleep(1)


options = uc.ChromeOptions()
options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument(f"--profile-directory={profile_directory}")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--new-window")

undetected_driver = uc.Chrome(options=options, use_subprocess=True)

driver = webdriver.Chrome(
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
        multiple_boxes()
    else:
        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, choose_random_box))
        )
        shake_single_bubu()

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()
