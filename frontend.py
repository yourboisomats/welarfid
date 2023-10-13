
# -*- coding: utf-8 -*-
from Tkinter import *
import tkFont
from PIL import Image, ImageTk
from subprocess import call
from db import *

# common variables

label_font = None
name_font = None
value_font = None
status_font = None
time_font = None
image_width = None
lunch_font = None
commuter_font = None
distance = None


class ImageLabel(Frame):
    def __init__(self, master, filename):
        Frame.__init__(self, master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.master = master
        self.original = Image.open(filename).resize((300, 300))
        self.image = ImageTk.PhotoImage(self.original)
        self.display = Canvas(self, bd=0, highlightthickness=0)
        self.display.create_image(0, 0, image=self.image, anchor='nw', tags="IMG")
        self.display.pack(fill='both', expand=1)
        self.bind("<Configure>", self.resize)

    def resize(self, event):
        if event.width > event.height:
            size = (event.height, event.height)
            image_width = event.height
        else:
            size = (event.width, event.width)
            image_width = event.width

        resized = self.original.resize(size, Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(resized)
        self.display.delete("IMG")
        self.display.create_image(0, 0, image=self.image, anchor='nw', tags="IMG")
        self.display.configure(width=image_width, height=image_width)

    def resize2(self):

        #somewidget.winfo_width()
        #somewidget.winfo_height()

        if self.display.winfo_width() > self.display.winfo_height():
            size = (self.display.winfo_height(), self.display.winfo_height())
            image_width = self.display.winfo_height()
        else:
            size = (self.display.winfo_width(), self.display.winfo_width())
            image_width = self.display.winfo_width()

        resized = self.original.resize(size, Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(resized)
        self.display.delete("IMG")
        self.display.create_image(0, 0, image=self.image, anchor='nw', tags="IMG")
        self.display.configure(width=image_width, height=image_width)


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.resize = 1
        self.grid()
        self.master.title("Wela RFID")
        self.id_number = ""

        for r in range(16):
            self.master.rowconfigure(r, weight=1)

        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=distance)

        self.label_Font = label_font
        self.name_Font = name_font
        self.value_Font = value_font
        self.status_Font = status_font
        self.time_Font = time_font
        self.lunch_font = lunch_font
        self.commuter_font = commuter_font

        # pad frame
        Frame(master).grid(row=1, rowspan=2, column=1, sticky='wens')
        #Frame(master).grid(row=1, column=1, sticky='wens')

        # id
        id_number_label_x = Frame(master, relief=SUNKEN)
        id_number_label_x.grid(row=3, column=1, sticky='wens')
        self.id_number_label_y = Label(id_number_label_x, text="ID #:", font=self.label_Font, anchor='w').pack(
            fill='both', expand=1)
        id_number_frame = Frame(master)
        id_number_frame.grid(row=4, column=1, sticky='wens',pady=10)
        self.id_number_label = Label(id_number_frame, text="x-x-x-x", font=self.value_Font, anchor='w', padx=0)
        self.id_number_label.pack(fill='both', expand=1)

        # pad frame
        #Frame(master).grid(row=6, column=1, sticky='wens')

        # grade
        level_label_x = Frame(master)
        level_label_x.grid(row=5, column=1, sticky='wens')
        Label(level_label_x, text="Level:", font=self.label_Font, anchor='w').pack(fill='both', expand=1)
        level_frame = Frame(master)
        level_frame.grid(row=6, column=1, sticky='wens')
        self.level_label = Label(level_frame, text="x-x-x-x", font=self.value_Font, anchor='w', padx=0)
        self.level_label.pack(fill='both', expand=1)

        # pad frame
        #Frame(master).grid(row=9, column=1, sticky='wens')

        # section
        section_label_x = Frame(master)
        section_label_x.grid(row=7, column=1, sticky='wens')
        Label(section_label_x, text="Section:", font=self.label_Font, anchor='w').pack(fill='both', expand=1)
        section_frame = Frame(master)
        section_frame.grid(row=8, column=1, sticky='wens')
        self.section_label = Label(section_frame, text="x-x-x-x", font=self.value_Font, anchor='w', padx=0)
        self.section_label.pack(fill='both', expand=1)

        # pad frame
        #Frame(master).grid(row=11, column=1, sticky='wens')

        # date/time
        time_label_x = Frame(master)
        Label(time_label_x, text="Date/Time:", font=self.label_Font, anchor='w').pack(fill='both', expand=1)
        time_label_x.grid(row=9, column=1, sticky='wens')
        time_label = Frame(master)
        time_label.grid(row=10, column=1, sticky='wens')
        self.time_label_value = Label(time_label, text="", padx=0, anchor='w', font=self.time_Font)
        self.time_label_value.pack(fill='both', expand=1)

        # pad frame
        #Frame(master).grid(row=12, column=1, sticky='wens')

        # name
        name_frame = Frame(master)
        name_frame.grid(row=11, columnspan=2, rowspan=5, sticky='wens', ipady=10)
        #self.name_label = Label(name_frame, text="x-x-x-x\nx-x-x-x", font=self.value_Font)
        #ini_string = "张南生"
        self.name_label = Label(name_frame, text="x-x-x-x\nx-x-x-x", font=self.value_Font)
        self.name_label.pack(fill='both', expand=1)
        #self.name_label.config(text=format_string(ini_string.decode("utf-8"), 28), fg="black")

        # status
        status_frame = Frame(master)
        #status_frame.grid(row=16, column=1, sticky='e')
        status_frame.grid(row=16, columnspan=2, sticky='wens')
        self.status_label = Label(status_frame, text="").pack(fill='both', expand=1)

        Frame(master).grid(row=1, rowspan=2,column=0, sticky='wens', ipady=10)

        #Lunch Pass
        lunch_frame = Frame(master)
        lunch_frame.grid(row=3, column=0,sticky='nsew')
        self.lunch_label = Label(lunch_frame, text="Lunch Pass", font=self.lunch_font, fg="grey70")
        self.lunch_label.pack(fill='both', expand=1)

        #Commuter Pass
        commuter_frame = Frame(master)
        commuter_frame.grid(row=4, column=0,sticky='nsew')
        self.commuter_label = Label(commuter_frame, text="Commuter's Pass", font=self.commuter_font, padx=0, fg="grey70")
        self.commuter_label.pack(fill='both', expand=1)

        # image
        self.image = Frame(master)
        self.image.grid(row=5, rowspan=6, column=0,sticky='nsew', padx=0)
        self.label = ImageLabel(self.image, "{0}/default.png".format(os.path.dirname(os.path.abspath(__file__))))
        self.label.pack(fill="both", expand=1)

        self._poll_job_id = self.poll()
        master.geometry("700x430")
        self.heightxx, self.widthxx = None, None

    def _configure(self, event):
        label_width = float(event.width) / 2

        if event.height == self.heightxx and event.width == self.widthxx: return
        self.heightxx = event.height
        self.widthxx = event.width

        padx = label_width * .50

        self.id_number_label.configure(padx=padx, width=1)
        self.level_label.configure(padx=padx, width=1)
        self.section_label.configure(padx=padx, width=1)
        self.time_label_value.configure(padx=padx, width=1)
        self.master.configure(width=event.width, height=event.height)

    def poll(self):
        try:
            call(["xdotool", "key", "1"])
        except:
            print "error xdotool"
        shared = memcache.Client(['127.0.0.1:11211'], debug=0)
        if shared.get('connection'):
            try:
                con_message = json.loads(shared.get('connection'))
                text = con_message['status'] + '/' + con_message['school_name'] + '/' + con_message['school_year'] + '/' + con_message['kind']
            except:
                text = 'OFFLINE' + '/' + school_name + '/' + school_year + '/' + kind
            if self.status_label:
               self.status_label.config(text=text)
        elif self.status_label:
            text = 'OFFLINE' + '/' + school_name + '/' + school_year + '/' + kind
            self.status_label.config(text=text)

        if shared.get('message'):
            messages = json.loads(shared.get('message'))

            try:
                msg_id_number = messages['id_number']
            except:
                msg_id_number = ""

            if self.id_number != msg_id_number:

                self.id_number = messages['id_number']

                try:
                    status = messages['status']
                except:
                    status = "INVALID"

                if status == "VALID":
                    try:
                        name_value = messages['name']
                        try:
                            chinese_name = messages['chinese_name']
                            #name_value = chinese_name + "\n" + name_value
                            if chinese_name:
                                #chinese_name = ascii(chinese_name)
                                name_value = chinese_name.decode("utf-8") + "\n" + name_value
                            else:
                                name_value = messages['name']
                        except:
                            name_value = messages['name']
                    except:
                        name_value = "x-x-x-x"

                    try:
                        id_number_value = messages['id_number']
                    except:
                        id_number_value = ""

                    try:
                        level_value = messages['level']
                    except:
                        level_value = ""

                    try:
                        section_value = messages['section']
                    except:
                        section_value = ""

                    try:
                        filename = messages['id_picture']
                    except:
                        filename = '{0}/default.png'.format(os.path.dirname(os.path.abspath(__file__)))

                    if not filename:
                        filename = '{0}/default.png'.format(os.path.dirname(os.path.abspath(__file__)))

                    #Lunch Pass
                    try:
                        lunch_value = messages['lunch_pass']
                        if lunch_value == "Yes":
                            self.lunch_label.config(fg="green")
                        else:
                            self.lunch_label.config(fg="grey70")
                    except:
                        lunch_value = ""

                    #Commuter Pass
                    try:
                        commuter_value = messages['commuter_pass']
                        if commuter_value == "Yes":
                            self.commuter_label.config(fg="green")
                        else:
                            self.commuter_label.config(fg="grey70")
                    except:
                        commuter_value = ""

                    self.name_label.config(text=format_string(name_value, 60), fg="black")
                    self.id_number_label.config(text=format_string(id_number_value, 15), fg="black")
                    self.level_label.config(text=format_string(level_value, 15), fg="black")
                    self.section_label.config(text=format_string(section_value, 25), fg="black")


                    try:
                        orig = Image.open(filename)
                        self.label.original = orig
                        self.label.resize2()
                    except:
                        pass

                else:
                    self.name_label.config(text="X X X X X X X X X X X X", fg="red")
                    self.id_number_label.config(text="X X X X X X", fg="red")
                    self.level_label.config(text="X X X X X X", fg="red")
                    self.section_label.config(text="X X X X X X", fg="red")

                    filename = '{0}/default.png'.format(os.path.dirname(os.path.abspath(__file__)))
                    #self.image = Frame(root)
                    #self.image.grid(row=0, rowspan=12, sticky='nsew', padx=0)
                    #self.label = ImageLabel(self.image, filename)
                    #self.label.pack(fill="both", expand=1)
                    self.image = Frame(root)
                    self.image.grid(row=5, rowspan=6, column=0, sticky='nsew', padx=0)
                    self.label = ImageLabel(self.image,filename)
                    self.label.pack(fill="both", expand=1)

        self.time_label_value.config(text=get_time().strftime('%b %d, %Y %I:%M:%S %p'))
        self._poll_job_id = self.master.after(100, self.poll)


def format_string(value, length):
    if not value:
        return ""
    else:
        return value[:length]


def get_font(config, section):
    config_value = config.get('ui', section, 0)
    weight = 'normal'
    line = config_value.split(',')
    size = line[0].split(':')[1].strip()
    if len(line) > 1:
        weight = line[1].split(':')[1].strip()
    return tkFont.Font(family=family, size=size, weight=weight)


if __name__ == '__main__':

    root = Tk()
    root.attributes('-fullscreen', True)

    config = ConfigParser.ConfigParser()
    config.read("{0}/rfid.ini".format(os.path.dirname(os.path.abspath(__file__))))
    family = config.get('ui', 'font_family', 0)
    distance = config.get('ui', 'distance', 0)
    school_name = config.get('data', 'school_name', 0)
    school_year = config.get('data', 'school_year', 0)
    kind = config.get('data', 'kind', 0)

    label_font = get_font(config, 'label_font')
    name_font = get_font(config, 'name_font')
    value_font = get_font(config, 'value_font')
    status_font = get_font(config, 'status_font')
    time_font = get_font(config, 'time_font')
    lunch_font = get_font(config, 'lunch_font')
    commuter_font = get_font(config, 'commuter_font')

    app = Application(master=root)
    app.mainloop()
