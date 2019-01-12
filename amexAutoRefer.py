#!/usr/bin/env python
import sys
import time
from selenium import webdriver
from datetime import datetime
from helper import loadConfig, loadLink, getDriver, waitForReferLinkPop, openAllReferList, findCardAndVerifyOffer, checkTargetOffer
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def referOfferProcess(link, card, best_offer, driver):
    try:
        # step 2: open refer link
        driver.get(link)
        time.sleep(2)

        # step 3: wait for 'refer' window, close it
        waitForReferLinkPop(driver)

        # step 4: open refer list
        openAllReferList(driver)

        # step 5: find card by name and verify offer
        time.sleep(2)

        allReferOfers = findCardAndVerifyOffer(driver)
        return checkTargetOffer(allReferOfers, card, best_offer)

    except Exception as e:
        print(e)
        print("Something is wrong with login\n")


def findBestOffer(link, card, best_offer, browser="Chrome"):

    ret = False

    # Step 1: check correct refer link
    if (len(link) > 0):
        driver = getDriver(browser)
        driver.execute_script("window.open('www.google.com');")
        time.sleep(1)
        google_window = driver.current_window_handle  # Define main window
        while(ret == False):
            driver.execute_script("window.open('');")
            # Define Bing window
            new_window = [
                window for window in driver.window_handles if window != google_window][0]
            driver.switch_to.window(new_window)

            time.sleep(1)
            if (ret):
                print("DONE")
            else:
                ret = referOfferProcess(link, card, best_offer, driver)
                if not ret:
                    driver.execute_script("window.close();")
                    time.sleep(1)
                    driver.switch_to.window(google_window)


def main(argv):
    browser = argv[0] if len(argv) >= 1 else 'Chrome'
    card = argv[1] if len(argv) >= 2 else ''
    best_offer = argv[1] if len(argv) >= 2 else ''

    card = "Green Card"
    best_offer = 25000

    findBestOffer(loadLink("./config/referlink.txt"),
                  card, best_offer, browser)


if __name__ == '__main__':
    main(sys.argv[1:])
