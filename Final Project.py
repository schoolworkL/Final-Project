import tkinter as tk
from tkinter import *
import requests
from bs4 import BeautifulSoup
import time


class Scrape(tk.Tk):
    # The holders of the self functionality and of all very important variables, including the starting frame
    def __init__(self):
        super().__init__()
        frame = tk.Frame(master=self)
        frame.pack()
        self.lst = []
        self.comments = []
        self.geometry("400x400")
        self.search()
        self.tracker = 0
        self.selection = 0
        self.setting = 0
        self.click_1 = 0
        self.click_2 = 0
        self.click_3 = 0
        self.check = 0

    # reads from reddits
    # @param self - holds the self functionality for the class
    # @param url - holds the reddit url
    # returns the r and soup variables to the calling function
    def read_reddit(self, url):
        r = requests.get(url)  # gets the data from the website
        soup = BeautifulSoup(r.content, 'html.parser')  # formats the data in r
        return r, soup  # returns r and soup to the calling function

    # reads in data from the clicked post
    # @param self - holds the self functionality for the class
    # @param data - holds the list of values including post urls gathered
    # @param value - holds the index value of the clicked button
    def open_posts(self, data, value):
        print(value)
        r, soup = Scrape.read_reddit(self, data[value][3])  # saves the data in r, soup from the read_reddit function
        #print(page)
    # The binary search that can find the location of a post with compatiblity for multiple different sorting methods
    # @param self - holds tehe self functionality for the class
    # @param low - holds the lower range of the list
    # @param high - holds the upper range of the list
    # @param x - holds the index the binary search is trying to find
    # @param setting - holds the index depending on how the list is sorted
    # @return mid - returns the index of the value
    # @return return Scrape.binary_search(self, low, mid - 1, x, setting) - runs the binary search with new parameters
    # @return Scrape.binary_search(self, mid + 1, high, x, setting) - reuns the binary search with new parameters
    # @return -1 - returns a value to determine if the value was found
    def binary_search(self, low, high, x, setting):
        #print(f'hi {x}')
        #print(f'Joe: {setting}')
        # Check base case
        #print(f'option: {x}')
        #print(f'setting {setting}')
        if self.check == 1:  # checks if the list is set to sort greatest to least
            if high >= low:  # checks if the upper range of the list is greater than the lower range of the list

                mid = (high + low) // 2  # determines the middle index value

                # If element is present at the middle itself
                if self.lst[mid][setting] == x[setting]:  # checks if x is at the middle value
                    return mid  # returns index of the mid

                # If element is smaller than mid, then it can only
                # be present in left subarray
                elif self.lst[mid][setting] > x[setting]:  # checks if the x[setting] is lesser than the mid[setting]
                    return Scrape.binary_search(self, low, mid - 1, x, setting)

                # Else the element can only be present in right subarray
                else:  # x[setting] is greater the mid[setting] value
                    return Scrape.binary_search(self, mid + 1, high, x, setting)

            else:
                # Element is not present in the array
                return -1
        else:
            if high >= low:  # checks if the upper range of the list is greater than the lower range of the list

                mid = (high + low) // 2

                # If element is present at the middle itself
                if self.lst[mid][setting] == x[setting]:  # checks if x is at the middle value
                    return mid

                # If element is smaller than mid, then it can only
                # be present in left subarray
                elif x[setting] > self.lst[mid][setting]:  # checks if the x[setting] is lesser than the mid[setting]
                    return Scrape.binary_search(self, low, mid - 1, x, setting)

                # Else the element can only be present in right subarray
                else:  # x[setting] is greater the mid[setting] value
                    return Scrape.binary_search(self, mid + 1, high, x, setting)

            else:
                # Element is not present in the array
                return -1

    # sorts the list forwards or in reverse and based on an index value
    # @param self - holds the self functionality of the class
    # @param lst - holds the lst (redundant)
    # @param direction - holds the direction (forward or reverse) the lst will be sorted
    # @param i_value - holds the index the lst will be sorting around
    def sorter(self, lst, direction, i_value):
        if direction == 1:  # least to greatest sort
            for i in range(len(self.lst) - 1, 0, -1):  # iterates through the list backwards
                value = 0  # variable to the second value
                for j in range(1, i + 1):  # iterates through the list using i+1 as the end range
                    if self.lst[j][i_value] > self.lst[value][
                        i_value]:  # checks if the second value in the tuple is greater than the second value in the second
                        # tuple
                        value = j  # sets value to equal j
                self.lst[j], self.lst[value] = self.lst[value], self.lst[
                    j]  # switches the values of list[j] and list[value]
            # self.lst = lst
            #return self.lst  # returns the sorted list to the main
        else:  # greatest to the least sort
            for i in range(len(self.lst) - 1, 0, -1):  # iterates through the list backwards
                value = 0  # variable to the second value
                for j in range(1, i + 1):  # iterates through the list using i+1 as the end range
                    if self.lst[j][i_value] < self.lst[value][
                        i_value]:  # checks if the second value in the tuple is greater than the second value in the second
                        # tuple
                        value = j  # sets value to equal j
                self.lst[j], self.lst[value] = self.lst[value], self.lst[
                    j]  # switches the values of list[j] and list[value]
            # self.lst = lst
            #return self.lst  # returns the sorted list to the main

    # Determines while sort option is chosen and resorts the list.
    # @param self - Holds the self functionality of the class
    # @param data - NEEDS TO BE DELETED (USELESS)
    # @param i_value - NEEDS TO BE DELETED (useless)
    # @param option - holds the button
    def sort_button(self, data, i_value, option):
        value = str(option.cget("text"))  # holds the text of the button
        for widget in self.results.winfo_children():  # checks each child in the results window
            widget.destroy()  # destroys the previous displayed frames
        if value == "Alphabetical":  # checks if "Alphabetical" is the button text
            self.setting = 0  # index to sort by set to 0
            self.click_1 += 1  # tracks how many times in a row this option was clicked
            self.click_2 = 0  # option 2 set to 0 clicks in a row
            self.click_3 = 0  # option 3 set to 0 clicks in a row
        elif value == "Upvotes":  # checks if "Upvotes" is the button text
            self.setting = -1  # index to sort by set to -1
            self.click_1 = 0  # option 3 set to 0 clicks in a row
            self.click_2 += 1  # tracks how many times in a row this option was clicked
            self.click_3 = 0  # option 3 set to 0 clicks in a row
        else:  # only one other option the text could be (Comments)
            self.setting = 2  # index to sort by set to 2
            self.click_1 = 0  # option 1 set to 0 clicks in a row
            self.click_2 = 0  # option 2 set to 0 clicks in a row
            self.click_3 += 1  # tracks how many times in a row this option was clicked

        if self.click_1 % 2 == 0 and not self.click_1 == 0:  # checks if buttons has been clicked 2 times and is not the first click
            print(f"click 1 : {self.click_1}")
            self.check = 0  # sets the check to 0
            self.lst = Scrape.sorter(self, data, 0, self.setting)  # updates self.lst

            #for i in self.lst:
            #    print(i)
            #print(self.lst)
            Scrape.new_window(self)  # creates a new window
        elif self.click_1 % 2 > 0:  # checks that the remainder of clicks is greater than 1
            print(f"click 1 : {self.click_1}")
            self.check = 1  # sets the check to 1
            self.lst = Scrape.sorter(self, data, 1, self.setting)  # updates self.lst
            #for i in self.lst:
            #    print(i)
            #print(self.lst)
            Scrape.new_window(self)  # creates a new window
        elif self.click_2 % 2 == 0 and not self.click_2 == 0:  # checks if buttons has been clicked 2 times and is not the first click
            print(f"click 2 : {self.click_2}")
            self.check = 0  # sets the check to 0
            self.lst = Scrape.sorter(self, data, 0, self.setting)  # updates self.lst
            #for i in self.lst:
            #    print(i[-1])
            Scrape.new_window(self)  # creates a new window
        elif self.click_2 % 2 > 0:  # checks that the remainder of clicks is greater than 1
            print(f"click 2 : {self.click_2}")
            self.check = 1  # sets the check to 1
            self.lst = Scrape.sorter(self, data, 1, self.setting)  # updates self.lst
            #for i in self.lst:
            #    print(i[-1])
            Scrape.new_window(self)  # creates a new window
        elif self.click_3 % 2 == 0 and not self.click_3 == 0:  # checks if buttons has been clicked 2 times and is not the first click
            print(f"click 3 : {self.click_3}")
            self.check = 0  # sets the check to 0
            self.lst = Scrape.sorter(self, data, 0, self.setting)  # updates self.lst
            #for i in self.lst:
            #    print(i[2])
            Scrape.new_window(self)  # creates a new window
        else:  # checks that the remainder of clicks is greater than 1
            print(f"click 3 : {self.click_3}")
            self.check = 1  # sets the check to 1
            self.lst = Scrape.sorter(self, data, 1, self.setting)  # updates self.lst
            #for i in self.lst:
            #    print(i[2])
            Scrape.new_window(self)  # creates a new window
            
    def get_comments(self, index):
        #print(self.lst)
        self.comments = [[]]
        r, soup = Scrape.read_reddit(self, self.lst[index][4])
        #print(self.lst[index][4])
        rows = soup.find_all('div', {"class": "sitetable"})
        #print(rows)
        count = 0
        while True:
            for i in rows:
                try:
                    username = i.find("a", {"class": "author"}).text.strip()

                    text = i.find("div", {"class": "md"}).text.strip()

                    #likes = i.find("div", {"class": "midcol"})
                    #print(likes)

                    self.comments[count].append(username)
                    self.comments[count].append(text)
                    self.comments.append([])
                    count += 1

                    tagline = i.find("p", {"class": "tagline"}).text.strip()
                    comments = i.find("li", {"class": "first"}).text.strip()
                    page = i.find("a", {"class": "bylink"})
                    page_url = page["href"]
                    likes = i.find("div", {"class": "score"})
                    exact_likes = likes["title"]
                    #print(tagline)
                    #print(comments)
                    #print(page_url)
                    #self.lst[count].append(i.find("p", {"class": "title"}).text.strip())
                    #self.lst[count].append(f"\n{tagline}")
                    #self.lst[count].append(comments)
                    #self.lst[count].append(page_url)
                    #self.lst[count].append(exact_likes)
                    #count += 1
                    #self.lst.append([])
                except:
                    pass
            if not self.comments:
                print(self.comments)
                time.sleep(.5)
                return Scrape.checker(self, index)
            else:
                self.comments = [item for item in self.comments if item != []]
                # if not self.lst:
                print(self.comments)
                # return Scrape.checker(self, url)

                print(self.comments)
                self.comments = [item for item in self.comments if item != []]
                break

            break
        self.comment_window = Toplevel(self)
        Scrape.comment_new_window(self)
    def comment_new_window(self):
        self.comment_window.geometry('600x500')
        heading = self.comment_window.title('Front of Reddit')

        self.m_canvas = Canvas(self.comment_window)
        self.m_canvas.config(width=600, height=500)

        self.m_canvas.config(scrollregion=(0, 0, 300, 2700))

        y_axis = Scrollbar(self.comment_window)
        y_axis.config(command=self.m_canvas.yview)

        self.m_canvas.config(yscrollcommand=y_axis.set)
        y_axis.pack(side=RIGHT, fill=Y)
        self.m_canvas.pack(side=LEFT, expand=YES, fill=BOTH)
        top_frame = Frame(self.comment_window)
        sort_options = Label(top_frame, text="Sort by:")

        counter = 0
        button_heights = 25
        number_of_canvas_frames = 0
        #print(self.comments)
        for i in self.comments:
            text_2 = StringVar()
            # print(self.comments)
            text_2.set(f'{i[0]}\n"{i[1]}"')
            # print(i[3])
            # main_frame = Frame(comment_window, highlightthickness=2, bd=10, highlightbackground='red')
            frame_b = Frame(self.comment_window, bd=2, relief=SUNKEN)
            button = Button(frame_b, textvariable=text_2, highlightthickness=0, bd=0, wraplength=500, width=75)
            button.config(
                command=lambda button=button: Scrape.button_pressed(self, button,
                                                                    self.comments))  # Scrape.open_posts(self, lst,)
            # upvotes = Label(frame_b, text=f"{i[-1]} Upvotes", fg="orange")
            button.pack()
            # upvotes.pack()
            self.m_canvas.create_window(20, button_heights, anchor=NW, window=frame_b)
            counter += 1
            number_of_canvas_frames += 1
            self.m_canvas.update()
            button_heights += frame_b.winfo_reqheight()
            self.m_canvas.config(scrollregion=(0, 0, 300, button_heights))
    def button_pressed(self, button, lst):
        options = (button.cget("text")).splitlines()
        #print(options)
        options_updated = [line.split() for line in options]
        options_updated = [item for item in options_updated if item != []]
        options_updated[-1].remove("Upvotes")
        options_updated[-2].remove("comments")
        options_updated[0] = ' '.join(options_updated[0])
        options_updated[1] = ' '.join(options_updated[1])
        options_updated[2] = ' '.join(options_updated[2])
        options_updated[3] = ' '.join(options_updated[3])
        #print(options_updated)
        #print(self.setting)
        #options_updated[2] = int(options_updated[2])
        #options_updated[-1]
        for i in range(len(self.lst)):
            self.lst[i][-1] = int(self.lst[i][-1])
            self.lst[i][2] = int(self.lst[i][2])
            options_updated[2] = int(options_updated[2])
            options_updated[-1] = int(options_updated[-1])

        result = Scrape.binary_search(self, 0, len(lst) - 1, options_updated, self.setting)

        if result != -1:
            print("Element is present at index", str(result))
            #print(lst[result])
            comment_display = Scrape.get_comments(self, result)
        else:
            #for i in self.lst:
            #print(i[-1])
            print("Element is not present in array")

    def new_window(self):

        self.results.geometry('600x500')
        heading = self.results.title('Front of Reddit')

        self.m_canvas = Canvas(self.results)
        self.m_canvas.config(width=600, height=500)

        self.m_canvas.config(scrollregion=(0, 0, 300, 2700))

        y_axis = Scrollbar(self.results)
        y_axis.config(command=self.m_canvas.yview)

        self.m_canvas.config(yscrollcommand=y_axis.set)
        y_axis.pack(side=RIGHT, fill=Y)
        self.m_canvas.pack(side=LEFT, expand=YES, fill=BOTH)
        top_frame = Frame(self.results)
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
        self.m_canvas.create_window(20, option_1.winfo_reqheight(), anchor=NW, window=top_frame)
        option_1.pack(side=LEFT)
        option_2.pack(side=LEFT)
        option_3.pack(side=LEFT)

        counter = 0
        button_heights = option_1.winfo_reqheight() + 25
        number_of_canvas_frames = 0
        print(self.lst)
        for i in self.lst:
            text_2 = StringVar()
            # print(self.lst)
            text_2.set(f'{i[0]}\n{i[1]}\n{i[2]} {i[3]}\n{i[-1]} Upvotes')
            # print(i[3])
            # main_frame = Frame(results, highlightthickness=2, bd=10, highlightbackground='red')
            frame_b = Frame(self.results, bd=2, relief=SUNKEN)
            button = Button(frame_b, textvariable=text_2, highlightthickness=0, bd=0, wraplength=500, width=75)
            button.config(
                command=lambda button=button: Scrape.button_pressed(self, button,
                                                                    self.lst))  # Scrape.open_posts(self, lst,)
            # upvotes = Label(frame_b, text=f"{i[-1]} Upvotes", fg="orange")
            button.pack()
            # upvotes.pack()
            self.m_canvas.create_window(20, button_heights, anchor=NW, window=frame_b)
            counter += 1
            number_of_canvas_frames += 1
            self.m_canvas.update()
            button_heights += frame_b.winfo_reqheight()
            self.m_canvas.config(scrollregion=(0, 0, 300, button_heights))

    def checker(self, url):
        self.lst.append([])
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
                time.sleep(.5)
                self.lst.clear()
                return Scrape.checker(self, url)
            else:
                self.lst = [item for item in self.lst if item != []]
                #if not self.lst:
                #print(self.lst)
                    #return Scrape.checker(self, url)

                print(self.lst)
                #self.lst = [item for item in self.lst if item != []]
                break
        self.lst = Scrape.sorter(self, self.lst, 0, 0)  # sorts list least to greatest
        #self.lst = Scrape.sorter(self, self.lst, 1, 0)  # sorts list least to greatest

        for i in range(len(self.lst)):
            l = str(self.lst[i][2]).split()
            self.lst[i][2] = l[0]
            self.lst[i].insert(3, l[1])
            #print(self.lst[i][2])

        self.results = Toplevel(self)
        Scrape.new_window(self)

    def search(self):

        tk.Button(text="Reddit", command=lambda: Scrape.checker(self, 'https://old.reddit.com/')).pack()


        #tk.Label(textvariable=text).pack()


Scrape().mainloop()
