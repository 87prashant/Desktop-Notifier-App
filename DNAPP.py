import requests   #The requests module allows you to send HTTP requests using Python
import bs4   # Beautiful Soup is a Python library for pulling data out of HTML and XML files
import tkinter as tk   #Tkinter in Python is used to create Graphical User interfaces (GUIs)
import plyer   #Plyer is a platform-independent api to use features commonly found on various platforms, in Python.
import time   #This module provides various time-related functions
import threading   # threading module is used for creating, controlling and managing threads in python


# get html data of website
def get_html_data(url):
    data = requests.get(url)
    return data


# parsing html and extracting data
def get_corona_detail_of_india():
    url = "https://www.worldometers.info/coronavirus/country/india/"
    html_data = get_html_data(url)
    bs = bs4.BeautifulSoup(html_data.text, 'html.parser')
    info_div=bs.find("div",class_="content-inner").find_all("div",id="maincounter-wrap")
    all_details=""
    for i in info_div[0:3]:
        count=i.find("span").get_text()
        text=i.find("h1").get_text()
        all_details+=text + " : " + count + "\n"
    return all_details
    
# function use to  reload the data from website
def refresh():
    newdata = get_corona_detail_of_india()
    print("Refreshing..")
    mainLabel['text'] = newdata


# function for notifying...
def notify_me():
    while True:
        plyer.notification.notify(
            title="COVID 19 cases of INDIA",
            message=get_corona_detail_of_india(),
            timeout=5,
            app_icon='icon.ico'
        )
        time.sleep(5)


# creating gui:
root = tk.Tk()
root.geometry("900x800")
root.iconbitmap(None)
root.title("CORONA DATA TRACKER - INDIA")
root.configure(background='white')
f = ("poppins", 25, "bold")
banner = tk.PhotoImage(file="banner.png")
bannerLabel = tk.Label(root, image=banner)
bannerLabel.pack()
mainLabel = tk.Label(root, text=get_corona_detail_of_india(), font=f, bg='white')
mainLabel.pack()

reBtn = tk.Button(root, text="REFRESH", font=f, relief='solid', command=refresh)
reBtn.pack()

# create a new thread
th1 = threading.Thread(target=notify_me)
th1.setDaemon(True)
th1.start()

root.mainloop()
