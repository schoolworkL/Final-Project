import tkinter as tk
from tkinter import *
import requests
from bs4 import BeautifulSoup
import time


class Scrape(tk.Tk):
    def __init__(self):
        super().__init__()
        frame = tk.Frame(master=self)
        frame.pack()
        self.geometry("400x400")
        self.search()

    def read_reddit(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        return r, soup

    def open_posts(self, data, value):
        print(value)
        r, soup = Scrape.read_reddit(self, data[value][3])
        #print(page)

    def button_pressed(button, lst):
        # `button.cget("text")` gets text attribute of the button
        print("Button text =", button.cget("text"))

        def sorter(lst):
            for i in range(len(lst) - 1, 0, -1):  # iterates through the list backwards
                value = 0  # variable to the second value
                for j in range(1, i + 1):  # iterates through the list using i+1 as the end range
                    if lst[j][0] > lst[value][
                        0]:  # checks if the second value in the tuple is greater than the second value in the second
                        # tuple
                        value = j  # sets value to equal j
                lst[j], lst[value] = lst[value], lst[j]  # switches the values of list[j] and list[value]
            return lst  # returns the sorted list to the main

        def binary_search(arr, low, high, x):

            # Check base case
            if high >= low:

                mid = (high + low) // 2

                # If element is present at the middle itself
                if (str(arr[mid][0]) + '\n' + str(arr[mid][1]) + '\n' + str(arr[mid][2])) == x:
                    #print(str(arr[mid][0])+str(arr[mid][1])+' '+str(arr[mid][2]))
                    return mid

                # If element is smaller than mid, then it can only
                # be present in left subarray
                elif (str(arr[mid][0]) + '\n' + str(arr[mid][1]) + '\n' + str(arr[mid][2])) > x:
                    #print(str(arr[mid][0]) + '\n' + str(arr[mid][1]) + '\n' + str(arr[mid][2]))
                    return binary_search(arr, low, mid - 1, x)

                # Else the element can only be present in right subarray
                else:
                    #print(str(arr[mid][0]) + str(arr[mid][1]) + ' ' + str(arr[mid][2]))
                    return binary_search(arr, mid + 1, high, x)

            else:
                # Element is not present in the array
                return -1

        lst = sorter(lst)
        # Function call
        result = binary_search(lst, 0, len(lst) - 1, str(button.cget("text")).strip())

        if result != -1:
            print("Element is present at index", str(result))
            print(lst[result])
        else:
            print("Element is not present in array")

    def checker(self, url):
        lst = []
        lst_2 = []
        count = 0
        r, soup = Scrape.read_reddit(self, url)
        rows = soup.find_all('div', {"class": "link"})
        time.sleep(.05)
        while True:
            for i in rows:
                try:
                    lst.append([])
                    tagline = i.find("p", {"class": "tagline"}).text.strip()
                    comments = i.find("li", {"class": "first"}).text.strip()
                    page = i.find("a", {"class": "bylink"})
                    page_url = page["href"]
                    print(tagline)
                    print(comments)
                    print(page_url)
                    lst[count].append(i.find("p", {"class": "title"}).text.strip())
                    lst[count].append(f"\n{tagline}")
                    lst[count].append(comments)
                    lst[count].append(page_url)
                    count += 1
                except:
                    pass
            # ensures the window always pulls up. Sometimes code can't get data fast enough for the list.
            if not lst:
                print(lst)
                time.sleep(.25)
                return Scrape.checker(self, url)
            else:
                break

        results = Toplevel(self)
        results.geometry('500x500')
        heading = results.title('Front of Reddit')
        main_frame = Frame(results)


        canvas = Canvas(main_frame)
        scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        for i in lst:
            text_2 = StringVar()
            text_2.set(i[0] + '\n' + i[1] + '\n' + i[2])
            #main_frame = Frame(results, highlightthickness=2, bd=10, highlightbackground='red')

            button = Button(scrollable_frame, textvariable=text_2, highlightthickness=0, bd=0)
            button.config(
                command=lambda button=button: Scrape.button_pressed(button, lst))  #Scrape.open_posts(self, lst,)
            button.pack()

        main_frame.pack(fill=BOTH, expand=1)
        #canvas.config(yscrollcommand=scroll_bar.set)
        #canvas.bind('<configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    def search(self):
        tk.Button(text="Reddit", command=lambda: Scrape.checker(self, 'https://old.reddit.com/')).pack()

        #tk.Label(textvariable=text).pack()


Scrape().mainloop()