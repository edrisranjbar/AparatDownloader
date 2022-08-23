from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import wget
from time import sleep
from os import getcwd


class Scrapper():
    def __init__(self):
        self.currentFolder = getcwd()
        self.count = 0
        self.videoLinks = []
        self.errors = ""
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option(
            "excludeSwitches", ["enable-logging"])
        self.options.add_argument('headless')
        self.browser = webdriver.Chrome(options=self.options,
                                        service=Service(
                                            ChromeDriverManager().install()
                                        )
                                        )

    def isUrlValid(self, url):
        if "aparat.com/" in url:
            self.errors = ""
            return True
        else:
            self.errors = "URL is invalid!"
            return False

    def getASingleVideoDownloadLink(self, url):
        if (self.isUrlValid(url) is False):
            raise Exception("URL is invalid") from None
        self.browser.get(url)
        sleep(10)
        self.title = self.browser.title
        try:
            # Download button
            self.browser.find_element(By.CSS_SELECTOR,
                                      "#primary > div.single-details > div.single-details__info > div.single-details__utils > div > div > div.download-button > div > div > button").click()

            # Download link with 720p
            self.browser.find_element(
                By.XPATH, "//*[@id='720p']/div/span/span").click()
            sleep(5)
            self.browser.switch_to.window(self.browser.window_handles[-1])
            return self.browser.current_url
        except Exception as error1:
            self.errors = f"\nDownload link was not found\n {error1}"
            raise Exception("Download link was not found") from None
        finally:
            self.browser.close()

    def downloadSingleVideo(self, DownloadLink):
        wget.download(DownloadLink, self.currentFolder +
                      "/"+self.title+".mp4")

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
            downloadLink = self.getASingleVideoDownloadLink(link)
            self.downloadSingleVideo(downloadLink)
            self.count += 1
