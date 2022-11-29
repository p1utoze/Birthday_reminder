from tkinter import *
from tkinter import font
from PIL import ImageTk, Image
from tkcalendar import Calendar
from tkinter import messagebox
import json


class Birthday(Frame):
    def __init__(self, root):
        super().__init__(root)
        self["bg"] = "#ffd4d4"
        self.place(x=0, y=0, width=900, height=500)
        self.name = StringVar()
        self.banner()
        self.heading()
        self.choice()

    def choice(self):
        self.frame = Frame(self, bg=self['bg'], relief="raised")
        self.frame.place(relx=0.45, rely=0.3, relheight=0.5, relwidth=0.5)

        ch = Label(self.frame, text="What do you want to do?", bg=self["bg"],
             fg="black", font=("Ubuntu", 18, "bold"))
        ch.place(relx=0.1, rely=0.1, anchor="nw")

        but1 = Button(self.frame, text='ADD DATE', command=self.choice_add, activebackground="#03fc0b",
                      font=('broadway', 14, 'bold'), height=2, width=10, relief="flat", bg='#009105')
        but1.place(relx=0.15, rely=0.4)

        but2 = Button(self.frame, text='DELETE DATE', command=self.choice_del, activebackground="#ff0000",
                      font=('aerial', 14, 'bold'), height=2, width=10, relief="flat", bg='#b50000')
        but2.place(relx=0.5, rely=0.4)

    def choice_add(self):
        self.flag = 1
        self.forget(self.frame)
        self.subframe = Frame(self, bg=self['bg'], relief="raised")
        self.subframe.place(relx=0.45, rely=0.2, relheight=0.55, relwidth=0.55)

        Label(self.subframe, text="Enter the name to be saved as reminder: ",
              bg=self["bg"], fg="black", font=("aerial", 14, "bold")).place( rely=0.2)
        self.value = StringVar()
        self.text1 = Entry(self.subframe, width=35, textvariable=self.value, borderwidth=5, relief=FLAT)
        self.text1.bind("<Return>", self.val)
        self.text1.place(relx=.15, rely=0.4)

        Button(self.subframe, font=('aerial', 9, 'bold'), text='ENTER', command=lambda: self.val(1),
               background='#a881af').place(relx=0.7, rely=0.4)

        Label(self.subframe, bg=self['bg'], text="Click on 'Choose Date' to add birthday: ",
              font=("Ubuntu", 14, 'bold')).place(rely=0.7)

        Button(self.subframe, font=('aerial', 12, 'bold'), text='Choose Date', command=self.fetch,
               height=1, background='#a881af').place(relx=0.35, rely=.85)

    def choice_del(self):
        self.flag = 0
        self.forget(self.frame)
        self.subframe = Frame(self, bg=self['bg'], relief="raised")
        self.subframe.place(relx=0.45, rely=0.2, relheight=0.55, relwidth=0.55)

        Label(self.subframe, text="Enter the name to be removed: ",
              bg=self["bg"], fg="black", font=("aerial", 14, "bold")).place( rely=0.2)
        self.value = StringVar()
        self.text1 = Entry(self.subframe, width=35, textvariable=self.value, borderwidth=5, relief=FLAT)
        self.text1.bind("<Return>", self.val)
        self.text1.place(relx=.05, rely=0.4)

        Button(self.subframe, font=('aerial', 9, 'bold'), text='ENTER', command=lambda: self.val(1),
               background='#a881af').place(relx=0.6, rely=0.4)

        Label(self.subframe, bg=self['bg'], text="Click to remove the birthday: ",
              font=("Ubuntu", 14, 'bold')).place(rely=0.7)

        Button(self.subframe, font=('aerial', 12, 'bold'), text='Choose Date', command=self.fetch,
               height=1, background='#a881af').place(relx=0.25, rely=.85)


    def banner(self):
        self.img = ImageTk.PhotoImage(Image.open("../bdayrem/bg.png"))
        self.ban_font = font.Font(font=('Times New Roman', 40, 'bold'))
        lab = Label(self, image=self.img, text="BIRTHDAY\nREMINDER",
                    font=self.ban_font, fg="white", borderwidth=3, relief="raised", compound='center')
        lab.place(x=0, y=0, relwidth=0.4, relheight=1)

    def heading(self):
        textlabel = Label(self, text="NEVER MISS OUT ANYTHING!", fg=self["bg"],
                 padx=20, pady=100, bg="#ff5667", font=('Ubuntu Mono', 25, 'bold', 'underline'))
        textlabel.place(relx=0.4, rely=0.0, relheight=0.1)
        # root.wait_visibility(root)

    def forget(self, widget):
        widget.place_forget()

    def fetch(self):
        top = Toplevel(root)   
        def date():
            self.name.set(cal.get_date()[:5])
            self.forget(self.subframe)
            self.frame.place(relx=0.45, rely=0.3, relheight=0.5, relwidth=0.5)
            top.destroy()
            self.submit()


        cal = Calendar(top,
                    font="Arial 14", selectmode='day',
                    cursor="hand1", year=2022, month=2, day=5)
        cal.pack(fill="both", expand=True)
        Button(top, text="OK", command=date).pack()

    def val(self, a):
        t = self.value.get()
        self.cpy = t
        print(t, type(t))
        if not t:
            self.text1.delete(0, "end")
            self.text1.insert(15, "               Can't be empty!")
        else:
            self.text1.delete(0,"end")
            self.text1.insert(15, "                   Added!")

    def submit(self):
        with open("data.json",'r') as f:
            d=json.load(f)
        if self.flag:
            self.json_add(d)
        else:
            self.json_del(d)

    def json_add(self, d):
        date = self.name.get()
        try:
            d[date].append(self.cpy.capitalize())
        except KeyError:
            d[date] = [self.cpy.capitalize()]
        d[date].sort()
        with open("data.json", 'w') as f:
            json.dump(d, f, sort_keys=True, indent=4)
        messagebox.showinfo(message="Birthday date added!")
        print(d)

    def json_del(self, d):
        date = self.name.get()
        try:
            name = self.cpy.capitalize()
            if name in d[date]:
                d[date].remove(name)
            else:
                raise KeyError("No name Found!")
        except KeyError:
            messagebox.showinfo(message="Couldn't find the date or name!\n Please try again.")
        else:
            messagebox.showinfo(message="Birthday date removed!")
            if not d[date]:
                d.pop(date, "No key Found!")
            else:
                d[date].sort()
            with open("data.json", 'w') as f:
                json.dump(d, f, sort_keys=True, indent=4)
        print(d)

if __name__ == "__main__":
    root = Tk()
    root.geometry("900x500")
    root.title("Birthday Reminder")
    root.after(300000, root.destroy)
    root.resizable(None, None)
    ref = Birthday(root)
    root.mainloop()
