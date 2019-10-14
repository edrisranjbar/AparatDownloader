# Import libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import wget,os

currentFolder = os.getcwd()
urls = []
count = 0

# Getting URLs
def getUrl():
    message ="Give me the URL: (N for exit getting URL)"
    # If it is a NO or something like this
    if len(message) < 5:
        return input(message).lower()
    return input(message)

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
            print("\n Something went wrong")
            return
    except:
        print("\n URL is invalid or no internet")
        return
    return True


userUrl = getUrl()
while userUrl!="n" and userUrl != "no":
    urls.append(userUrl)
    userUrl = getUrl()

browser = webdriver.Chrome(executable_path="{0}/chromedriver".format(currentFolder))
for url in urls:
    status = downloadWithUrl(url)
    if status:
        count += 1
browser.close()
print("---------------------------------")
print("Count of downloaded videos: " + str(count))