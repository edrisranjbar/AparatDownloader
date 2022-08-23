from xmlrpc.client import Boolean
from selenium import webdriver
from selenium. webdriver. common. keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import wget
from time import sleep
from os import getcwd


class Scrapper():
    def __init__(self):
        self.currentFolder = getcwd()
        self.quality_selectors = {
            "1080": "//*[@id='1080p']/div/span/span",
            "720": "//*[@id='720p']/div/span/span",
            "480": "//*[@id='480p']/div/span/span",
            "360": "//*[@id='360p']/div/span/span",
            "240": "//*[@id='240p']/div/span/span",
            "144": "//*[@id='144p']/div/span/span",
        }
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

    def isAPlayList(self, url) -> Boolean:
        selector = "single-playlist"
        self.browser.get(url)
        sleep(30)
        return len(self.browser.find_elements(By.CLASS_NAME, selector)) > 0

    def isUrlValid(self, url):
        if "aparat.com/" in url:
            self.errors = ""
            return True
        else:
            self.errors = "URL is invalid!"
            return False

    def getASingleVideoDownloadLink(self, url, quality='720'):
        if (self.isUrlValid(url) is False):
            raise Exception("URL is invalid") from None
        self.browser.get(url)
        sleep(30)
        self.title = self.browser.title
        try:
            # Download button
            self.browser.find_element(By.CSS_SELECTOR,
                                      "#primary > div.single-details > div.single-details__info > div.single-details__utils > div > div > div.download-button > div > div > button").click()

            # Download link with 720p
            self.browser.find_element(
                By.XPATH, self.quality_selectors[quality]).click()
            sleep(5)
            self.browser.switch_to.window(self.browser.window_handles[-1])
            return self.browser.current_url
        except Exception as error1:
            self.errors = f"\nDownload link was not found\n {error1}"
            raise Exception("Download link was not found") from error1
        finally:
            self.browser.close()

    def downloadSingleVideo(self, DownloadLink):
        try:
            wget.download(DownloadLink, self.currentFolder +
                          "/"+self.title+".mp4")
        except Exception as error:
            raise Exception("Can not download") from error

    def getPlaylistVideoLinks(self, url):
        self.browser.get(url)
        sleep(30)
        links = self.browser.find_elements(By.CSS_SELECTOR,
                                           "a.titled-link.title[data-refer=playlists]")
        for link in links:
            self.videoLinks.append(link.get_attribute("href"))
        return self.videoLinks

    def downloadPlaylistVideos(self, url):
        self.getPlaylistVideoLinks(url)
        for link in self.videoLinks:
            downloadLink = self.getASingleVideoDownloadLink(link)
            self.downloadSingleVideo(downloadLink)
            self.count += 1

    def getVideoQualitiesLink(self, url):
        found_qualities = []
        self.browser.get(url)
        sleep(20)
        # Download button
        self.browser.find_element(By.CSS_SELECTOR,
                                  "#primary > div.single-details > div.single-details__info > div.single-details__utils > div > div > div.download-button > div > div > button").click()
        for quality in self.quality_selectors:
            if self.browser.find_element(By.XPATH, self.quality_selectors[quality]).is_displayed():
                found_qualities.append(quality)
        return found_qualities
