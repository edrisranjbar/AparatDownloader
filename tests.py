import sys
import unittest
from scrapper import *


class ScrapperTest(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.downloader = Scrapper()

    def testThatAllRequirementsSatisfied(self):
        if sys.modules.get('wget') is None or sys.modules.get('selenium') is None \
                or sys.modules.get('webdriver_manager') is None or sys.modules.get('time') is None:
            self.fail("requirements are not satisfied")

    def testThatUrlValidationWorks(self):
        validUrls = [
            "https://www.aparat.com/v/4Z9Zb",
            "www.aparat.com/v/4Z9Zb/",
        ]
        invalidUrls = [
            "https://www.google.com/",
            "aparat.co/v/4Z9Zb",
            # "edrisranjbar.ir/www.aparat.com/",
            # "https://www.edrisranjbar.ir/index.php?www.aparat.com/",
        ]
        for url in validUrls:
            self.assertTrue(self.downloader.isUrlValid(url))
        for url in invalidUrls:
            self.assertIsNot(self.downloader.isUrlValid(url), True)

    def testThatWeCanGetDownloadLinkOfASingleVideo(self):
        url = "https://www.aparat.com/v/6hSwx"
        downloadLink = self.downloader.getASingleVideoDownloadLink(url)
        self.assertTrue(
            "https://" in downloadLink
        )

    def testThatWeGetPropperErrorMessages(self):
        # expect to get "Download link was not found"
        with self.assertRaisesRegex(Exception, "Download link was not found"):
            self.downloader.getASingleVideoDownloadLink(
                "https://www.aparat.com/v/6hSws2dsdsd")

        # expect to get "URL is invalid"
        with self.assertRaisesRegex(Exception, "URL is invalid"):
            self.downloader.getASingleVideoDownloadLink(
                "aparat.co/v/4Z9Zb")

    def testThatWeCanDownloadAFile(self):
        self.downloader.title = "test video"
        dl_link = "https://aspb26.cdn.asset.aparat.com/aparat-video/56b2e43e9d89dbf760db3a1f672696e332127095-144p.mp4?wmsAuthSign=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6ImI1NGJiZWQ0ZWYwNTk0NTRkODRiZmMyZjIwMTk3YmQyIiwiZXhwIjoxNjYxMzAxNTkxLCJpc3MiOiJTYWJhIElkZWEgR1NJRyJ9.jW-pu7yXyIoETHIfkqp9882noLmt8oM9OqTcIDuEiMs"
        try:
            self.downloader.downloadSingleVideo(
                dl_link)
        except Exception as errorMessage:
            self.fail(errorMessage)

    def testThatWeCanGetAllOfTheVideosLinksInAPlaylist(self):
        # returned links list's length should be more that 0
        count = len(self.downloader.getPlaylistVideoLinks(
            "https://www.aparat.com/v/GojkW"))
        self.assertGreater(count, 0)

    def testThatWeCanDetectPlaylistURL(self):
        isAPlayList = self.downloader.isAPlayList(
            "https://www.aparat.com/v/GojkW")
        self.assertTrue(isAPlayList)
