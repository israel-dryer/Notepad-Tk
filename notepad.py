import tkinter as tk
from tkinter import font as tkfont
from tkinter import filedialog, messagebox
import pathlib
import datetime

class Notepad(tk.Tk):
    """A notepad application"""
    def __init__(self):
        super().__init__()
        #self.tk_setPalette('#e6e6ea')
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
        self.menu_edit.add_command(label='Find', accelerator='Ctrl+F', command=lambda: FindTextTool(self))
        self.menu_edit.add_command(label='Find Next', accelerator='F3', command=None)
        self.menu_edit.add_command(label='Replace', accelerator='Ctrl+H', command=None)
        self.menu_edit.add_separator()
        self.menu_edit.add_command(label='Select All', accelerator='Ctrl+A', command=None)
        self.menu_edit.add_command(label='Time/Date', accelerator='F5', command=self.get_datetime)

        # format menu
        self.wrap_var = tk.IntVar()
        self.wrap_var.set(True)
        self.block_var = tk.IntVar()
        self.block_var.set(False)
        self.menu_format.add_checkbutton(label='Word Wrap', variable=self.wrap_var, command=None)
        self.menu_format.add_checkbutton(label='Block Cursor', variable=self.block_var, command=None)
        self.menu_format.add_separator()
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
        self.multiline = tk.Text(self, wrap=tk.WORD, font='-size 12', undo=True, maxundo=10,
            autoseparator=True, yscrollcommand=self.yscrollbar.set, blockcursor=False, padx=5, pady=10)
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
        # new unsaved document with content is prompted to save
        elif self.multiline.count(1.0, tk.END)[0] > 1:
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
            self.multiline.edit_undo()
        except tk.EXCEPTION:
            pass

    def redo_edit(self):
        """Redo the last edit in the stack"""
        try:
            self.multiline.edit_redo()
        except tk.EXCEPTION:
            pass

    def text_copy(self):
        """Append selected text to the clipboard"""
        selected = self.multiline.get(tk.SEL_FIRST, tk.SEL_LAST)
        self.multiline.clipboard_clear()
        self.multiline.clipboard_append(selected)

    def text_paste(self):
        """Paste clipboard text into text widget at cursor"""
        self.multiline.insert(tk.INSERT, self.multiline.clipboard_get())

    def text_cut(self):
        """Cut selected text and append to clipboard"""
        selected = self.multiline.get(tk.SEL_FIRST, tk.SEL_LAST)
        self.multiline.delete(tk.SEL_FIRST, tk.SEL_LAST)
        self.multiline.clipboard_clear()
        self.multiline.clipboard_append(selected)

    def get_datetime(self):
        """insert date and time at cursor position"""
        self.multiline.insert(tk.INSERT, datetime.datetime.now().strftime("%c"))        

class FindTextTool(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.root = master
        self.title('Find')
        self.wm_attributes('-topmost', 'true', '-toolwindow', 'true')
        tk.Label(self, text='Find what:', underline=2).grid(row=0, column=0, padx=(10, 5), pady=(10, 0))
        self.input = tk.Entry(self, width=30)
        self.btn_next = tk.Button(self, text='Find Next', underline=0, command=self.find_all_matches)
        self.btn_cancel = tk.Button(self, text='Cancel')

        self.dir_var = tk.IntVar()
        self.dir_var.set(1)
        self.dir_frame = tk.LabelFrame(self, text='Direction')
        self.dir_up = tk.Radiobutton(self.dir_frame, text='Up', underline=0, variable=self.dir_var, value=0)
        self.dir_dw = tk.Radiobutton(self.dir_frame, text='Down', underline=0, variable=self.dir_var, value=1)
        self.match_case = tk.Checkbutton(self, text='Match case', underline=7)

        # add widgets to window
        self.input.grid(row=0, column=1, columnspan=3, sticky=tk.EW, pady=(10, 0), padx=(5, 5))
        self.btn_next.grid(row=0, column=4, sticky=tk.EW, pady=(10, 5), padx=(5, 10), ipadx=5)
        self.btn_cancel.grid(row=1, column=4, sticky=tk.EW, pady=(5), padx=(5, 10), ipadx=5)
        self.dir_frame.grid(row=1, column=2, rowspan=2, columnspan=2, sticky=tk.EW, pady=5, padx=10)
        self.dir_up.pack(side=tk.LEFT)
        self.dir_dw.pack(side=tk.LEFT)
        self.match_case.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(0, 10), padx=10)
        self.matches = []
        self.query = None
        self.input.focus_set()

        # event bindings
        self.btn_next.bind("<F3>", self.goto_next_match)

    def find_all_matches(self):
        """Find and highlight the next matching token from the entry widget"""
        # check to see if a new query has initiated
        new_query = self.input.get()
        if self.query == new_query and self.matches:
            self.goto_next_match()
        else:
            self.query = new_query
            matches = []
            start = 1.0
            while True:
                pos_start = self.root.multiline.search(self.query, start, stopindex=tk.END)
                pos_end = pos_start + f"+{len(self.query)}c"
                if not pos_start:
                    break
                matches.append([pos_start, pos_end])
                start = pos_start + "+1c"
            self.matches = iter(matches)
            self.goto_next_match()

    def goto_next_match(self, event=None):
        """Goto next match in matches"""
        try:
            # remove existing tags
            self.root.multiline.tag_remove(tk.SEL, 1.0, tk.END)
            pos_start, pos_end = next(self.matches)
            self.root.multiline.tag_add(tk.SEL, pos_start, pos_end)
            self.root.multiline.mark_set(tk.INSERT, pos_start)
            self.root.multiline.focus_set()
        except StopIteration:
            self.matches = None

if __name__ == '__main__':
    notepad = Notepad()
    notepad.mainloop()
