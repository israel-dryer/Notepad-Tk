"""
    Menubar
        File
            New (CTRL+N), Open(CTRL+O), Save(CTRL+S), SaveAs, 
            ---, Exit
        Edit
            Undo(CTRL+Z), 
            ---, Cut(CTRL+X), Copy(CTRL+C), Paste(CTRL+V), Delete(Del)
            ---, Find(CTRL+F), FindNext(F3), Replace(CTRL+H), GoTo(CTRL+G)
            ---, SelectAll(CTRL+A), TimeDate(F5)
        Format
            WordWrap, Font...
        Help
            ViewHelp
            About

    Window + Scrollbar
"""
# http://effbot.org/tkinterbook/text.htm

import tkinter as tk
from tkinter import font as tkfont
from tkinter import filedialog, messagebox
import pathlib
import datetime


class Notepad(tk.Tk):
    """A notepad application"""
    def __init__(self):
        super().__init__()
        self.tk_setPalette('#e6e6ea')
        self.iconbitmap('Notepad.ico')

        # general app variables
        self.file = pathlib.Path.cwd() / 'untitled.txt'
        self.file_defaults = {
            'defaultextension': 'txt', 
            'filetypes': [('Text', ['txt', 'text']), ('All Files', '.*')]}

        # main menu setup
        self.menu = tk.Menu(self)
        self.configure(menu=self.menu)
        self.menu_file = tk.Menu(self.menu, tearoff=False)
        self.menu_edit = tk.Menu(self.menu, tearoff=False)
        self.menu_format = tk.Menu(self.menu, tearoff=False)
        self.menu_help = tk.Menu(self.menu, tearoff=False)
        
        # file menu
        self.menu_file.add_command(label='New', accelerator='Ctrl+N', command=self.new_file)
        self.menu_file.add_command(label='Open', accelerator='Ctrl+O', command=self.open_file)
        self.menu_file.add_command(label='Save', accelerator='Ctrl+S', command=self.save_file)
        self.menu_file.add_command(label='Save As', command=self.save_file_as)
        self.menu_file.add_separator()
        self.menu_file.add_command(label='Exit', command=self.quit_application)
        
        # edit menu
        self.menu_edit.add_command(label='Undo', accelerator='Ctrl+Z', command=None)
        self.menu_edit.add_separator()
        self.menu_edit.add_command(label='Cut', accelerator='Ctrl+X', command=None)
        self.menu_edit.add_command(label='Copy', accelerator='Ctrl+C', command=None)
        self.menu_edit.add_command(label='Paste', accelerator='Ctrl+V', command=None)
        self.menu_edit.add_command(label='Delete', accelerator='Del', command=None)
        self.menu_edit.add_separator()
        self.menu_edit.add_command(label='Find', accelerator='Ctrl+F', command=None)
        self.menu_edit.add_command(label='Find Next', accelerator='F3', command=None)
        self.menu_edit.add_command(label='Replace', accelerator='Ctrl+H', command=None)
        self.menu_edit.add_command(label='Go To', accelerator='Ctrl+G', command=None)
        self.menu_edit.add_separator()
        self.menu_edit.add_command(label='Select All', accelerator='Ctrl+A', command=None)
        self.menu_edit.add_command(label='Time/Date', accelerator='F5', command=self.get_datetime)

        # format menu
        self.wrap_var = tk.IntVar()
        self.wrap_var.set(1)
        self.menu_format.add_checkbutton(label='Word Wrap', variable=self.wrap_var, command=None)
        self.menu_format.add_command(label='Font...', command=None)

        # help menu
        self.menu_help.add_command(label='View Help', command=None)
        self.menu_help.add_command(label='About Notepad', command=None)

        # add cascading menus to main menu
        self.menu.add_cascade(label='File', menu=self.menu_file)
        self.menu.add_cascade(label='Edit', menu=self.menu_edit)
        self.menu.add_cascade(label='Format', menu=self.menu_format)
        self.menu.add_cascade(label='Help', menu=self.menu_help)

        # setup multiline text widget
        self.yscrollbar = tk.Scrollbar(self)
        self.multiline = tk.Text(self, wrap=tk.WORD, font='-size 12', yscrollcommand=self.yscrollbar.set, padx=5, pady=10)

        # set default tab size to 4 characters
        font = tkfont.Font(font=self.multiline['font'])
        tab_width = font.measure(' ' * 4)
        self.multiline.configure(tabs=(tab_width,))
        self.multiline.insert(tk.END, self.file.read_text() if self.file.is_file() else '')

        # pack all widget to screen
        self.yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.multiline.pack(fill=tk.BOTH, expand=tk.YES)

        self.update_title()

    #---FILE MENU CALLBACKS------------------------------------------------------------------------

    def new_file(self):
        """Create a new file"""
        # check for content change before opening new file
        self.confirm_changes()

        # reset text widget
        self.multiline.delete(1.0, tk.END)
        self.file = pathlib.Path.cwd() / 'untitled.txt'
        self.update_title()

    def open_file(self):
        """Open an existing file"""
        # check for content change before opening new file
        self.confirm_changes()

        # open new file
        file = filedialog.askopenfilename(initialdir=self.file.parent, **self.file_defaults)
        if file:
            self.multiline.delete(1.0, tk.END)  # delete existing content
            self.file = pathlib.Path(file)
            self.multiline.insert(tk.END, self.file.read_text())
            self.update_title()

    def save_file(self):
        """Save the currently open file"""
        if self.file.name == 'untitled.txt':
            file = filedialog.asksaveasfilename(initialfile=self.file, **self.file_defaults)
            self.file = pathlib.Path(file) if file else self.file
        self.file.write_text(self.multiline.get(1.0, tk.END))

    def save_file_as(self):
        """Save the currently open file with a different name or location"""
        file = filedialog.asksaveasfilename(initialdir=self.file.parent, **self.file_defaults)
        if file:
            self.file = pathlib.Path(file)
            self.file.write_text(self.multiline.get(1.0, tk.END))
            self.update_title()

    def confirm_changes(self):
        """Check to see if content has changed from original file; if so, confirm save"""
        if self.file.is_file():
            original = self.file.read_text()
            current = self.multiline.get(1.0, tk.END)
            if original != current:
                confirm = messagebox.askyesno(message="Save current file changes?")
                if confirm:
                    self.save_file()
        elif len(self.multiline.get(1.0, tk.END)) > 1:
            confirm = messagebox.askyesno(message="Save current document?")
            if confirm:
                self.save_file()

    def quit_application(self):
        """Quit application after checking for user changes"""
        self.confirm_changes()
        self.destroy()

    def update_title(self):
        """Update the title with the file name"""
        self.title(self.file.name + " - Notepad")

    #---EDIT MENU CALLBACKS------------------------------------------------------------------------

    def get_datetime(self):
        """insert date and time at cursor position"""
        self.multiline.insert(tk.INSERT, datetime.datetime.now().strftime("%c"))        

if __name__ == '__main__':
    notepad = Notepad()
    notepad.mainloop()
