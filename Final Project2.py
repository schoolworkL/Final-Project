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
        rows = soup.find_all('div', {"class": "top-matter"})
        #print(r)
        #print(rows)
        for i in rows:
            try:
                #title = i.select.('div div div p a').text.strip()
                #print(title)
                #title_r = title[0]
                lst.append(i.find('p', {"class": "title"}).text)
            except:
                pass

        print(lst)


        results = Toplevel(self)
        heading = results.title('Front of Reddit')
        for i in lst:
            text_2 = StringVar()
            text_2.set(i)
            print(i)
            text = Label(results, textvariable=text_2)
            text.pack()

    def search(self):
        search_bar = tk.Entry()
        search_bar.pack()
        text_2 = StringVar()
        tk.Button(text="Reddit", command=lambda: Scrape.checker(self, 'https://old.reddit.com/')).pack()

        #tk.Label(textvariable=text).pack()


Scrape().mainloop()
