import numpy as np
from gettext import npgettext
import pytesseract
import selenium
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from PIL import Image, ImageEnhance, ImageFilter, ImageColor
from numpy import array
import cv2
#import maskpass
import getpass
from pywebio.input import input, FLOAT
from pywebio.input import input, NUMBER
from pywebio.input import TEXT
from pywebio.output import put_text
from pywebio.input import input, PASSWORD
from pywebio.input import input_group
from pywebio.session import set_env


class AutoTranscriber:

    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'

    numCycles = 0
    msDelay = 0

    def _init_(self, numCycles, msDelay): 
        self.numCycles = numCycles
        self.msDelay = msDelay

    set_env(title= "Library of Congress AutoTranscriber")

    #credentials = input_group("Enter your credentials",[
        #input("Username", name="username"),
        #input("Password", name="password", type=PASSWORD)
   # ])

    def checkValidCycles(numCycles):
        if(numCycles < 1):
            raise Exception("Number of cycles must be greater than 0.")

    name = input("Enter your username", type=TEXT)
    password = input("Enter your password", type=PASSWORD)
    numCycles = input("Enter the number of cycles", type=NUMBER, validate= checkValidCycles)

    driver = webdriver.Chrome()
    #print(5)
    driver.get('https://crowd.loc.gov/')
    driver.fullscreen_window()
    driver.implicitly_wait(255)
    loginButton = driver.find_element(By.XPATH, '//*[@id="body"]/header/nav/ul/li[1]/a')
    loginButton.click()

    driver.implicitly_wait(455)
    userNameField = driver.find_element(By.XPATH, '//*[@id="id_username"]')
    pwField = driver.find_element(By.XPATH, '//*[@id="id_password"]')

    userNameField.send_keys(name)
    pwField.send_keys(password)
    driver.implicitly_wait(550)
    driver.find_element(By.XPATH, '//*[@id="body"]/main/div[2]/div[1]/div/form/div[3]/button').click()
    driver.implicitly_wait(350)

    #Bypass CAPTCHA (not needed currently)

    campaign = driver.find_element(By.XPATH, '//*[@id="nav-menu"]/ul/li[2]/a')
    campaign.click()

    driver.implicitly_wait(300)

    #A list of 10 campaigns are always available under the 'campaigns' section. Query all of them and let the script pick a random one.

    campaignList = ['//*[@id="campaign-list"]/li[1]/div/div/a', '//*[@id="campaign-list"]/li[2]/div/div/a', '//*[@id="campaign-list"]/li[3]/div/div/a',
     '//*[@id="campaign-list"]/li[4]/div/div/a','//*[@id="campaign-list"]/li[5]/div/div/a', '//*[@id="campaign-list"]/li[6]/div/div/a', '//*[@id="campaign-list"]/li[7]/div/div/a',
      '//*[@id="campaign-list"]/li[8]/div/div/a', '//*[@id="campaign-list"]/li[9]/div/div/a', '//*[@id="campaign-list"]/li[10]/div/div/a']

    randomCampaignNum = random.randint(0, 9)
    driver.find_element(By.XPATH, campaignList[randomCampaignNum]).click()
    driver.implicitly_wait(1500)

    #Automatically go to the "Not started" category to ensure we will only be doing transcriptions. 

    driver.find_element(By.XPATH, '//*[@id="body"]/main/div[2]/div[7]/div/div/a[5]').click()
    driver.implicitly_wait(3800)
    #There are an indeterminate amount of available "Collections" of documents to transcribe for each available category.


    pageList = []
    valueList = []
    newPages = driver.find_elements(By.XPATH, '//*[@id="body"]/main/div[2]/div[8]')
    driver.implicitly_wait(1000)
    newValues = driver.find_elements(By.TAG_NAME, 'h6')
    print(len(newPages))
    print("Boxes amount:" + str(len(newValues)))
    randomVal = random.randint(0, len(newValues) - 1)
    for i in range(len(newValues)):

        #if i is the random value, then make webdriver click on it.
        if(i == randomVal):
            newValues[i].click()

    if(not newValues):
        raise Exception("No incomplete archives found.")
    else:
        #valueList[randomVal].click()
        driver.implicitly_wait(1500)  

        page_buttons = []
        newButtons = driver.find_elements(By.CLASS_NAME, 'page-item')
        if(not newButtons):
                print("No page buttons found.")
        else:
                randomPage = random.randint(0, len(newButtons) - 1)
                for i in range(len(newButtons)):
                    page_buttons.append(newButtons[i])
                    #print(page_buttons[i].text)
                    if(i == randomPage):
                        newButtons[i].click()
                        driver.implicitly_wait(500)
                        print("Page clicked")
    
#Once again, we need to pick a random page to transcribe. This time, we will need to pick a random page from the list of pages that are available for transcription.
#We will need to pick a random page from the list of pages that are available for transcription.

    newValue2 = driver.find_elements(By.TAG_NAME, 'h6')
    randomPage = random.randint(0, len(newValue2) - 1)
    for i in range(len(newValue2)):
        #print(newValue2[i].text)
        if(i == randomVal):
            newValue2[i].click()
    driver.implicitly_wait(1500)
    print("Page clicked")

#Pick a random page to transcribe. This time, we will need to pick a random page from the list of pages that are available for transcription.

    transcribeTags = driver.find_elements(By.CLASS_NAME, 'card-img-container')
    randomTag = random.randint(0, len(transcribeTags) - 1)
    for i in range(len(transcribeTags)):
        if(i == randomTag):
            transcribeTags[i].click()
            driver.implicitly_wait(1500)
            print("Tag clicked")


    def transcribeLoop(self, numPages):
        stringTexts = []
        for i in range(numPages):
            self.driver.implicitly_wait(2500)
            self.driver.find_element(By.XPATH, '//*[@id="viewer-fullscreen"]/span').click()
            self.driver.implicitly_wait(5500)
            self.driver.implicitly_wait(3500)
            self.driver.save_screenshot('num' + str(i) + '.png')
            self.driver.implicitly_wait(6500)
            self.driver.implicitly_wait(3500)
            self.driver.find_element(By.XPATH, '//*[@id="viewer-fullscreen"]/span').click()
            self.driver.implicitly_wait(3500)
            self.driver.implicitly_wait(3500)
    
            img = cv2.imread('num' + str(i) + '.png', 0)
            #grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #blur = cv2.GaussianBlur(grey, (5, 5), 0)
            #thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            kernel = np.ones((1,1),np.uint8)
            opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=2)
            #invert = 255 - opening
            data = pytesseract.image_to_string(opening, lang='eng', config='--psm 6')
            img = Image.fromarray(img)
            img = img.filter(ImageFilter.SHARPEN)
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(2)
            img = img.convert('1')
            img.save('num' + str(i) + '.png')

            transcribedText = data
            stringTexts.append(transcribedText)
            textField = self.driver.find_element(By.XPATH,'//*[@id="transcription-input"]')
            textField.send_keys(stringTexts[i])
            self.driver.implicitly_wait(1500)
            self.driver.find_element(By.XPATH, '//*[@id="save-transcription-button"]').click()
            self.driver.implicitly_wait(1500)
            self.driver.find_element(By.XPATH, '//*[@id="submit-transcription-button"]').click()
            self.driver.implicitly_wait(1500)
            self.driver.find_element(By.XPATH, '//*[@id="successful-submission-modal"]/div/div/div[3]/p[2]/a').click()


    #Transcription loop
    index = 0
    #while(int index < numPages):
    
    #Call the transcribeLoop method
    
A = AutoTranscriber()
A.transcribeLoop(2)

        #index += 1









































































