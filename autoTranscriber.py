import json
import numpy as np
import pytesseract
import selenium
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from PIL import Image, ImageEnhance, ImageFilter
from numpy import array
import cv2
import uuid
from pywebio import start_server
from pywebio.input import input, NUMBER
from pywebio.input import TEXT
from pywebio.input import input, PASSWORD
from pywebio.session import set_env
from pywebio.output import put_image 
from pywebio.platform.flask import webio_view
from enum import Enum
from flask import Flask

#Library of Congress Auto-Transcriber by Boris Brondz

app = Flask(__name__)

@app.route('/')

#JSON serializable enum with all required paths and class names for the web driver to find elements on the page.
class webSettings(str, Enum):
    #Include all xpaths from autoTranscriber.py here
    #Example:
    #loginButton = driver.find_element(By.XPATH, '//*[@id="body"]/header/nav/ul/li[1]/a')

    #Include all xpaths from autoTranscriber.py here
    LOGIN_BUTTON_PATH = '//*[@id="body"]/header/nav/ul/li[1]/a'
    USERNAME_PATH = '//*[@id="id_username"]'
    PASSWORD_PATH = '//*[@id="id_password"]'
    LOGIN_SUBMIT_PATH = '//*[@id="body"]/main/div[2]/div[1]/div/form/div[3]/button'
    CAMPAIGN_LIST = '//*[@id="nav-menu"]/ul/li[2]/a'
    NOT_STARTED_BUTTON = '//*[@id="body"]/main/div[2]/div[7]/div/div/a[5]'
    NEW_COLLECTIONS = '//*[@id="body"]/main/div[2]/div[8]'
    FULL_SCREEN_BUTTON = '//*[@id="viewer-fullscreen"]/span'
    TRANSCRIPTION_BOX = '//*[@id="transcription-input"]'
    SAVE_BUTTON = '//*[@id="save-transcription-button"]'
    SUBMIT_BUTTON = '//*[@id="submit-transcription-button"]'
    NEXT_PAGE_BUTTON = '//*[@id="successful-submission-modal"]/div/div/div[3]/p[2]/a'

    #Class names. These will be found by "class name" instead of their xpaths.
    TRANSCRIPTION_TAGS = 'card-img-container'
    PAGE_ITEM = 'page-item'

    #Tag names. These will be found by "tag name" instead of their xpaths.
    HEADER_TAG = 'h6'
    
#Library of Congress Autoscriber by Boris Brondz

class AutoTranscriber:

    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'

    numCycles = 100
    msDelay = 700

    set_env(title= "LOC Auto-Transcriber")

    def getNumCycles(self):
        return self.numCycles

    def checkValidCycles(numCycles):
        if(numCycles < 1):
            raise Exception("Number of cycles must be greater than 0.")

    def checkValidDelay(msDelay):
        if(msDelay < 500):
            raise Exception("Delay must be greater than 500 milliseconds to ensure all webpage content can be loaded in time.")

    #Input user credentials and amount of cycles.

    name = input("Enter your LOC username", type=TEXT)
    password = input("Enter your LOC password", type=PASSWORD)
    numCycles = input("Enter the number of transcription cycles", type=NUMBER, validate= checkValidCycles)
    msDelay = input("Enter the delay between each cycle (in milliseconds)", type=NUMBER, validate= checkValidDelay)

    driver = webdriver.Chrome()
    options = webdriver.ChromeOptions()
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches",["enable-automation"])
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    driver.get('https://crowd.loc.gov/')
    driver.fullscreen_window()
    driver.implicitly_wait(msDelay)
    loginButton = driver.find_element(By.XPATH, webSettings.LOGIN_BUTTON_PATH)
    loginButton.click()
    driver.implicitly_wait(msDelay)
    userNameField = driver.find_element(By.XPATH, webSettings.USERNAME_PATH)
    pwField = driver.find_element(By.XPATH, webSettings.PASSWORD_PATH)

    userNameField.send_keys(name)
    pwField.send_keys(password)
    driver.implicitly_wait(msDelay)
    driver.find_element(By.XPATH, webSettings.LOGIN_SUBMIT_PATH).click()
    driver.implicitly_wait(msDelay)

    #Bypass CAPTCHA (not needed currently)
    campaign = driver.find_element(By.XPATH, webSettings.CAMPAIGN_LIST)
    campaign.click()
    driver.implicitly_wait(msDelay)

    #A list of campaigns is always available under the 'campaigns' section. Query all of them and let the script pick a random one.
    campaignList = ['//*[@id="campaign-list"]/li[1]/div/div/a', '//*[@id="campaign-list"]/li[2]/div/div/a', '//*[@id="campaign-list"]/li[3]/div/div/a',
     '//*[@id="campaign-list"]/li[4]/div/div/a','//*[@id="campaign-list"]/li[5]/div/div/a', '//*[@id="campaign-list"]/li[6]/div/div/a', '//*[@id="campaign-list"]/li[7]/div/div/a',
      '//*[@id="campaign-list"]/li[8]/div/div/a', '//*[@id="campaign-list"]/li[9]/div/div/a', '//*[@id="campaign-list"]/li[10]/div/div/a']

    randomCampaignNum = random.randint(0, len(campaignList) - 1)
    driver.find_element(By.XPATH, campaignList[randomCampaignNum]).click()
    driver.implicitly_wait(msDelay)

    #Automatically go to the "Not started" category to ensure we will only be doing transcriptions. 

    driver.find_element(By.XPATH, webSettings.NOT_STARTED_BUTTON).click()
    driver.implicitly_wait(msDelay)
    #There are an indeterminate amount of available "Collections" of documents to transcribe for each available category.

    valueList = []
    newPages = driver.find_elements(By.XPATH, webSettings.NEW_COLLECTIONS)
    driver.implicitly_wait(msDelay)
    newValues = driver.find_elements(By.TAG_NAME, 'h6')
    if(len(newValues) < 1):
        driver.implicitly_wait(msDelay)
        driver.back()
    randomVal = random.randint(0, len(newValues) - 1)
    for i in range(len(newValues)):
        #if i is the random value, then make webdriver click on it.
        if(i == randomVal):
            newValues[i].click()
    if(not newValues):
        raise Exception("No incomplete archives found.")
    else:
        #valueList[randomVal].click()
        driver.implicitly_wait(msDelay)  

        page_buttons = []
        newButtons = driver.find_elements(By.CLASS_NAME, webSettings.PAGE_ITEM)
        if(not newButtons):
                print("No page buttons found.")
        else:
                randomPage = random.randint(0, len(newButtons) - 1)
                for i in range(len(newButtons)):
                    page_buttons.append(newButtons[i])
                    if(i == randomPage):
                        newButtons[i].click()
                        driver.implicitly_wait(msDelay)
                        print("Page clicked")
    
#Pick a random page to transcribe. This time, we will need to pick a random page from the list of pages that are available for transcription.
   
    def transcribeLoop(self, numCycles):
        stringTexts = []
        for i in range(numCycles):
            WebDriverWait(self.driver, timeout=500).until(EC.element_to_be_clickable((By.XPATH, webSettings.FULL_SCREEN_BUTTON)))
            self.driver.find_element(By.XPATH, webSettings.FULL_SCREEN_BUTTON).click()

            self.driver.implicitly_wait(self.msDelay)
            self.driver.save_screenshot('num' + str(i) + '.png')
            put_image('num' + str(i) + '.png')
            self.driver.implicitly_wait(self.msDelay)
            self.driver.find_element(By.XPATH, webSettings.FULL_SCREEN_BUTTON).click()
            self.driver.implicitly_wait(self.msDelay)

            #Use cv2 (OpenCV) and pytesseract to convert captured image to string data.
            img = cv2.imread('num' + str(i) + '.png', 0)
            kernel = np.ones((1,1),np.uint8)
            opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=2)
            data = pytesseract.image_to_string(opening, lang='eng', config='--psm 6')
            img = Image.fromarray(img)
            img = img.filter(ImageFilter.SHARPEN)
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(2)
            img = img.convert('1')
            #img.save('num' + str(i) + '.png')

            #Send string data to text field, save, submit, and look for another document.
            transcribedText = data
            stringTexts.append(transcribedText)

            # Store the transcribed text in DynamoDB
            response = self.table.put_item(
                Item={
                    'id': str(uuid.uuid4()),  # Unique UUID as string
                    'transcription': stringTexts[i]
                }
            )
            print("PutItem succeeded:" + json.dumps(response, indent=4))

            textField = self.driver.find_element(By.XPATH, webSettings.TRANSCRIPTION_BOX)
            textField.send_keys(stringTexts[i])
            self.driver.implicitly_wait(self.msDelay)
            self.driver.find_element(By.XPATH, webSettings.SAVE_BUTTON).click()
            self.driver.implicitly_wait(self.msDelay)
            self.driver.find_element(By.XPATH, webSettings.SUBMIT_BUTTON).click()
            self.driver.implicitly_wait(self.msDelay)
            self.driver.find_element(By.XPATH, webSettings.NEXT_PAGE_BUTTON).click()
    
def start_flask_server():
    app.add(url_rule='/tool', view_func=webio_view(AutoTranscriber), methods=['GET', 'POST', 'OPTIONS'])
    app.run(host='localhost', port=80)

if __name__ == '__main__':
    start_flask_server()

A = AutoTranscriber()
A.transcribeLoop(A.getNumCycles())
