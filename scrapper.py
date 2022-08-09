from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import wget

from time import sleep


class Scrapper():
    def __init__(self, currentFolder):
        self.currentFolder = currentFolder
        self.count = 0
        self.videoLinks = []
        self.errors = ""
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option(
            "excludeSwitches", ["enable-logging"])
        self.options.add_argument('headless')
        self.browser = webdriver.Chrome(options=self.options, service=Service(ChromeDriverManager().install())
                                        )

    def isUrlValid(self, url):
        if "https://www.aparat.com/" in url:
            self.errors = ""
            return True
        else:
            self.errors = "URL is invalid!"
            return False

    def downloadSingleVideo(self, url):
        try:
            self.browser.get(url)
            sleep(6)
            title = self.browser.title
            try:
                # Download button
                self.browser.find_element(By.CSS_SELECTOR,
                                          "#primary > div.single-details > div.single-details__info > div.single-details__utils > div > div > div.download-button > div > div > button").click()

                # Get Download link with 720p
                DownloadLink = self.browser.find_element(By.XPATH,
                                                         "//*[@id='720p']/div/span/span").click()
                sleep(3)
                self.browser.switch_to.window(self.browser.window_handles[-1])
                DownloadLink = self.browser.current_url

                # Download the video with the name of page
                wget.download(DownloadLink, self.currentFolder +
                              "/"+title+".mp4")
            except Exception as error:
                self.errors = f"\nDownload link was not found\n {error}"
                return False
        except Exception as error:
            self.errors = f"\nURL is invalid or no internet\n {error}"
            return False
        finally:
            self.browser.close()
        return True

    def getPlaylistVideoLinks(self, url):
        self.browser.get(url)
        sleep(10)
        links = self.browser.find_elements(By.CSS_SELECTOR,
                                           "a.titled-link.title[data-refer=playlists]")
        for link in links:
            self.videoLinks.append(link.get_attribute("href"))

    def downloadPlaylistVideos(self, url):
        self.getPlaylistVideoLinks(url)
        for link in self.videoLinks:
            self.downloadSingleVideo(link)
            self.count += 1
