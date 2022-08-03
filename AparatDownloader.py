# Import libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import wget
import os
from tkinter import *


class AparatDownloader():
    def __init__(self):
        self.currentFolder = os.getcwd()
        self.url = ""
        self.count = 0
        self.videoLinks = []
        self.errors = ""

    def isValid(self, url):
        if "https://www.aparat.com/" in url:
            self.errors = ""
            return True
        else:
            self.errors = "URL is invalid!"
            return False

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
                self.errors = "\n Download link was not found"
                return False
        except:
            self.errors = "\n URL is invalid or no internet"
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


# Inititalizing UI
root = Tk()
root.resizable(FALSE, FALSE)
root.minsize(250, 250)
root.title("Aparat Downloader")
lblErrors = Label(root, text="")
lblErrors.pack()
Label(root, text="Type URL:").pack()
txtUrl = Entry(root)
txtUrl.pack()
lblCount = Label(root, text="Count of downloaded videos:")
lblCount.pack()


def download():
    if downloader.isValid(txtUrl.get()):
        downloader.downloadFromPlayList(txtUrl.get())
        lblCount['text'] = "Count of downloaded videos:" + \
            str(downloader.count)
    print(downloader.errors)
    lblErrors['text'] = downloader.errors


downloader = AparatDownloader()

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install())
                           )

Button(root, text="Download", command=download).pack()

root.mainloop()
browser.close()
