import tkinter as tk
from tkinter import *
import requests
from bs4 import BeautifulSoup


class Scrape(tk.Tk):
    def __init__(self):
        super().__init__()
        frame = tk.Frame(master=self)
        frame.pack()
        self.geometry("400x400")
        self.search()

    def checker(self, url):
        print(url)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        rows = soup.select('html body shreddit-app dsa-transparency-modal-provider div div div main shreddit-post h1')
        title = rows[0].text.strip()
        print(title)
        return title



    def search(self):
        search_bar = tk.Entry()
        search_bar.pack()
        text_2 = StringVar()
        tk.Button(text='Press to Search', command=lambda: Scrape.checker(self, search_bar.get())).pack()
        #tk.Label(textvariable=text).pack()



Scrape().mainloop()
