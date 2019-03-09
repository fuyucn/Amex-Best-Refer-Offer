import time
import string
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def loadConfig(filename):
    res = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            res.append(row)
    return res


def loadLink(filename):
    lines = []
    text_file = open(filename, "r")
    lines = text_file.read().split(',')
    return lines[0]

def loadTargets(filename):
    lines = []
    tragets = []

    text_file = open(filename, "r")
    lines = text_file.readlines()
    for line in lines:
        target = line.split(",")
        tragets.append({"card": target[0], "target":target[1].replace('\n','').replace(" ", "")})
    return tragets

def getDriver(browser):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--window-size=1440,900")
    chrome_options.add_experimental_option("detach", True)
    if browser.lower() == 'firefox':
        driver = webdriver.Firefox()
    elif browser.lower() == 'chrome':
        driver = webdriver.Chrome(
            './webdriver/chromedriver', chrome_options=chrome_options)
    elif browser.lower() == 'chrome_linux':
        driver = webdriver.Chrome(
            './webdriver/chromedriver_linux64', chrome_options=chrome_options)
    elif browser.lower() in ('phantomjs', 'headless'):
        driver = webdriver.PhantomJS()
    else:
        print("WARNING: browser selection not valid, use PhantomJS as default")
        driver = webdriver.PhantomJS()
    return driver


def waitForReferLinkPop(driver):
    wait = WebDriverWait(driver, 120)
    try:
        welcomeBtn = wait.until(
            EC.presence_of_element_located((By.ID, "welcomeBtn")))

        welcomeBtn.click()

    except NoSuchElementException:
        print('Cannot load welcome button')


def openAllReferList(driver):
    referListText = "View all Cards with a Referral Offer"
    referListBtn = driver.find_elements_by_xpath(
        "//a[contains(text(), '"+referListText+"')]")

    if isinstance(referListBtn, list):
        referListBtn = referListBtn[0]

    referListBtn.click()
    time.sleep(2)
    allPersonalCards = "All Personal Cards"

    # allPersonalCardsBtn = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), '" + allPersonalCards + "')]")))
    WebDriverWait(driver, 120).until(EC.element_to_be_clickable(
        (By.XPATH, "//a/span[contains(text(), '" + allPersonalCards + "')]"))).click()
    # allPersonalCardsBtn = driver.find_elements_by_xpath("//a[contains(text(), '" + allPersonalCards + "')]")


def findCardAndVerifyOffer(driver):
    retOffer = []

    cardsList_section = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, "//section[contains(@class, 'row')]")))

    cardsList = cardsList_section.find_elements_by_xpath(
        "//div[@ng-repeat='product in products']")

    # for cardE in cardsList:

    cardE = cardsList[0]
    h3_element_list = cardE.find_elements_by_xpath('//h3')

    name = ""
    bonus = ""

    for h3 in h3_element_list:
        if "Card" in h3.text:
            name = h3.text
        elif "Earn" in h3.text or "Bouns" in h3.text or "bonus miles" in h3.text or "Bonus Miles" in h3.text:
            tmpbonus = h3.text.replace("\n", "")
            bonus = tmpbonus
            # h3_element_list = cardsList[0].find_elements_by_xpath('//h3')
            # for h3 in h3_element_list:
            #     if "Card" in h3.text:
            #         print(h3.text)
            #     elif "Earn" in h3.text:
            #         print(h3.text)
        if (len(name) != 0 and len(bonus) != 0):
            retOffer.append({"name": name, "bonus": bonus})
            name = ""
            bonus = ""

    return retOffer


def checkTargetOffer(offerList, targetCard, targetbonue):
    for offer in offerList:
        # print(offer.get("name") + ": " + offer.get("bonus"))
        if targetCard in offer.get('name'):
            currentOffer = get_num(offer.get('bonus'))
            # print(currentOffer)
            if currentOffer == targetbonue:
                return True
            else:
                return False


def get_num(x):
    return int(''.join(ele for ele in x if ele.isdigit()))
