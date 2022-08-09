from tkinter import *
import os
from scrapper import Scrapper

downloader = Scrapper(os.getcwd())


def download():
    if downloader.isUrlValid(txtUrl.get()):
        downloader.downloadPlaylistVideos(txtUrl.get())
        lblCount['text'] = "Count of downloaded videos:" + \
            str(downloader.count)
    print(downloader.errors)
    lblErrors['text'] = downloader.errors


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
Button(root, text="Download", command=download).pack()
root.mainloop()
