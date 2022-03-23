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


#filterAntigen takes the list of prot seq,
#threshold value (optional/default:0.4) and
#organism type(optional:default:virus)
def filterAntigens(seqList, THRESHOLD = '0.4', ORGANISM = 'virus'):
    #set up the driver
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get("http://www.ddg-pharmfac.net/vaxijen/VaxiJen/VaxiJen.html")

    #values that are saved automatically after one run 
    threshold = driver.find_element_by_name("threshold")
    threshold.send_keys(THRESHOLD)
    target = driver.find_element_by_name("Target")
    select_target = Select(target)
    select_target.select_by_value(ORGANISM)

    #store probable antigenic seq in this list
    filteredAntigens = []

    for seq in seqList:
        try:
            #locate the textarea for entering the seq
            protSeq = WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.NAME, 'seq'))
            )
            #enter the seq
            protSeq.send_keys(seq)

            #locate and click the submit button
            submit = WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.NAME, 'submit'))
            )
            submit.click()
            #wait and obtain the result
            result = WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.XPATH,'/html/body/div/table/tbody/tr[4]/td[3]/table/tbody/tr/td/b[4]/font' ))
            )
            #check if antigenic or non antigenic
            if(result.text == 'ANTIGEN'):
                filteredAntigens.append(seq)
        except:
            driver.quit()
            print("DRIVER FAILED FOR SOME REASON")
        finally:
            driver.back()
    
    return filteredAntigens
