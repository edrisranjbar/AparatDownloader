# Import libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import wget
import os
from tkinter import *
from time import sleep


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
            sleep(6)
            title = browser.title
            try:
                # Download button
                browser.find_element(By.CSS_SELECTOR,
                                     "#primary > div.single-details > div.single-details__info > div.single-details__utils > div > div > div.download-button > div > div > button").click()

                # Get Download link with 720p
                DownloadLink = browser.find_element(By.XPATH,
                                                    "//*[@id='720p']/div/span/span").click()
                sleep(3)
                DownloadLink = browser.current_url

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
        sleep(10)
        links = browser.find_elements(By.CSS_SELECTOR,
                                      "a.titled-link.title[data-refer=playlists]")
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

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
browser = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install())
                           )

Button(root, text="Download", command=download).pack()

root.mainloop()
browser.close()
