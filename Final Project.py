# Created by: Landon Walker
# 13/6/2024
# Read from Reddit Program
# Version = '0.1'
# Program Description: Read and display data from reddit using a gui


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
        self.lst = []  # hold data from the website
        self.comments = []  # holds comments from the website
        self.geometry("400x400")  # window size
        self.search()  # calls the search function
        self.tracker = 0  # tracks the number of clicks
        self.selection = 0  # tracks the current selected mode
        self.setting = 0  # tracks the current selected index
        self.click_1 = 0  # tracks the number of clicks for sort 1
        self.click_2 = 0  # tracks the number of clicks for sort 2
        self.click_3 = 0  # tracks the number of clicks for sort 3
        self.check = 0  # checks which way to use the binary search

    # reads from reddit
    # @param self - holds the self functionality for the class
    # @param url - holds the reddit url
    # returns the r and soup variables to the calling function
    def read_reddit(self, url):
        r = requests.get(url)  # gets the data from the website
        soup = BeautifulSoup(r.content, 'html.parser')  # formats the data in r
        return r, soup

    # reads in data from the clicked post
    # @param self - holds the self functionality for the class
    # @param data - holds the list of values including post urls gathered
    # @param value - holds the index value of the clicked button
    def open_posts(self, data, value):
        #print(value)
        r, soup = Scrape.read_reddit(self, data[value][3])  # saves the data in r, soup from the read_reddit function
        #print(page)

    # The binary search that can find the location of a post with compatibility for multiple different sorting methods
    # @param self - holds the self functionality for the class
    # @param low - holds the lower range of the list
    # @param high - holds the upper range of the list
    # @param x - holds the index the binary search is trying to find
    # @param setting - holds the index depending on how the list is sorted
    # @return mid - returns the index of the value
    # @return Scrape.binary_search(self, low, mid - 1, x, setting) - runs the binary search with new parameters
    # @return Scrape.binary_search(self, mid + 1, high, x, setting) - runs the binary search with new parameters
    # @return -1 - returns a value to determine if the value was found
    def binary_search(self, low, high, x, setting):
        if self.check == 1:  # checks if the list is set to sort greatest to least
            if high >= low:  # checks if the upper range of the list is greater than the lower range of the list

                mid = (high + low) // 2  # determines the middle index value

                # If element is present at the middle itself
                if self.lst[mid][setting] == x[setting]:  # checks if x is at the middle value
                    return mid

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

                mid = (high + low) // 2  # determines the middle index value

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
    # sorts the list forwards on in reverse
    # @param self - holds the self functionality of the class
    # @param direction - The direction (forward or reverse) to sort the data
    # @param i_value - The index value to sort by
    def sorter(self, direction, i_value):
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
            return self.lst  # returns the sorted list to the main
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
            return self.lst  # returns the sorted list to the main

    # Determines while sort option is chosen and resorts the list.
    # @param self - Holds the self functionality of the class
    # @param data - NEEDS TO BE DELETED (USELESS)
    # @param i_value - NEEDS TO BE DELETED (useless)
    # @param option - holds the button
    def sort_button(self, option):
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
            #print(f"click 1 : {self.click_1}")
            self.check = 0  # sets the check to 0
            self.lst = Scrape.sorter(self, 0, self.setting)  # updates self.lst
            Scrape.new_window(self)  # creates a new window
        elif self.click_1 % 2 > 0:
            #print(f"click 1 : {self.click_1}")
            self.check = 1  # sets the check to 1
            self.lst = Scrape.sorter(self, 1, self.setting)  # updates self.lst
            Scrape.new_window(self)  # creates a new window
        elif self.click_2 % 2 == 0 and not self.click_2 == 0:
            #print(f"click 2 : {self.click_2}")
            self.check = 0  # sets the check to 0
            self.lst = Scrape.sorter(self, 0, self.setting)  # updates self.lst
            Scrape.new_window(self)  # creates a new window
        elif self.click_2 % 2 > 0:
            #print(f"click 2 : {self.click_2}")
            self.check = 1  # sets the check to 1
            self.lst = Scrape.sorter(self, 1, self.setting)  # updates self.lst
            Scrape.new_window(self)  # creates a new window
        elif self.click_3 % 2 == 0 and not self.click_3 == 0:
            #print(f"click 3 : {self.click_3}")
            self.check = 0  # sets the check to 0
            self.lst = Scrape.sorter(self, 0, self.setting)  # updates self.lst
            Scrape.new_window(self)  # creates a new window
        else:
            #print(f"click 3 : {self.click_3}")
            self.check = 1  # sets the check to 1
            self.lst = Scrape.sorter(self, 1, self.setting)  # updates self.lst
            Scrape.new_window(self)  # creates a new window

    # gets data from posts on reddit
    # @param self - holds the self functionality of the class
    # @param index - holds the index value
    def get_comments(self, index):
        self.comments = [[]]  # appends self.comments with an empty list
        r, soup = Scrape.read_reddit(self, self.lst[index][4])  # stores request in r and soup in soup
        rows = soup.find_all('div', {"class": "sitetable"})  # gets the table with the comments
        count = 0  # creates a count starting at 0
        while True:
            for i in rows:  # iterates through the table of comments
                try:
                    username = i.find("a", {"class": "author"}).text.strip()  # gets the usernames

                    text = i.find("div", {"class": "md"}).text.strip()  # gets the comment text

                    self.comments[count].append(username)  # appends the comment usernames
                    self.comments[count].append(text)  # appends the comment text
                    self.comments.append([])  # creates a new empty list in self.comments
                    count += 1  # increases count by 1

                except:
                    pass  # makes the loop run through again

            if not self.comments:  # checks if the list is empty
                time.sleep(.5)  # halts the program for .5 seconds
                return Scrape.checker(self, index)
            else:
                self.comments = [item for item in self.comments if
                                 item != []]  # checks for and deletes empty lists in the 2D list
                if not self.comments:  # checks if the list is empty
                    time.sleep(.5)  # halts the program for .5 seconds
                    return Scrape.checker(self, index)
                else:
                    break  # exits the loop
            break

        self.comment_window = Toplevel(self)  # creates a window for the comments
        Scrape.comment_new_window(self)  # runs the comment_new_window function

    # Utilizes the comment window to display comments
    # @param self - holds the self functionality of the program
    def comment_new_window(self):
        self.comment_window.geometry('600x500')  # the dimensions of the window
        heading = self.comment_window.title('Post Comments')  # window title

        self.m_canvas = Canvas(self.comment_window)  # creates a canvas for the comments
        self.m_canvas.config(width=600, height=500)  # dimensions of the canvas

        self.m_canvas.config(scrollregion=(0, 0, 300, 2700))  # Scroll area of the canvas

        y_axis = Scrollbar(self.comment_window)  # creates a y-axis scroll bar
        y_axis.config(command=self.m_canvas.yview)  # attaches the scroll bar to the canvas

        self.m_canvas.config(yscrollcommand=y_axis.set)  # sets the yscrollcommand to the scrollbar
        y_axis.pack(side=RIGHT, fill=Y)  # displays the y-axis
        self.m_canvas.pack(side=LEFT, expand=YES, fill=BOTH)  # displays the canvas
        top_frame = Frame(self.comment_window)  # creates a frame
        #sort_options = Label(top_frame, text="Sort by:")

        counter = 0  # creates a variable to hold a count
        button_heights = 25  # button heights starting value
        for i in self.comments:  # iterates through the 2D list of comments
            text_2 = StringVar()  # for holding text for display on frame
            # print(self.comments)
            text_2.set(f'{i[0]}\n"{i[1]}"')  # sets the text to hold values from the 2D list of comment data
            # print(i[3])
            # main_frame = Frame(comment_window, highlightthickness=2, bd=10, highlightbackground='red')
            frame_b = Frame(self.comment_window, bd=2, relief=SUNKEN)  # creates a new frame
            button = Button(frame_b, textvariable=text_2, highlightthickness=0, bd=0, wraplength=500,
                            width=75)  # creates buttons within frame_b
            button.pack()  # displays the button
            self.m_canvas.create_window(20, button_heights, anchor=NW, window=frame_b)  # creates a window in the canvas
            counter += 1  # increases the counter by 1
            self.m_canvas.update()  # updates the canvas
            button_heights += frame_b.winfo_reqheight()  # adds the height of the current button to the height of the total buttons
            self.m_canvas.config(scrollregion=(0, 0, 300, button_heights))  # sets the scroll region

    # Curates a list of data for use in the binary search upon the click of a button
    # @param self - holds the self functionality of the class
    # @param button - holds the button
    def button_pressed(self, button):
        options = (button.cget("text")).splitlines()  # gets the text of the button
        options_updated = [line.split() for line in options]  # stores option in a 2D list
        options_updated = [item for item in options_updated if item != []]  # deletes any empty lists in options_updated
        options_updated[-1].remove("Upvotes")  # removes text
        options_updated[-2].remove("comments")  # removes text
        options_updated[0] = ' '.join(options_updated[0])  # joins the values at the index
        options_updated[1] = ' '.join(options_updated[1])  # joins the values at the index
        options_updated[2] = ' '.join(options_updated[2])  # joins the values at the index
        options_updated[3] = ' '.join(options_updated[3])  # joins the values at the index
        for i in range(len(self.lst)):  # iterates through the len of self.lst
            self.lst[i][-1] = int(self.lst[i][-1])  # changes numbers from strings to integers
            self.lst[i][2] = int(self.lst[i][2])  # changes numbers from strings to integers
            options_updated[2] = int(options_updated[2])  # changes numbers from strings to integers
            options_updated[-1] = int(options_updated[-1])  # changes numbers from strings to integers

        result = Scrape.binary_search(self, 0, len(self.lst) - 1, options_updated,
                                      self.setting)  # stores the result of the binary search

        if result != -1:  # if results is not -1, an index was found
            print("Element is present at index", str(result))
            comment_display = Scrape.get_comments(self,
                                                  result)  # stores get_comments in a variable. Get comments retrieves comment data.
        else:  # -1 index returned. No result found
            print("Element is not present in array")

    # displays the posts from scraping reddit
    # @param self - holds the self functionality of the program
    def new_window(self):

        self.results.geometry('600x500')  # sets the dimensions of the window
        heading = self.results.title('Front of Reddit')  # stores the heading in a variable

        self.m_canvas = Canvas(self.results)  # creates a canvas
        self.m_canvas.config(width=600, height=500)  # sets the dimensions of the canvas

        self.m_canvas.config(scrollregion=(0, 0, 300, 2700))  # sets the scroll region of the canvas

        y_axis = Scrollbar(self.results)  # creates a scrollbar
        y_axis.config(command=self.m_canvas.yview)  # attaches the scrollbar to the canvas

        self.m_canvas.config(yscrollcommand=y_axis.set)  # sets y_axis to the yscrollcommand of the canvas
        y_axis.pack(side=RIGHT, fill=Y)  # displays y_axis
        self.m_canvas.pack(side=LEFT, expand=YES, fill=BOTH)  # displays canvas
        top_frame = Frame(self.results)  # creates a frame
        option_1 = Button(top_frame, text="Alphabetical")  # first sort option
        option_1.config(
            command=lambda button=option_1: Scrape.sort_button(self, button))  # calls sort_button function
        option_2 = Button(top_frame, text="Upvotes")  # second sort option
        option_2.config(
            command=lambda button=option_2: Scrape.sort_button(self, button))  # calls sort_button function
        option_3 = Button(top_frame, text="Comments")  # third sort option
        option_3.config(
            command=lambda button=option_3: Scrape.sort_button(self, button))  # calls sort_button function
        self.m_canvas.create_window(20, option_1.winfo_reqheight(), anchor=NW,
                                    window=top_frame)  # creates a window in the canvas
        option_1.pack(side=LEFT)  # displays the button
        option_2.pack(side=LEFT)  # displays the button
        option_3.pack(side=LEFT)  # displays the button

        counter = 0  # creates a counter starting at 0
        button_heights = option_1.winfo_reqheight() + 25  # stores the button heights with the heights of the sort buttons
        for i in self.lst:  # iterates through self.lst
            text_2 = StringVar()  # variable for displayin text
            text_2.set(f'{i[0]}\n{i[1]}\n{i[2]} {i[3]}\n{i[-1]} Upvotes')  # data to be displayed on the buttons
            frame_b = Frame(self.results, bd=2, relief=SUNKEN)  # creates a frame
            button = Button(frame_b, textvariable=text_2, highlightthickness=0, bd=0, wraplength=500,
                            width=75)  # creates a button within frame_b
            button.config(
                command=lambda button=button: Scrape.button_pressed(self, button))  # runs the button_pressed function
            button.pack()  # displays the button
            self.m_canvas.create_window(20, button_heights, anchor=NW, window=frame_b)  # creates a window in the canvas
            counter += 1  # increases the counter by 1
            self.m_canvas.update()  # updates the canvas
            button_heights += frame_b.winfo_reqheight()  # adds the current button height to the total heights
            self.m_canvas.config(scrollregion=(0, 0, 300, button_heights))  # updates the scroll region of the canvas

    # gets data from reddit
    # @param self - holds the self functionality of the class
    # @param url - holds the reddit url
    # @return Scrape.checker(self, url) - returns the checker function if a value is not present in self.lst
    def checker(self, url):
        self.lst.append([])  # adds an empty list to self.lst
        count = 0  # creates a counter variable
        r, soup = Scrape.read_reddit(self, url)  # stores the values from read_reddit in r and soup
        rows = soup.find_all('div', {"class": "link"})  # gets the table of posts from reddit
        time.sleep(.05)  # halts the program for .05 seconds
        while True:
            for i in rows:  # iterates through the data in rows
                try:
                    tagline = i.find("p", {"class": "tagline"}).text.strip()  # gets the tagline
                    comments = i.find("li", {"class": "first"}).text.strip()  # gets the comment count
                    page = i.find("a", {"class": "bylink"})  # gets the page
                    page_url = page["href"]  # gets the url from page
                    likes = i.find("div", {"class": "score"})  # gets the number of likes and other data
                    exact_likes = likes["title"]  # gets the exact value of likes from like

                    self.lst[count].append(
                        i.find("p", {"class": "title"}).text.strip())  # appends self.lst with the title
                    self.lst[count].append(f"\n{tagline}")  # appends self.lst with the tagline
                    self.lst[count].append(comments)  # appends self.lst with the comments count
                    self.lst[count].append(page_url)  # appends self.lst with the page url
                    self.lst[count].append(exact_likes)  # appends self.lst with the likes
                    count += 1  # increases the counter by 1
                    self.lst.append([])  # appends self.lst with an empty list
                except:
                    pass  # skips this iteration if an error is encountered

            # ensures the window always pulls up. Sometimes code can't get data fast enough for the list.
            if not self.lst:  # checks if self.lst is empty
                print(self.lst)
                time.sleep(.5)  # halts the program for .5 seconds

                return Scrape.checker(self, url)  # reruns the current function
            else:
                self.lst = [item for item in self.lst if item != []]  # deletes empty lists in self.lst
                if not self.lst:  # checks if self.lst is empty
                    time.sleep(.5)  # halts the program for .5 seconds
                    return Scrape.checker(self, url)  # reruns the current function
                else:
                    break  # exists the loop
        self.lst = Scrape.sorter(self, 0, 0)  # sorts self.lst greatest to least

        for i in range(len(self.lst)):  # iterates through the length of self.lst
            l = str(self.lst[i][2]).split()  # splits a value and store it in l
            self.lst[i][2] = l[0]  # replaces a value in self.lst with a value in l
            self.lst[i].insert(3, l[1])  # replaces a value in self.lst with a value in l

        self.results = Toplevel(self)  # creates a new window
        Scrape.new_window(self)  # runs the new_window function

    # button to run search reddit
    # @param self - holds the self functionality of the class

    def search(self):

        tk.Button(text="Reddit", command=lambda: Scrape.checker(self,
                                                                'https://old.reddit.com/')).pack()  # the button to
        # run the entire program


# main

Scrape().mainloop()
