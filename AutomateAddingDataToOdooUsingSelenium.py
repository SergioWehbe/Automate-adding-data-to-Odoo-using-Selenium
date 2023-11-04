from dataclasses import dataclass
from enum import Enum

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# warnings.filterwarnings("ignore")

browser: webdriver.Chrome
pageLoadDelay = 10

def initializeBrowser():
    global browser
    browser = webdriver.Chrome()

def login():
    email = "admin"
    password = "admin"
    browser.get("http://localhost:8069/web/login")

    inputEmail = WebDriverWait(browser, pageLoadDelay).until(EC.presence_of_element_located((By.ID, "login")))
    inputPassword = browser.find_element(By.ID, 'password')
    inputEmail.send_keys(email)
    inputPassword.send_keys(password)
    inputPassword.submit()
    WebDriverWait(browser, pageLoadDelay).until(EC.presence_of_element_located((By.XPATH, '//*[@title="Home Menu"]')))

class PageType(Enum):
    CREATE_VENDOR = 1
    CREATE_PRODUCT = 2

def openPage(pageType: PageType):
    match pageType:
        case PageType.CREATE_VENDOR:
            browser.get("http://localhost:8069/web#cids=1&menu_id=235&action=263&model=res.partner&view_type=form")
        case PageType.CREATE_PRODUCT:
            browser.get("http://localhost:8069/web#cids=1&menu_id=235&action=384&model=product.template&view_type=form")

def getSaveButton():
    return WebDriverWait(browser, pageLoadDelay).until(EC.presence_of_element_located((By.CLASS_NAME, "o_form_button_save")))

def addVendor(name: str):
    createButton = WebDriverWait(browser, pageLoadDelay).until(EC.presence_of_element_located((By.CLASS_NAME, "o_form_button_create")))
    createButton.click()
    inputName = WebDriverWait(browser, pageLoadDelay).until(EC.presence_of_element_located((By.CLASS_NAME, "o-autocomplete--input")))
    inputName.send_keys(name)
    buttonSave = getSaveButton()
    buttonSave.click()

def addVendorList():
    vendorArray = ["Vendor 1", "Vendor 2", "Vendor 3", "Vendor 4", "Vendor 5", "Vendor Last"]
    openPage(PageType.CREATE_VENDOR)
    for vendor in vendorArray:
        addVendor(vendor)

@dataclass
class Product:
    name: str
    isAvailableInPOS: bool
    category: str

def addProduct(product: Product):
    createButton = WebDriverWait(browser, pageLoadDelay).until(EC.presence_of_element_located((By.CLASS_NAME, "o_form_button_create")))
    createButton.click()
    inputName = WebDriverWait(browser, pageLoadDelay).until(EC.presence_of_element_located((By.ID, "name")))
    inputName.send_keys(product.name)
    if product.isAvailableInPOS:
        browser.find_element(By.NAME, "sales").click()
        availableInPos = WebDriverWait(browser, pageLoadDelay).until(EC.presence_of_element_located((By.ID, "available_in_pos")))
        availableInPos.click()
        inputCategory = WebDriverWait(browser, pageLoadDelay).until(EC.presence_of_element_located((By.ID, "pos_categ_id")))
        inputCategory.send_keys(product.category)
        # Wait for Dropdown "Create category" to show
        WebDriverWait(browser, pageLoadDelay).until(EC.presence_of_element_located((By.CLASS_NAME, "o-autocomplete--dropdown-menu")))
        inputCategory.send_keys(Keys.RETURN)
    buttonSave = getSaveButton()
    buttonSave.click()

def addProductList():
    productArray = [Product(name="Sechoir Luv 1", isAvailableInPOS=True, category="Categorios"),
                    Product(name="Sechoir Luv 2", isAvailableInPOS=True, category="Categorios"),
                    Product(name="Sechoir Luv 3", isAvailableInPOS=True, category="Categorios"),
                    Product(name="ProdCat 1", isAvailableInPOS=True, category="Catz"),
                    Product(name="ProdCat 2", isAvailableInPOS=True, category="Catz"),]
    openPage(PageType.CREATE_PRODUCT)
    for product in productArray:
        addProduct(product)

if __name__ == "__main__":
    initializeBrowser()
    login()
    # addVendorList()
    # addProductList()

    print("Press return key to close the browser")
    input()