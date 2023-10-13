# author: Chris Ian Fiel v1
from Tkinter import *
from PIL import Image, ImageTk
from subprocess import call
import memcache
import json
import os
from db import *
from pykeyboard import PyKeyboard


class App(object):
    def __init__(self):
        self.root = Tk()
        self.id_number = ""
        # self.root.attributes('-zoomed', True)
        self.name_label = Label(self.root, text="**********")
        self.level_label = Label(self.root, text="**********")
        self.section_label = Label(self.root, text="**********")
        self.id_number_label = Label(self.root, text="**********")
        self.time_label = Label(self.root, text="**********")
        self.status_label = Label(self.root, text="**********")

        self.id_number_label.grid(row=0, sticky=E)
        self.name_label.grid(row=1, sticky=E)
        self.level_label.grid(row=2, sticky=E)
        self.section_label.grid(row=3, sticky=E)
        self.status_label.grid(row=4, sticky=E)
        self.time_label.grid(row=5, sticky=E)

        self.image = Image.open("{0}/default.png".format(os.path.dirname(os.path.abspath(__file__)))).resize((300, 300))
        self.photo = ImageTk.PhotoImage(self.image)
        self.label = Label(image=self.photo)
        self.label.image = self.photo
        self.label.grid(row=0, column=2, rowspan=6)
        self._poll_job_id = self.poll()

    def poll(self):
        shared = memcache.Client(['127.0.0.1:11211'], debug=0)
        if shared.get('connection'):
            try:
                con_message = json.loads(shared.get('connection'))
                text = con_message['status'] + '/' + con_message['school_name'] + '/' + con_message['school_year'] + '/' + con_message['kind']
            except:
                text = 'OFFLINE' + '/' + school_name + '/' + school_year + '/' + kind
            self.status_label.config(text=text)
        else:
            text = 'OFFLINE' + '/' + school_name + '/' + school_year + '/' + kind
            self.status_label.config(text=text)

        if shared.get('message'):
            messages = json.loads(shared.get('message'))

            try:
                msg_id_number = messages['id_number']
            except:
                msg_id_number = ""

            if self.id_number != msg_id_number:
                call(["xdotool", "key", "1"])

                self.id_number = messages['id_number']

                try:
                    status = messages['status']
                except:
                    status = "INVALID"

                if status == "VALID":
                    try:
                        self.name_label.config(text=messages['name'])
                    except:
                        print "error"
                    try:
                        self.id_number_label.config(text=messages['id_number'])
                    except:
                        print "error"
                    try:
                        self.level_label.config(text=messages['level'])
                    except:
                        print "error"
                    try:
                        self.section_label.config(text=messages['section'])
                    except:
                        print "error"
                    try:
                        self.image = Image.open(messages['id_picture']).resize((300, 300))
                    except:
                        self.image = Image.open('{0}/default.png'.format(os.path.dirname(os.path.abspath(__file__)))).resize((300, 300))

                    self.photo = ImageTk.PhotoImage(self.image)
                    self.label.config(image=self.photo)
                    self.label.image = self.photo
                else:
                    self.name_label.config(text="**********")
                    self.id_number_label.config(text="**********")
                    self.level_label.config(text="**********")
                    self.section_label.config(text="**********")
                    self.image = Image.open('{0}/default.png'.format(os.path.dirname(os.path.abspath(__file__)))).resize((300, 300))
                    self.photo = ImageTk.PhotoImage(self.image)
                    self.label.config(image=self.photo)
                    self.label.image = self.photo
                    self.id_number = ""

        self.time_label.config(text=get_time().strftime('%b %d, %Y %I:%M:%S %p'))
        self._poll_job_id = self.root.after(500, self.poll)

    def stop(self):
        self.root.after_cancel(self._poll_job_id)
        self.cancel.configure(text='Go', command=self.go)

    def go(self):
        self.cancel.configure(text='Stop', command=self.stop)
        self._poll_job_id = self.poll()


app = App()
app.root.mainloop()
