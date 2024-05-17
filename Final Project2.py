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
        lst = []
        print(url)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        rows = soup.select('html body div div')
        #print(rows)
        for i in rows:
            title = i.select('div div div p a')
            print(title)
            #title_r = title[0]
            lst.append(title)

        print(lst)
        #title = rows[0]
        #title2 = title.select_one('.linklisting')
        #print(title2)
        #return title



    def search(self):
        search_bar = tk.Entry()
        search_bar.pack()
        text_2 = StringVar()
        tk.Button(text='Press to Search', command=lambda: Scrape.checker(self, 'https://old.reddit.com/')).pack()
        #tk.Label(textvariable=text).pack()



Scrape().mainloop()
