# Import libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import wget,os

currentFolder = os.getcwd()
urls = []
count = 0

# URL Validation
def isValid(url):
    if "https://www.aparat.com/" in url:
        return True
    else:
        return False


# Getting URLs
def getUrl():
    message ="Give me the URL: (N or NO for exit getting URL)"
    userUrl = input(message)
    if len(userUrl) > 2:
        if isValid(userUrl):
            urls.append(userUrl)
            getUrl()
        else:
            print("URL is invalid!")
    else:
        userUrl.lower()
        if userUrl == "n" or userUrl == "no":
            return

        
# Download Based on URL
def downloadWithUrl(url):
    try:
        browser.get(url)
        title = browser.title
        try:
            # Download button
            browser.find_element_by_xpath("/html/body/main/div[1]/div/div/div/div/section[2]/div/div[2]/div[2]/div[2]/div[1]/div[1]/div/button").click()
            
            # Get Download link with 720p
            DownloadLink = browser.find_elements_by_css_selector(".dropdown .dropdown-content .menu-wrapper .menu-list .menu-item-link a")[4]
            DownloadLink = DownloadLink.get_attribute("href")
            
            # Download the video with the name of page
            wget.download(DownloadLink,currentFolder+"/"+title+".mp4")
        except:
            print("\n Download link was not found")
            return False
    except:
        print("\n URL is invalid or no internet")
        return False
    return True


browser = webdriver.Chrome(executable_path="{0}/chromedriver".format(currentFolder))
getUrl()

for url in urls:
    status = downloadWithUrl(url)
    if status:
        count += 1

browser.close()
print("---------------------------------")
print("Count of downloaded videos: " + str(count))