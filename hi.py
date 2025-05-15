from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScXpB4E8oo1ihME_LQSfmrrVAp3URo4U_VExR5veb-ROJei6w/viewform"

def setup_browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

def extract_fields():
    driver = setup_browser()
    driver.get(FORM_URL)
    
    # Wait until questions load
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[role="listitem"]'))
    )

    questions = driver.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]')

    field_map = {}

    for question in questions:
        try:
            # Extract question label - sometimes inside a span with role heading
            label = question.find_element(By.CSS_SELECTOR, 'div[role="heading"], div[aria-level]').text.strip()
        except:
            label = "Unknown Question"

        # Extract all input fields in this question (there can be multiple for checkboxes)
        inputs = question.find_elements(By.CSS_SELECTOR, 'input[name^="entry"]')
        for input_elem in inputs:
            name_attr = input_elem.get_attribute('name')
            # Save label and input name (id)
            field_map[label] = name_attr

    driver.quit()

    print("\n=== Extracted Field Map ===")
    for k,v in field_map.items():
        print(f"'{k}': '{v}'")

    return field_map

if __name__ == "__main__":
    extract_fields()
