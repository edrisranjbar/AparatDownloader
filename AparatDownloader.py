# Import libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import wget
import os


class AparatDownloader():
    def __init__(self):
        self.currentFolder = os.getcwd()
        self.url = ""
        self.count = 0
        self.videoLinks = []

    def isValid(self, url):
        if "https://www.aparat.com/" in url:
            return True
        else:
            print("URL is invalid!")
            self.getUrl()

    def getUrl(self):
        userUrl = input("Give me the URL: ")
        if self.isValid(userUrl):
            self.url = userUrl

    def downloadWithUrl(self, url):
        try:
            browser.get(url)
            title = browser.title
            try:
                # Download button
                browser.find_element_by_xpath(
                    "/html/body/main/div[1]/div/div/div/div/section[2]/div/div[2]/div[2]/div[2]/div[1]/div[1]/div/button").click()

                # Get Download link with 720p
                DownloadLink = browser.find_elements_by_css_selector(
                    ".dropdown .dropdown-content .menu-wrapper .menu-list .menu-item-link a")[4]
                DownloadLink = DownloadLink.get_attribute("href")

                # Download the video with the name of page
                wget.download(DownloadLink, self.currentFolder +
                              "/"+title+".mp4")
            except:
                print("\n Download link was not found")
                return False
        except:
            print("\n URL is invalid or no internet")
            return False
        return True

    def downloadFromPlayList(self, url):
        browser.get(url)
        links = browser.find_elements_by_css_selector(
            ".playlist-body .thumb-title a")
        for link in links:
            self.videoLinks.append(link.get_attribute("href"))

        for link in self.videoLinks:
            self.downloadWithUrl(link)
            self.count += 1


downloader = AparatDownloader()

browser = webdriver.Chrome(
    executable_path="{0}/chromedriver".format(downloader.currentFolder))

downloader.getUrl()
downloader.downloadFromPlayList(downloader.url)

browser.close()
print("---------------------------------")
print("Count of downloaded videos: " + str(downloader.count))
