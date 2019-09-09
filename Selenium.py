from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import os
import time
import csv


base_url = 'https://www.dir.ca.gov/pwc100ext/ExternalLookup.aspx'
header = ['ID','Awarding Body','Project Name','Site Address','Dates','Classification','County','Contractor PWCR/CSLB/Lic','Contractor Name','Sub Contractor PWCR/CSLB/Lic','Sub Contractor Name']
with open('DIR_Projects.csv', 'w') as csv_file:
	csvwriter = csv.writer(csv_file)
	csvwriter.writerow(header)

# Firefox session
with open ("names.txt") as name:
	for i in name:
		driver = webdriver.Firefox()
		driver.get(base_url)
		driver.implicitly_wait(100)
		selectElem=driver.find_element_by_xpath('//*[@id="Mstr_BodyContent_txtProjectName"]')
		selectElem.clear()
		selectElem.send_keys(i)
		submission=driver.find_element_by_xpath('//*[@id="Mstr_BodyContent_Button1"]')
		submission.click()
		time.sleep(1)
		html = driver.page_source
		soup = BeautifulSoup(html, "lxml")
		print('Gathered ', i)

		#GET OVERALL TABLE
		table = soup.find('table', id='Mstr_BodyContent_tblResults')		

		#GET TH OF TABLE
		table_th = table.findAll('th')		

		#GET TR OF TABLE
		cols = table.findAll('tr')		

		#GET SPECIFIC TR
		data = cols[2]			

		#LIC DATA
		licdata = cols[5].findAll('td')		
		
		

		#GET TD OF SPECIFIC TR
		rows = data.findAll('td')		
		
		
		

		#GET ROW DATA
		row_all = []
		for row in rows:
			row_all.append(row.text)
		for lic in licdata:
			row_all.append(lic.text)		
		
		
		

		###WRITE CSV###
		with open('DIR_Projects.csv', 'a') as csv_file:
			csvwriter = csv.writer(csv_file)
			csvwriter.writerow(row_all)

		driver.close()

driver.quit()