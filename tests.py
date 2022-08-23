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
        print(downloadLink)
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
