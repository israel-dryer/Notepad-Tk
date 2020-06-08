"""
    A simple notepad application with functionality for some formatting commands, font selection,
    find & replace, etc...

    Author: Israel Dryer
    Modified: 2020-06-07
"""

import tkinter as tk
from tkinter import font as tkfont
from tkinter import filedialog, messagebox
import pathlib
import datetime
from widgets.texttools import Find, Replace
from widgets.fontselect import FontSelector
from widgets.about import AboutMe
from widgets.ribbon import Ribbon
from widgets.statusbar import StatusBar


class Notepad(tk.Tk):
    """A notepad application"""
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.iconbitmap('images/Notepad.ico')
        self.wm_state('zoomed')  # start application zoomed

        # file variables
        self.file = pathlib.Path.cwd() / 'untitled.txt'
        self.file_defaults = {
            'defaultextension': 'txt', 
            'filetypes': [('Text', ['txt', 'text']), ('All Files', '.*')]}

        # find search replace variables
        self.query = None
        self.matches = None
        self.findnext = None
        self.findreplace = None

        # main menu setup
        self.menu = tk.Menu(self)
        self.configure(menu=self.menu)
        self.menu_file = tk.Menu(self.menu, tearoff=False)
        self.menu_edit = tk.Menu(self.menu, tearoff=False)
        self.menu_format = tk.Menu(self.menu, tearoff=False)
        self.menu_help = tk.Menu(self.menu, tearoff=False)
        
        # file menu
        self.menu_file.add_command(label='New', accelerator='Ctrl+N', command=self.new_file)
        self.menu_file.add_command(label='Open...', accelerator='Ctrl+O', command=self.open_file)
        self.menu_file.add_command(label='Save', accelerator='Ctrl+S', command=self.save_file)
        self.menu_file.add_command(label='Save As...', command=self.save_file_as)
        self.menu_file.add_separator()
        self.menu_file.add_command(label='Exit', command=self.quit_application)

        # edit menu
        self.menu_edit.add_command(label='Undo', accelerator='Ctrl+Z', command=self.undo_edit)
        self.menu_edit.add_command(label='Redo', accelerator='Ctrl+Y', command=self.redo_edit)
        self.menu_edit.add_separator()
        self.menu_edit.add_command(label='Cut', accelerator='Ctrl+X', command=self.text_cut)
        self.menu_edit.add_command(label='Copy', accelerator='Ctrl+C', command=self.text_copy)
        self.menu_edit.add_command(label='Paste', accelerator='Ctrl+V', command=self.text_paste)
        self.menu_edit.add_separator()
        self.menu_edit.add_command(label='Find', accelerator='Ctrl+F', command=self.ask_find_next)
        self.menu_edit.add_command(label='Replace', accelerator='Ctrl+H', command=self.ask_find_replace)
        self.menu_edit.add_separator()
        self.menu_edit.add_command(label='Select All', accelerator='Ctrl+A', command=self.select_all)
        self.menu_edit.add_command(label='Time/Date', accelerator='F5', command=self.get_datetime)

        # format menu
        self.wrap_var = tk.IntVar()
        self.wrap_var.set(True)
        self.block_var = tk.IntVar()
        self.block_var.set(False)
        self.menu_format.add_checkbutton(label='Word Wrap', variable=self.wrap_var, command=self.word_wrap)
        self.menu_format.add_checkbutton(label='Block Cursor', variable=self.block_var, command=self.block_cursor)
        self.menu_format.add_separator()
        self.menu_format.add_command(label='Font...', command=self.ask_font_select)

        # help menu
        self.menu_help.add_command(label='View Help', state=tk.DISABLED, command=None)
        self.menu_help.add_command(label='About Notepad', command=self.about_me)

        # add cascading menus to main menu
        self.menu.add_cascade(label='File', menu=self.menu_file)
        self.menu.add_cascade(label='Edit', menu=self.menu_edit)
        self.menu.add_cascade(label='Format', menu=self.menu_format)
        self.menu.add_cascade(label='Help', menu=self.menu_help)

        # add ribbon menu
        self.ribbon = Ribbon(self)

        # setup text text widget
        self.text_frame = tk.Frame(self)
        self.yscrollbar = tk.Scrollbar(self.text_frame, command=self.yscroll)
        self.text = tk.Text(self.text_frame, wrap=tk.WORD, font='-size 14', undo=True, maxundo=10,
            autoseparator=True, yscrollcommand=self.yscrollbar.set, blockcursor=False, padx=5, pady=10)
         
        # set default tab size to 4 characters
        self.font = tkfont.Font(family='Courier New', size=12, weight=tkfont.NORMAL, slant=tkfont.ROMAN, underline=False, overstrike=False)        
        self.text.configure(font=self.font)
        tab_width = self.font.measure(' ' * 4)
        self.text.configure(tabs=(tab_width,))
        self.text.insert(tk.END, self.file.read_text() if self.file.is_file() else '')

        # pack all widget to screen
        self.yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.pack(fill=tk.BOTH, expand=tk.YES)
        self.text_frame.pack(fill=tk.BOTH, expand=tk.YES)

        # add status bar
        self.status_bar = StatusBar(self, self.text)

        # general callback binding
        self.bind("<Control-f>", self.ask_find_next)
        self.bind("<Control-h>", self.ask_find_replace)
        self.bind("<F5>", self.get_datetime)

        # final setup
        self.update_title()

        #self.eval('tk::PlaceWindow . center')
        self.deiconify()

    #---SCROLLBAR CALLBACK-------------------------------------------------------------------------        

    def yscroll(self, event, *args):
        """Move scrollbar when slider is dragged or pointers are clicked"""
        if event == 'moveto':
            self.text.yview_moveto(*args)
        else:
            self.text.yview_scroll(*args)

    #---FILE MENU CALLBACKS------------------------------------------------------------------------

    def new_file(self):
        """Create a new file"""
        # check for content change before opening new file
        self.confirm_changes()

        # reset text widget
        self.text.delete(1.0, tk.END)
        self.file = pathlib.Path.cwd() / 'untitled.txt'
        self.update_title()

    def open_file(self):
        """Open an existing file"""
        # check for content change before opening new file
        self.confirm_changes()

        # open new file
        file = filedialog.askopenfilename(initialdir=self.file.parent, **self.file_defaults)
        if file:
            self.text.delete(1.0, tk.END)  # delete existing content
            self.file = pathlib.Path(file)
            self.text.insert(tk.END, self.file.read_text())
            self.update_title()
            self.status_bar.update_status()

    def save_file(self):
        """Save the currently open file"""
        if self.file.name == 'untitled.txt':
            file = filedialog.asksaveasfilename(initialfile=self.file, **self.file_defaults)
            self.file = pathlib.Path(file) if file else self.file
        self.file.write_text(self.text.get(1.0, tk.END))

    def save_file_as(self):
        """Save the currently open file with a different name or location"""
        file = filedialog.asksaveasfilename(initialdir=self.file.parent, **self.file_defaults)
        if file:
            self.file = pathlib.Path(file)
            self.file.write_text(self.text.get(1.0, tk.END))
            self.update_title()

    def confirm_changes(self):
        """Check to see if content has changed from original file; if so, confirm save"""
        if self.file.is_file():
            original = self.file.read_text()
            current = self.text.get(1.0, tk.END)
            if original != current:
                confirm = messagebox.askyesno(message="Save current file changes?")
                if confirm:
                    self.save_file()
        # new unsaved document with content is prompted to save
        elif self.text.count(1.0, tk.END)[0] > 1:
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

    def undo_edit(self):
        """Undo the last edit in the stack"""
        try:
            self.text.edit_undo()
        except tk.TclError:
            pass

    def redo_edit(self):
        """Redo the last edit in the stack"""
        try:
            self.text.edit_redo()
        except tk.TclError:
            pass

    def text_copy(self):
        """Append selected text to the clipboard"""
        selected = self.text.get(tk.SEL_FIRST, tk.SEL_LAST)
        self.text.clipboard_clear()
        self.text.clipboard_append(selected)

    def text_paste(self):
        """Paste clipboard text into text widget at cursor"""
        self.text.insert(tk.INSERT, self.text.clipboard_get())

    def text_cut(self):
        """Cut selected text and append to clipboard"""
        selected = self.text.get(tk.SEL_FIRST, tk.SEL_LAST)
        self.text.delete(tk.SEL_FIRST, tk.SEL_LAST)
        self.text.clipboard_clear()
        self.text.clipboard_append(selected)

    def ask_find_next(self, event=None):
        """Create find next popup widget"""
        self.findnext = Find(self, self.text)

    def ask_find_replace(self, event=None):
        """Create replace popup widget"""
        self.findreplace = Replace(self, self.text)        

    def select_all(self):
        """Select all text in the text widget"""
        self.text.tag_add(tk.SEL, '1.0', tk.END)

    def get_datetime(self, event=None):
        """insert date and time at cursor position"""
        self.text.insert(tk.INSERT, datetime.datetime.now().strftime("%c"))

    #---FORMAT MENU CALLBACKS------------------------------------------------------------------------

    # TODO `word_wrap` and `block_cursor` will not call from button press... investigating
    def word_wrap(self):
        """Toggle word wrap in text widget"""
        w = self.wrap_var.get()
        if w:
            self.text.configure(wrap=tk.WORD)
        else:
            self.text.configure(wrap=tk.NONE)

    def block_cursor(self):
        """Toggle word wrap in text widget"""
        if self.block_var.get():
            self.text.configure(blockcursor=True)
        else:
            self.text.configure(blockcursor=False)

    def ask_font_select(self):
        """Font selector popup"""
        f = FontSelector(self)
        tab_width = self.font.measure(' ' * 4)
        self.text.configure(tabs=(tab_width,))        

    #---OTHER--------------------------------------------------------------------------------------
    def about_me(self):
        """Application and license info"""
        AboutMe(self)

 
if __name__ == '__main__':
    notepad = Notepad()
    notepad.mainloop()
