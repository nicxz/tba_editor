from tkinter import *
#from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog   import asksaveasfilename
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askstring
from tkinter.messagebox import askokcancel
from tkinter.messagebox import showerror


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
        Quitter(frm).pack(side=LEFT)
        super().__init__(parent, file=file)

        self.text['font'] = 'courier', 12, 'normal'
        self.target = ''

    def onNew(self):
        self.text.delete('1.0', END)

    def onOpen(self):
        filename = askopenfilename(title='Open File', filetypes=[("Text files", "*.txt")])
        if filename:
            try:
                f = open(filename)
                contents = f.read()
                self.text.delete('1.0', END)
                self.text.insert('1.0', contents)
                f.close()
            except:
                showerror("Open File", "Failed to read file\n'%s'" % filename)
            return


    def onSave(self):
        filename = asksaveasfilename(defaultextension='.txt',
                                     filetypes=(('Text files', '*.txt'),
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

################################################################################



################################################################################

if __name__ == '__main__':
    SimpleEditor(file=sys.argv[1] if len(sys.argv) > 1 else None).mainloop()