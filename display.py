from tkinter import *
import paho.mqtt.client as mqtt
import json
from PIL import Image, ImageTk
import time
import utils
import os.path
from tinydb import TinyDB
import os, fnmatch

label_lunch_com_size = utils.config.get('display', 'label_lunch_com_size')
label_username = utils.config.get('display', 'label_username')
label_sec_ID = utils.config.get('display', 'label_sec_ID')
label_user_sec_ID = utils.config.get('display', 'label_user_sec_ID')
image_user_size = utils.config.get('display', 'image_user_size')
image_logo = utils.config.get('display', 'image_logo')

folder_loc = os.getcwd() + "/"
root = Tk()


def close_escape(event=None):
    print("\n ESCAPED")
    root.destroy()


# full screen
root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.bind("<Escape>", close_escape)

##############HEADER
# container
head = Frame(root, width=450, height=100, pady=3)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
head.grid(row=0, sticky="ew")

# logo
logo = Image.open(image_logo)
logo = logo.resize((200, 90), Image.ANTIALIAS)
l = ImageTk.PhotoImage(logo)
panel = Label(head, image=l, anchor='nw')
panel.image = logo
# panel.pack(side="bottom", fill="both", expand="yes")
panel.grid(row=0, column=0, sticky='nw')

# clock frame
clockframe = Frame(root, width=450, height=100, pady=3)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
clockframe.grid(row=0, sticky="e")

# time
clock = Label(clockframe, font=('times', 25, 'bold'), fg='blue')
clock.grid(row=0, column=1, sticky='ne')


def tick():
    s = time.strftime('%b %d, %Y\n%I:%M %p')
    if s != clock["text"]:
        clock["text"] = s
    clock.after(1000, tick)


tick()

#### header
logo = Image.open(folder_loc + 'logo.png')
logo = logo.resize((900, 200), Image.ANTIALIAS)
l = ImageTk.PhotoImage(logo)
panel = Label(head, image=l, anchor='nw')
panel.image = logo
# panel.pack(side="bottom", fill="both", expand="yes")
panel.grid(row=0, column=0, sticky='nw')

##body
# main container
center = Frame(root, width=300, height=300, padx=1)
center.grid(row=1, sticky="nsew")
center.grid_rowconfigure(0, weight=1)
center.grid_columnconfigure(1, weight=1)
# left side
ctr_left = Frame(center, width=300, height=300)
ctr_left.grid(row=0, column=0, sticky="ns")
# lunchpass = Label(ctr_left, text='Lunch Pass', font=('Tahoma', label_lunch_com_size))
# lunchpass['fg'] = 'gray80'
# lunchpass.grid(row=0, column=0, sticky='nsew')
# compass = Label(ctr_left, text="Commuter's Pass", font=('Tahoma', label_lunch_com_size))
# compass['fg'] = 'gray80'
# compass.grid(row=1, column=0, sticky='nsew')
# pic container
picframe = Frame(ctr_left, width=image_user_size, height=image_user_size)
picframe.grid(row=2, column=0, sticky="ns", pady=10, padx=10)
# pic
size = picframe.winfo_reqwidth(), picframe.winfo_reqheight()
im_temp = Image.open(folder_loc + 'user.png')
im_temp = im_temp.resize((size), Image.ANTIALIAS)
user = ImageTk.PhotoImage(im_temp)
panel = Label(picframe, image=user, anchor='nw')
panel.image = im_temp
panel.grid(row=0, sticky='nw')
# center
ctr_mid = Frame(center, width=250, height=190, padx=3, pady=3)
ctr_mid.grid(row=0, column=1, sticky="nsew")
space = Frame(ctr_mid, width=250, height=100, padx=3, pady=3)
space.grid(row=1, column=1, sticky="nsew")

# username
usrnme = Label(ctr_mid, font=("Georgia", label_username))
uname = usrnme['text'] = "Full Name"
usrnme.grid(row=2, column=1, columnspan=2, sticky='w')
# section
sec = Label(ctr_mid, text='', font=('Tahoma', label_sec_ID))
sec.grid(row=3, column=1, sticky='w')
section = Label(ctr_mid, font=('Tahoma', label_user_sec_ID))
section['text'] = ""
section.grid(row=4, column=1, sticky='ns')
# ID number
nID = Label(ctr_mid, text='ID Number:', font=('Tahoma', label_sec_ID))
nID.grid(row=5, column=1, sticky='w')
idnum = Label(ctr_mid, font=('Tahoma', label_user_sec_ID))
idnum['text'] = "ID Number"
idnum.grid(row=6, column=1, sticky='ns')


def change_image(avatar):
    # print(avatar)
    im_temp = Image.open(avatar)
    im_temp = im_temp.resize((size), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(im_temp)
    img2 = ImageTk.PhotoImage(im_temp)
    panel.configure(image=img2)
    panel.image = img2


def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def display_student(student, direction):
    data = student
    try:
        image = find(student['user_id'] + "*", 'images/')[0]
    except:
        image = folder_loc + "user.png"

    if image:
        avatar = folder_loc + image
    else:
        avatar = folder_loc + "user.png"
    if data["name"]:
        usrnme["text"] = data["name"]
    else:
        usrnme["text"] = ""
    if data["user_id"]:
        idnum["text"] = data["user_id"]
    else:
        idnum["text"] = ""

    if direction:
        section["text"] = "**** " + direction + " ****"
    else:
        section["text"] = ""
    change_image(avatar)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("tele/+/SENSOR")


def on_message(client, userdata, message):
    tmp_data = str(message.topic).split("/")
    device = str(tmp_data[1]).split("-")[0]
    payload = json.loads(message.payload)
    active_employee = None
    direction = ''
    key = utils.find_device(device)

    db = TinyDB(os.path.abspath(utils.path_name) + '/employees.json')
    employees = db.all()
    for employee in employees:
        if employee['attendance_device_id']:
            if str(payload['hex_code']).strip() in str(employee['attendance_device_id']):
                if str(key[1]).strip() == "None":
                    direction = str(employee['company'])
                else:
                    direction = str(key[1]).strip()
                active_employee = employee
                break

    if active_employee:
        display_student(active_employee, direction)


client = mqtt.Client()
client.username_pw_set(username=str(utils.config.get("mqtt", "username")).strip(),
                       password=str(utils.config.get("mqtt", "password")).strip())
client.on_connect = on_connect
client.on_message = on_message
client.connect(str(utils.config.get("mqtt", "url")).strip(), 1883, 60)
client.loop_start()

root.bind("<Return>", change_image)
root.mainloop()
