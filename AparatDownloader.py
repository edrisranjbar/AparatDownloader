# Import libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import wget,os

currentFolder = os.getcwd()
urls = []

# Getting URLs
userUrl = input("Give me the URL: (N for exit getting URL)")
while userUrl!="n":
    urls.append(userUrl)
    userUrl = input("Give me the URL: (N for exit getting URL)")

browser = webdriver.Chrome(executable_path="{0}/chromedriver".format(currentFolder))
for url in urls:
    browser.get(url)
    title = browser.title
    browser.find_element_by_xpath("/html/body/main/div[1]/div/div/div/div/section[2]/div/div[2]/div[2]/div[2]/div[1]/div[1]/div/button").click()
    DownloadLink = browser.find_elements_by_css_selector(".dropdown .dropdown-content .menu-wrapper .menu-list .menu-item-link a")[4]
    DownloadLink = DownloadLink.get_attribute("href")
    DownloadStatus = wget.download(DownloadLink,currentFolder+"/"+title+".mp4")
browser.close()