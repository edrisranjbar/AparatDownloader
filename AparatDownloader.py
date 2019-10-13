# Import libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import wget

url = "https://www.aparat.com/v/Z9OH0"
savePath = "/home/edris/Dev/Aparat"
browser = webdriver.Chrome(executable_path="/home/edris/Dev/Aparat/chromedriver")

browser.get(url)

browser.find_element_by_xpath("/html/body/main/div[1]/div/div/div/div/section[2]/div/div[2]/div[2]/div[2]/div[1]/div[1]/div/button").click()
DownloadLink = browser.find_elements_by_css_selector(".dropdown .dropdown-content .menu-wrapper .menu-list .menu-item-link a")[4]
DownloadLink = DownloadLink.get_attribute("href")
print("Download {0} Started! \n".format(DownloadLink))
DownloadStatus = wget.download(DownloadLink)
while DownloadLink == False:
    print("Downloading... \n")
    
else:
    print("Download is Done \n!")
#browser.close()