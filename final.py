import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# Your Google Form URL
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScXpB4E8oo1ihME_LQSfmrrVAp3URo4U_VExR5veb-ROJei6w/viewform"

# Map your CSV headers or question labels to Google Form entry IDs (from your field_map)
field_map = {
    'Name': 'entry.2005620554',
    'Gender': 'entry.1922184502',
    'Age': 'entry.475496531',
    'Occupation': 'entry.614116491',
    'Car': 'entry.654082115',  # Replaces 'Model'
    'Monthly Income': 'entry.934253406',  # Replaces 'Income'
}
MULTIPLE_CHOICE_IDS = {
    "Q1": "entry.800023522",
    "Q2": "entry.479244205",
    "Q3": "entry.1423715575",
    "Q4": "entry.486908427",
    "Q5": "entry.342189178",
    "Q6": "entry.778899407",
    "Q7": "entry.144666218",
    "Q8": "entry.511549133",
    "Q9": "entry.1993757498",
    "Q10": "entry.1346967080",
    "Q11": "entry.616557489",
    "Q12": "entry.2005327552",
    "Q13": "entry.1120841825",
    "Q14": "entry.107339832",
    "Q15": "entry.363316929",
    "Q16": "entry.2101011618",
    "Q17": "entry.1548649962",
    "Q18": "entry.323570890",
    "Q19": "entry.88165610",
    "Q20": "entry.1236696860",
    "Q21": "entry.375858376",
    "Q22": "entry.1511332658",
    "Q23": "entry.1340819478",
    "Q24": "entry.930847742",
    "Q25": "entry.1486572076",
    "Q26": "entry.1818931857",
    "Q27": "entry.1420703750",
    "Q28": "entry.1401045893",
    "Q29": "entry.1235659964",
    "Q30": "entry.1506316557",
    "Q31": "entry.1625781146",
    "Q32": "entry.766884759",
    "Q33": "entry.1848766939",
    "Q34": "entry.1190028059",
    "Q35": "entry.1765749255",
    "Q36": "entry.1245369091",
    "Q37": "entry.362285798",
    "Q38": "entry.947176119",
    "Q39": "entry.1197374496",
    "Q40": "entry.75257028",
    "Q41": "entry.780270194",
    "Q42": "entry.1415945896",
    "Q43": "entry.1299842447",
    "Q44": "entry.2006623036",
    "Q45": "entry.817758609",
    "Q46": "entry.725764542",
    "Q47": "entry.778497562",
    "Q48": "entry.1987804027",
    "Q49": "entry.827798796",
    "Q50": "entry.1501835797"
}




def setup_browser():
    options = Options()
    options.debugger_address = "127.0.0.1:9222"  # match your Chrome debug port
    return webdriver.Chrome(options=options)

def fill_text_field(driver, value):
    try:
        # Try input field
        input_elem = driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
        input_elem.clear()
        input_elem.send_keys(value)
    except:
        try:
            # Fallback to textarea
            textarea_elem = driver.find_element(By.CSS_SELECTOR, 'textarea')
            textarea_elem.clear()
            textarea_elem.send_keys(value)
        except Exception as e:
            print(f"Error in fill_text_field: {e}")


def fill_textarea(driver, entry_id, value):
    try:
        elem = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, f'input[name="{entry_id}"]'))
        )
        elem.clear()
        driver.execute_script("arguments[0].scrollIntoView(true);", elem)
        elem.send_keys(value)
    except Exception as e:
        print(f"Error filling textarea {entry_id}: {e}")
def fill_radio(driver, entry_id, value):  # ✅ This is correct

    try:
        radios = driver.find_elements(By.CSS_SELECTOR, 'div[role="radio"]')
        for r in radios:
            if r.get_attribute("aria-label").strip().lower() == value.strip().lower():
                r.click()
                return
        print(f"Radio option '{value}' not found.")
    except Exception as e:
        print(f"Error filling radio: {e}")


def fill_radio(driver, entry_id, value):
    try:
        # Google Forms radios have inputs with value labels, so find label matching the value
        options = driver.find_elements(By.CSS_SELECTOR, f'div[role="radiogroup"][data-params="{entry_id}"] div[role="radio"]')
        for option in options:
            aria_label = option.get_attribute('aria-label')
            if aria_label and value.strip().lower() == aria_label.strip().lower():
                option.click()
                return
        # If no match found, fallback to input by name and value attribute if possible
        radios = driver.find_elements(By.CSS_SELECTOR, f'input[type="radio"][name="{entry_id}"]')
        for r in radios:
            if r.get_attribute('value').strip().lower() == value.strip().lower():
                r.click()
                return
        print(f"Radio option '{value}' not found for {entry_id}")
    except Exception as e:
        print(f"Error filling radio {entry_id}: {e}")

def fill_checkbox(driver, entry_id, values):
    try:
        # For checkboxes, values is a list of strings
        options = driver.find_elements(By.CSS_SELECTOR, f'div[role="checkbox"][data-params="{entry_id}"]')
        for option in options:
            aria_label = option.get_attribute('aria-label')
            if aria_label and aria_label.strip().lower() in [v.strip().lower() for v in values]:
                option.click()
    except Exception as e:
        print(f"Error filling checkboxes {entry_id}: {e}")

def submit_response(driver):
    try:
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[role="button"][aria-label="Submit"]'))
        )
        submit_button.click()
    except Exception as e:
        print(f"Error clicking submit button: {e}")

def reload_form(driver):
    try:
        driver.get(FORM_URL)     # Reload the form URL
        time.sleep(3)            # Wait a bit for page to load
    except Exception as e:
        print(f"Error reloading form: {e}")

def main():
    driver = setup_browser()
    driver.get(FORM_URL)

    with open('/Users/apple/Desktop/internship/tata_motor_survey_10_persons.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            time.sleep(2)

            all_values = list(row.values()) # Maintain input order

            form_items = driver.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]') # Google Form question containers

            for index, value in enumerate(all_values):
                value = value.strip()
                if not value:
                    continue
                try:
                    item = form_items[index]
                    driver.execute_script("arguments[0].scrollIntoView(true);", item)

                    # Check for radio buttons
                    radio_buttons = item.find_elements(By.CSS_SELECTOR, 'div[role="radio"]')
                    if radio_buttons:
                        for rb in radio_buttons:
                            if rb.get_attribute("aria-label").strip().lower() == value.lower():
                                rb.click()
                                break
                        continue
                    # Check for checkboxes
                    checkboxes = item.find_elements(By.CSS_SELECTOR, 'div[role="checkbox"]')
                    if checkboxes:
                        for cb in checkboxes:
                            if cb.get_attribute("aria-label").strip().lower() == value.lower():
                                cb.click()
                                break
                        continue
                        # Check for input box
                    try:
                        input_box = item.find_element(By.CSS_SELECTOR, 'input[type="text"]')
                        input_box.clear()
                        input_box.send_keys(value)
                        continue
                    except:
                        pass

                    # Check for textarea
                    try:
                        textarea_box = item.find_element(By.CSS_SELECTOR, 'textarea')
                        textarea_box.clear()
                        textarea_box.send_keys(value)
                        continue
                    except:
                        pass
                except Exception as e:
                    print(f"Error processing field {index}: {e}")

                except Exception as e:
                    print(f"Error processing field {index}: {e}")
            submit_response(driver)
            time.sleep(1)

            reload_form(driver)  # <-- Reload form fresh for next response
            time.sleep(1)

    print("All responses submitted.")
    driver.quit()
    # Close the browser
    # driver.quit()
if __name__ == "__main__":
    main()
