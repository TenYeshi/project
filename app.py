import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# === CONFIG ===
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScXpB4E8oo1ihME_LQSfmrrVAp3URo4U_VExR5veb-ROJei6w/viewform"

def setup_browser():
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(options=options)

def extract_field_ids(browser):
    browser.get(FORM_URL)
    time.sleep(2)  # Wait for the page to load

    soup = BeautifulSoup(browser.page_source, "html.parser")
    fields = []

    # Extract input fields
    for input_tag in soup.find_all("input"):
        name = input_tag.get("name")
        if name and name.startswith("entry."):
            question_div = input_tag.find_parent("div", attrs={"role": "listitem"})
            label = question_div.find("div", class_="M7eMe") if question_div else None
            question_text = label.get_text(strip=True) if label else "Unknown Question"
            fields.append((question_text, name))

    # Extract textarea fields
    for textarea_tag in soup.find_all("textarea"):
        name = textarea_tag.get("name")
        if name and name.startswith("entry."):
            question_div = textarea_tag.find_parent("div", attrs={"role": "listitem"})
            label = question_div.find("div", class_="M7eMe") if question_div else None
            question_text = label.get_text(strip=True) if label else "Unknown Question"
            fields.append((question_text, name))

    return fields

def main():
    browser = setup_browser()
    try:
        field_ids = extract_field_ids(browser)
        print("Field Mappings:")
        for idx, (question, field_id) in enumerate(field_ids, start=1):
            print(f"Q{idx}: '{question}' → {field_id}")
    finally:
        browser.quit()

if __name__ == "__main__":
    main()
