from tkinter import *
from datetime import datetime, timedelta
from PIL import ImageTk, Image

w = Tk()
w.geometry('1366x768')
w.minsize(750, 200)
w.title("Digital Clock")

#background
background_image_path = "/home/manya/clobg.png" #add your image path for custom background
img1 = Image.open(background_image_path)
img2 = ImageTk.PhotoImage(img1)
Label(w, image=img2).place(x=-2, y=0)

global switcher
switcher = 12

f1 = Frame(w, width=750, height=200, bg='#0e1013',highlightbackground="white")
f1.pack(expand=True)

#creating global labels for additional display info
l1 = Label(f1, font=('Century Gothic', 55), bg='#0e1013', foreground='#d3d3d3')
l1.place(x=275, y=45)

ltimer = Label(f1,font = ('Century Gothic', 55), bg='#0e1013', foreground='#d3d3d3')
ltimer.place(x=275, y=45)


date_label = Label(f1, font=('Century Gothic', 15), bg='#0e1013', fg='#bcbcbc')
date_label.place(x=275, y=10)


#creating global labels for time
l2 = Label(f1, font=('Century Gothic', 50), bg='#0e1013', fg='#7f7f7f', text='DAY')
l2.place(x=70, y=45)

l1_12 = Label(f1, font=('Century Gothic', 55), bg='#0e1013', foreground='#bcbcbc')
l1_12.place(x=275, y=45)

l1_24 = Label(f1, font=('Century Gothic', 55), bg='#0e1013', foreground='#bcbcbc')
l1_24.place(x=275, y=45)

#storing function id to stop flickering of time display
global scheduled_function_id
scheduled_function_id = None

def time_12_hour():
    current_time = datetime.now().strftime('%I : %M : %S')  
    l1.config(text=current_time)
    global scheduled_function_id
    scheduled_function_id = l1.after(1000, time_12_hour)

def time_24_hour():
    current_time = datetime.now().strftime('%H : %M : %S')  
    l1.config(text=current_time)
    global scheduled_function_id
    scheduled_function_id = l1.after(1000, time_24_hour)

def timer_countdown():
    remaining_time = timer_end_time - datetime.now()
    if remaining_time.total_seconds() > 0:
        timer_str = remaining_time.total_seconds()
        ltimer.config(text="           "+str(int(timer_str))+"              ")
        ltimer.after(1000, timer_countdown)
    else:
        switch_to_clock()
        ltimer.config(text="")
        lsec.config(text="")

def start_timer():
    global timer_end_time

    try:
        timer_seconds = int(timer_entry.get())
        if timer_seconds > 0:
            timer_end_time = datetime.now() + timedelta(seconds=timer_seconds)
            switch_to_timer()
            timer_countdown()
        else:
            l1.config(text="Invalid value")
    except ValueError:
        l1.config(text="Invalid value")


def switch_mode():
    global switcher
    if switcher == 12:
        switcher = 24
    else:
        switcher = 12
    switch_to_clock()


def switch_to_clock():
    if scheduled_function_id:
        l1.after_cancel(scheduled_function_id)
    current_day_abbreviation = datetime.today().strftime('%A')[:3].upper()
    mode.set("Clock")

    if switcher == 12:
        time_12_hour()
    elif switcher == 24:
        time_24_hour()
        
    l2.config(text=current_day_abbreviation + " |")
    l3.config(text='DAY')
    l4.config(text='HOURS')
    l5.config(text='MINUTES')
    labels() 

def switch_to_timer():
    mode.set("Timer")
    l2.config(text="TIMER |")
    l3.config(text='       ')
    l4.config(text='             ') 
    global lsec
    lsec = Label(f1, font=('Century Gothic', 8), bg='#0e1013', fg='#7f7f7f', text='  SECONDS LEFT')
    lsec.place(x=500,y=130)
    l5.config(text='               ')

def labels():
    global l3, l4, l5
    l3 = Label(f1, font=('Century Gothic', 8), bg='#0e1013', fg='#7f7f7f', text='HOURS')
    l3.place(x=305, y=130)

    l4 = Label(f1, font=('Century Gothic', 8), bg='#0e1013', fg='#7f7f7f', text='MINUTES')
    l4.place(x=445, y=130)

    l5 = Label(f1, font=('Century Gothic', 8), bg='#0e1013', fg='#7f7f7f', text='SECONDS')
    l5.place(x=615, y=130)

def update_date():
    current_date = datetime.today().strftime('%B %d, %Y')
    date_label.config(text=current_date)
    date_label.after(1000 * 60 * 60 * 24, update_date) #update each day

#update date
update_date()

#label creations
labels()

#timer labels
timer_entry_label = Label(f1, font=('Century Gothic', 12), bg='#0e1013', fg='#7f7f7f', text='SET TIMER (SECONDS):')
timer_entry_label.place(x=10, y=160)

timer_entry = Entry(f1, font=('Century Gothic', 8), bg='#0e1013', fg='#d3d3d3', width=8)
timer_entry.place(x=200, y=160)

start_timer_button = Button(f1, text="Start Timer", command=start_timer, font=('Century Gothic', 8), bg='#7f7f7f', fg='#0e1013')
start_timer_button.place(x=300, y=160)

switch_mode_button = Button(f1, text="Switch Mode", command=switch_mode, font=('Century Gothic', 8), bg='#7f7f7f', fg='#0e1013')
switch_mode_button.place(x=640, y=160)

#current mode
global mode
mode = StringVar()
mode.set("Clock")

switch_to_clock()

w.mainloop()
