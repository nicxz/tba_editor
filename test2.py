import Tkinter as tk
from Tkinter import *
from ScrolledText import *
import tkFileDialog
import tkMessageBox


class StartMenu(tk.Tk):
    def __init__(self, parent, *args, **kwargs):
        tk.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        label = tk.Label(self, text="Start Menu")

        self.button = Button(self,
                         text="Start new story",
                         command=lambda: controller.show_frame(Editor))
        self.button.pack(side=LEFT)
        self.slogan = Button(self.frame,
                         text="Open existing story",
                         command=self.write_slogan)
        self.slogan.pack(side=LEFT)
        self.exitbutton = Button(self.frame,
                             text="Quit",
                             command=self.frame.quit)
        self.exitbutton.pack(side=LEFT)
    def write_slogan(self):
        print "Open existing story"

    def write_slogan2(self):
        print "Start new story"

    def openEditor(self):
        myEditor = Editor
        myEditor.__init__

class Editor(tk.Tk):

    def open_command():
        file = tkFileDialog.askopenfile(parent=self,mode='rb',title='Select a file')
        if file != None:
            contents = file.read()
            textPad.insert('1.0',contents)
            file.close()

    def save_command(self):
        file = tkFileDialog.asksaveasfile(mode='w')
        if file != None:
            # slice off the last character from get, as an extra return is added
            data = self.textPad.get('1.0', END+'-1c')
            file.write(data)
            file.close()

    def exit_command():
        if tkMessageBox.askokcancel("Quit", "Do you really want to quit?"):
            self.frame.destroy()

    def about_command():
        label = tkMessageBox.showinfo("About", "Sample TextPad \n Base for new project \n To be filled in later ")

    def openEditor():
        textPad.pack()
        self.frame.mainloop()

    def dummy():
        print "I am a Dummy Command, I will be removed later"

    def createWidgets(self):
        self.menuBar = Menu(self)
        self.filemenu = Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="New", command=self.dummy)
        self.filemenu.add_command(label="Open...", command=self.open_command)
        self.filemenu.add_command(label="Save", command=self.save_command)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.exit_command)
        self.helpmenu = Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label="Help", menu=self.helpmenu)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Editor")
        label.pack()
        textPad = ScrolledText(self, width=100, height=80)
        self.createWidgets()
        self.config(menu=self.menuBar)

if __name__ == "__main__":
    root = tk.Tk()
    StartMenu(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
