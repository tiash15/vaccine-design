#automating bulk submission for vaxijen 2.0 server
#takes a list of protein sequences as input and gives back the list
# of prot seq that are probable antigens
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import csv

def filterNonAllergens(seqList):
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get("https://www.ddg-pharmfac.net/AllerTOP/")

    filteredNonAllergens = []
    i = 1

    for seq in seqList:
        try:
            #locate the textarea for entering the seq
            protSeq = WebDriverWait(driver,55).until(
                EC.presence_of_element_located((By.NAME, 'sequence'))
            )
            #enter the seq
            protSeq.send_keys(seq)
            
            submit = WebDriverWait(driver,55).until(
                EC.presence_of_element_located((By.NAME, 'Submit'))
            )
            submit.click()

            result = WebDriverWait(driver,55).until(
                EC.presence_of_element_located((By.XPATH,'//*[@id="box"]/h4[2]' ))
            )
            
            if(result.text == 'PROBABLE NON-ALLERGEN'):
                filteredNonAllergens.append(seq)
                print(i, ": OK")
                i = i + 1
                writer.writerow([i, seq])

            elif(result.text == 'PROBABLE ALLERGEN'):
                print(i, ": ALLERGEN")

        except:
            driver.quit()
            print("Something went wrong")
            c.close()
        finally:
            driver.back()

    return filteredNonAllergens

#test 1 
f = open('shuffled_vaccines.txt', 'r')
seqList = f.read().splitlines()
f.close()
c = open('probableAntigens.csv', 'a')
writer = csv.writer(c)
filterNonAllergens(seqList)
c.close()


