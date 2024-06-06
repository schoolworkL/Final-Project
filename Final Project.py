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
        self.lst = [[]]
        self.geometry("400x400")
        self.search()
        self.tracker = 0
        self.selection = 0
        self.setting = 0


    def read_reddit(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        return r, soup

    def open_posts(self, data, value):
        print(value)
        r, soup = Scrape.read_reddit(self, data[value][3])
        #print(page)

    def binary_search(arr, low, high, x, setting):
        #print(f'hi {x}')
        #print(f'Joe: {setting}')
        # Check base case
        print(f'option: {x}')
        print(f'setting {setting}')
        if high >= low:

            mid = (high + low) // 2
            #print(f'point {(str(arr[mid][setting]))}')
            # If element is present at the middle itself
            if (str(arr[mid][setting])) == x[setting]:
                # print(str(arr[mid][0])+str(arr[mid][1])+' '+str(arr[mid][2]))
                return mid

            # If element is smaller than mid, then it can only
            # be present in left subarray
            elif (str(arr[mid][setting])) > x[setting]:
                # print(str(arr[mid][0]) + '\n' + str(arr[mid][1]) + '\n' + str(arr[mid][2]))
                return Scrape.binary_search(arr, low, mid - 1, x, setting)

            # Else the element can only be present in right subarray
            else:
                # print(str(arr[mid][0]) + str(arr[mid][1]) + ' ' + str(arr[mid][2]))
                return Scrape.binary_search(arr, mid + 1, high, x, setting)

        else:
            # Element is not present in the array
            return -1

    def sorter(self, lst, direction, i_value):
        # print(lst)
        #print(lst)
        if direction == 1:  # least to greatest sort
            for i in range(len(lst) - 1, 0, -1):  # iterates through the list backwards
                value = 0  # variable to the second value
                for j in range(1, i + 1):  # iterates through the list using i+1 as the end range
                    if lst[j][i_value] > lst[value][
                        i_value]:  # checks if the second value in the tuple is greater than the second value in the second
                        # tuple
                        value = j  # sets value to equal j
                lst[j], lst[value] = lst[value], lst[j]  # switches the values of list[j] and list[value]
            return lst  # returns the sorted list to the main
        else:  # greatest to the least sort
            for i in range(len(lst) - 1, 0, -1):  # iterates through the list backwards
                value = 0  # variable to the second value
                for j in range(1, i + 1):  # iterates through the list using i+1 as the end range
                    if lst[j][i_value] < lst[value][
                        i_value]:  # checks if the second value in the tuple is greater than the second value in the second
                        # tuple
                        value = j  # sets value to equal j
                lst[j], lst[value] = lst[value], lst[j]  # switches the values of list[j] and list[value]
            return lst  # returns the sorted list to the main

    def sort_button(self, data, i_value, option):
        value = str(option.cget("text"))
        if value == "Alphabetical":
            self.setting = 0
        elif value == "Upvotes":
            self.setting = 3
        else:
            self.setting = -2

        if self.tracker % 2 == 0:
            self.tracker += 1
            #print(self.lst)
            #print(self.tracker)
            return Scrape.sorter(self, data, 1, i_value)
        else:
            self.tracker += 1
            #print(self.lst)
            #print(self.tracker)
            return Scrape.sorter(self, data, 0, i_value)

    def button_pressed(self, button, lst):
        # `button.cget("text")` gets text attribute of the button
        #print("Button text =", button.cget("text"))
        #print(str(button.cget("text")).splitlines())
        options = (button.cget("text")).splitlines()
        options_updated = [line.split() for line in options]
        options_updated = [item for item in options_updated if item != []]
        #print(options_updated[-1])
        options_updated[-1].remove("Upvotes")
        options_updated[-2].remove("comments")
        options_updated[0] = ' '.join(options_updated[0])
        options_updated[1] = ' '.join(options_updated[1])
        options_updated[2] = ' '.join(options_updated[2])
        options_updated[3] = ' '.join(options_updated[3])
        #print(f'checker {options_updated}')
        #new_options = [options_updated[0], options_updated[2], holder, holder_2]
        #print(new_options)
        # Function call
        #selection = options[-1]
        #print(f'option: {options_updated}')
        result = Scrape.binary_search(lst, 0, len(lst) - 1, options_updated, self.setting)
        #print(result)

        if result != -1:
            print("Element is present at index", str(result))
            #print(lst[result])
        else:
            print("Element is not present in array")

    def checker(self, url):

        lst_2 = []
        count = 0
        r, soup = Scrape.read_reddit(self, url)
        rows = soup.find_all('div', {"class": "link"})
        time.sleep(.05)
        while True:
            for i in rows:
                try:

                    tagline = i.find("p", {"class": "tagline"}).text.strip()
                    comments = i.find("li", {"class": "first"}).text.strip()
                    page = i.find("a", {"class": "bylink"})
                    page_url = page["href"]
                    likes = i.find("div", {"class": "score"})
                    exact_likes = likes["title"]
                    #print(tagline)
                    #print(comments)
                    #print(page_url)
                    self.lst[count].append(i.find("p", {"class": "title"}).text.strip())
                    self.lst[count].append(f"\n{tagline}")
                    self.lst[count].append(comments)
                    self.lst[count].append(page_url)
                    self.lst[count].append(exact_likes)
                    count += 1
                    self.lst.append([])
                except:
                    pass

            # ensures the window always pulls up. Sometimes code can't get data fast enough for the list.
            if not self.lst:
                print(self.lst)
                time.sleep(.25)
                return Scrape.checker(self, url)
            else:
                self.lst = [item for item in self.lst if item != []]
                break

        self.lst = Scrape.sorter(self, self.lst, 1, 0)  # sorts list least to greatest
        for i in range(len(self.lst)):
            l = str(self.lst[i][2]).split()
            self.lst[i][2] = l[0]
            self.lst[i].insert(3, l[1])
            #print(self.lst[i][2])


        Scrape.results = Toplevel(self)
        Scrape.results.geometry('600x500')
        heading = Scrape.results.title('Front of Reddit')

        m_canvas = Canvas(Scrape.results)
        m_canvas.config(width=600, height=500)

        m_canvas.config(scrollregion=(0, 0, 300, 2700))

        y_axis = Scrollbar(Scrape.results)
        y_axis.config(command=m_canvas.yview)

        m_canvas.config(yscrollcommand=y_axis.set)
        y_axis.pack(side=RIGHT, fill=Y)
        m_canvas.pack(side=LEFT, expand=YES, fill=BOTH)
        top_frame = Frame(Scrape.results)
        sort_options = Label(top_frame, text="Sort by:")
        option_1 = Button(top_frame, text="Alphabetical")
        option_1.config(
            command=lambda button=option_1: Scrape.sort_button(self, self.lst, 0, button))
        option_2 = Button(top_frame, text="Upvotes")
        option_2.config(
            command=lambda button=option_2: Scrape.sort_button(self, self.lst, -1, button))
        option_3 = Button(top_frame, text="Comments")
        option_3.config(
            command=lambda button=option_3: Scrape.sort_button(self, self.lst, 2, button))
        m_canvas.create_window(20, option_1.winfo_reqheight(), anchor=NW, window=top_frame)
        option_1.pack(side=LEFT)
        option_2.pack(side=LEFT)
        option_3.pack(side=LEFT)

        counter = 0
        button_heights = option_1.winfo_reqheight() + 25
        number_of_canvas_frames = 0
        print(self.lst)
        for i in self.lst:
            text_2 = StringVar()
            #print(self.lst)
            text_2.set(f'{i[0]}\n{i[1]}\n{i[2]} {i[3]}\n{i[-1]} Upvotes')
            #print(i[3])
            #main_frame = Frame(results, highlightthickness=2, bd=10, highlightbackground='red')
            frame_b = Frame(Scrape.results, bd=2, relief=SUNKEN)
            button = Button(frame_b, textvariable=text_2, highlightthickness=0, bd=0, wraplength=500, width=75)
            button.config(
                command=lambda button=button: Scrape.button_pressed(self, button, self.lst))  #Scrape.open_posts(self, lst,)
            #upvotes = Label(frame_b, text=f"{i[-1]} Upvotes", fg="orange")
            button.pack()
            #upvotes.pack()
            m_canvas.create_window(20, button_heights, anchor=NW, window=frame_b)
            counter += 1
            number_of_canvas_frames += 1
            m_canvas.update()
            button_heights += frame_b.winfo_reqheight()
            m_canvas.config(scrollregion=(0, 0, 300, button_heights))

    def search(self):
        tk.Button(text="Reddit", command=lambda: Scrape.checker(self, 'https://old.reddit.com/')).pack()

        #tk.Label(textvariable=text).pack()


Scrape().mainloop()
