from tkinter import *
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askstring
from tkinter.messagebox import askokcancel
from tkinter.messagebox import showerror
import csv
from collections import defaultdict

root = Tk()
columns = defaultdict(list) # each value in each column is appended to a list


class ScrolledText(Frame):

    def __init__(self, parent=None, text='', file=None):
        super().__init__(parent)
        self.pack(expand=YES, fill=BOTH)
        self.makewidgets()
        self.settext(text, file)

    def makewidgets(self):
        sbar = Scrollbar(self)
        self.text = Text(self, relief=SUNKEN, wrap=WORD)
        sbar['command'] = self.text.yview
        self.text['yscrollcommand'] = sbar.set
        sbar.pack(side=RIGHT, fill=Y)
        self.text.pack(side=LEFT, expand=YES, fill=BOTH)

    def settext(self, text='', file=None):
        if file:
            with open(file, 'r') as stream:
                text = stream.read()
        self.text.delete('1.0', END)
        self.text.insert('1.0', text)
        self.text.mark_set(INSERT, '1.0')
        self.text.focus()

    def gettext(self):
        return self.text.get('1.0', END + '-1c')

################################################################################

class Quitter(Frame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pack()
        widget = Button(self, text='Quit', command=self.quit)
        widget.pack(expand=YES, fill=BOTH, side=LEFT)

    def quit(self):
        if askokcancel('Verify exit', 'Really quit?'):
            self._root().destroy()

################################################################################

class SimpleEditor(ScrolledText):

    def __init__(self, parent=None, file=None):
        frm = Frame(parent)
        frm.pack(fill=X)
        Button(frm, text='New',   command=self.onNew).pack(side=LEFT)
        Button(frm, text='Open',  command=self.onOpen).pack(side=LEFT)
        Button(frm, text='Save',  command=self.onSave).pack(side=LEFT)
        Button(frm, text='Cut',   command=self.onCut).pack(side=LEFT)
        Button(frm, text='Paste', command=self.onPaste).pack(side=LEFT)
        Button(frm, text='Find',  command=self.onFind).pack(side=LEFT)

        #Button(frm, text='NewVariable', command=self.onNewVariable).pack(side=RIGHT)

        Quitter(frm).pack(side=LEFT)
        super().__init__(parent, file=file)

        self.text['font'] = 'courier', 12, 'normal'
        self.text.tag_configure('red', foreground='red', relief='raised')
        self.target = ''

        self.onVariable()


    def onNew(self):
        self.text.delete('1.0', END)

    def onOpen(self):
        filename = askopenfilename(title='Open File', filetypes=[("CSV files", "*.csv")])
        if filename:
            try:
                with open(filename, newline='') as f:
                    contents = csv.reader(f, delimiter='$', quotechar='|')
                    self.text.delete('1.0', END)
                    for row in contents:
                        if row[0] == 'TITLE':
                            storyTitle = row[1]
                            self.text.insert('1.0' , "Story title is: " + storyTitle + '\n\n')
                        elif row[0] == 'var':
                            pass
                        else:
                            self.text.insert(END, "ID: " + row[0], "red")
                            self.text.insert(END, "   " + row[1])
                            self.text.insert(END, '\n')
                    f.close()
            except:
                showerror("Open File", "Failed to read file\n'%s'" % filename)
            return
        else:
            showerror("Open File", "Cant find file\n'%s'" % filename)


    def onSave(self):
        filename = asksaveasfilename(defaultextension='.csv',
                                     filetypes=(('CSV files', '*.csv'),
                                                ('Python files', '*.py *.pyw'),
                                                ('All files', '*.*')))
        if filename:
            with open(filename, 'w') as stream:
                stream.write(self.gettext())

    def onCut(self):
        self.clipboard_clear()
        self.clipboard_append(self.text.get(SEL_FIRST, SEL_LAST))
        self.text.delete(SEL_FIRST, SEL_LAST)

    def onPaste(self):
        try:
            self.text.insert(INSERT, self.selection_get(selection='CLIPBOARD'))
        except TclError:
            pass

    def onFind(self):
        self.target = askstring('SimpleEditor', 'Search String?',
                                initialvalue=self.target)
        if self.target:
            where = self.text.search(self.target, INSERT, END, nocase=True)
            if where:
##                print(where)
##                self.text.tag_remove(SEL, '1.0', END)
                pastit = '{}+{}c'.format(where, len(self.target))
                self.text.tag_add(SEL, where, pastit)
                self.text.mark_set(INSERT, pastit)
                self.text.see(INSERT)
                self.text.focus()

    def onVariable(self):
        NewVarWindow = Tk()
        Label(NewVarWindow, text="Variable name").grid(row=0)
        Label(NewVarWindow, text="Variable type").grid(row=1)
        Label(NewVarWindow, text="Default value").grid(row=2)

        varname = Entry(NewVarWindow)
        vartype = Entry(NewVarWindow)
        vardefault = Entry(NewVarWindow)

        varname.grid(row=0, column=1)
        vartype.grid(row=1, column=1)
        vardefault.grid(row=2, column=1)

       #Button(NewVarWindow, text='Save', command=self.SaveNewVar).grid(row=4, column=0, sticky=W, pady=4)

    def SaveNewVar(self):
        randomvar = 1
        # placeholder


################################################################################



################################################################################



if __name__ == '__main__':
    SimpleEditor(file=sys.argv[1] if len(sys.argv) > 1 else None).mainloop()