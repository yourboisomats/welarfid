from Tkinter import *
import tkFont
from PIL import Image, ImageTk
from subprocess import call
from db import *

#common components
label_font = None
name_font = None
value_font = None
status_font = None
time_font = None
image_width = None
distance = None


class ImageLabel(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.master = master
        self.original = Image.open('default.png')
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


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.master.title("Wela RFID")

        for r in range(16):
            self.master.rowconfigure(r, weight=1)

        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=distance)

        self.label_Font = label_font
        self.name_Font = name_font
        self.value_Font = value_font
        self.status_Font = status_font
        self.time_Font = time_font

        # id
        id_number_label_x = Frame(master, relief=SUNKEN)
        id_number_label_x.grid(row=1, column=1, sticky='wens')
        self.id_number_label_y = Label(id_number_label_x, text="ID #:", font=self.label_Font, anchor='w').pack(
            fill='both', expand=1)
        id_number_frame = Frame(master)
        id_number_frame.grid(row=2, column=1, sticky='wens')
        self.id_number_label = Label(id_number_frame, text="09-2303423", font=self.value_Font, anchor='w', padx=0)
        self.id_number_label.pack(fill='both', expand=1)

        # pad frame
        Frame(master).grid(row=3, column=1, sticky='wens')

        # grade
        level_label_x = Frame(master)
        level_label_x.grid(row=4, column=1, sticky='wens')
        Label(level_label_x, text="Level:", font=self.label_Font, anchor='w').pack(fill='both', expand=1)
        level_frame = Frame(master)
        level_frame.grid(row=5, column=1, sticky='wens')
        self.level_label = Label(level_frame, text="Grade 6", font=self.value_Font, anchor='w', padx=0)
        self.level_label.pack(fill='both', expand=1)

        # pad frame
        Frame(master).grid(row=6, column=1, sticky='wens')

        # section
        section_label_x = Frame(master)
        section_label_x.grid(row=7, column=1, sticky='wens')
        Label(section_label_x, text="Section:", font=self.label_Font, anchor='w').pack(fill='both', expand=1)
        section_frame = Frame(master)
        section_frame.grid(row=8, column=1, sticky='wens')
        self.section_label = Label(section_frame, text="Diligence", font=self.value_Font, anchor='w', padx=0)
        self.section_label.pack(fill='both', expand=1)

        # pad frame
        Frame(master).grid(row=9, column=1, sticky='wens')

        # date/time
        time_label_x = Frame(master)
        Label(time_label_x, text="Date/Time:", font=self.label_Font, anchor='w').pack(fill='both', expand=1)
        time_label_x.grid(row=10, column=1, sticky='wens')
        time_label = Frame(master)
        time_label.grid(row=11, column=1, sticky='wens')
        self.time_label_value = Label(time_label, text="**********", padx=0, anchor='w', font=self.time_Font)
        self.time_label_value.pack(fill='both', expand=1)

        # pad frame
        Frame(master).grid(row=12, column=1, sticky='wens')

        # name
        name_frame = Frame(master)
        name_frame.grid(row=13, columnspan=2, rowspan=2, sticky='wens')
        self.name_label = Label(name_frame, text="Juan, De la Cruz", font=self.name_Font).pack(fill='both', expand=1)

        # status
        status_frame = Frame(master)
        status_frame.grid(row=15, column=1, sticky='e')
        self.status_label = Label(status_frame, text="ONLINE/Anglicum Learning Center/SY2016/IN/v12").pack(fill='both', expand=1)

        # image
        self.image = Frame(master)
        self.image.grid(row=0, rowspan=12, sticky='nsew', padx=0)

        self.photo = ImageLabel(self.image)
        self.photo.pack(fill="both", expand=1)
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
        shared = memcache.Client(['127.0.0.1:11211'], debug=0)
        if shared.get('connection'):
            try:
                con_message = json.loads(shared.get('connection'))
                text = con_message['status'] + '/' + con_message['school_name'] + '/' + con_message['school_year'] + '/' + con_message['kind']
            except:
                text = 'OFFLINE' + '/' + school_name + '/' + school_year + '/' + kind
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

        self.time_label_value.config(text=get_time().strftime('%b %d, %Y %I:%M:%S %p'))
        self._poll_job_id = self.master.after(500, self.poll)


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
    # root.attributes('-fullscreen', True)

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

    app = Application(master=root)
    app.mainloop()
