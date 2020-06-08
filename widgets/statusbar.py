"""
    Font Selector popup dialogue for text widget

    Author: Israel Dryer
    Modified: 2020-06-07
"""
import tkinter as tk
from tkinter import ttk


class StatusBar(tk.Frame):
    """Status bar that shows text widget statistics"""
    def __init__(self, master, text_widget):
        super().__init__(master, relief=tk.SUNKEN, bd=1)
        self.master = master
        self.text = text_widget
        ttk.Separator(self).pack(fill=tk.X, expand=tk.YES)

        # Line Index
        self.line_var = tk.StringVar()
        self.line_var.set('1')
        tk.Label(self, text='Line:', anchor=tk.W).pack(side=tk.LEFT)
        tk.Label(self, textvariable=self.line_var, anchor=tk.W).pack(side=tk.LEFT)

        # Column Index
        self.col_var = tk.StringVar()
        self.col_var.set('0')
        tk.Label(self, text='Col:', anchor=tk.W).pack(side=tk.LEFT)
        tk.Label(self, textvariable=self.col_var, anchor=tk.W).pack(side=tk.LEFT)

        # Character Count
        self.char_var = tk.StringVar()
        self.char_var.set('0')
        tk.Label(self, text='Chars:', anchor=tk.W).pack(side=tk.LEFT)
        tk.Label(self, textvariable=self.char_var, anchor=tk.W).pack(side=tk.LEFT)

        # Word Count
        self.word_var = tk.StringVar()
        self.word_var.set('0')
        tk.Label(self, text='Words:', anchor=tk.W).pack(side=tk.LEFT)
        tk.Label(self, textvariable=self.word_var, anchor=tk.W).pack(side=tk.LEFT)        

        # Event binding
        self.text.bind("<KeyRelease>", self.update_status)
        self.text.bind("<ButtonRelease-1>", self.update_status)
        self.update_status() # set initial status
        self.pack(side=tk.BOTTOM, fill=tk.X, padx=2, pady=2)        

    def update_status(self, event=None):
        """Update Status Bar"""
        line, col = self.text.index(tk.INSERT).split('.')
        self.line_var.set(line)
        self.col_var.set(col)

        raw_text = self.text.get('1.0', tk.END)
        spaces = raw_text.count(' ')

        char_count = "{:,d}".format(len(raw_text)-spaces)
        self.char_var.set(char_count)

        word_list = [char for char in raw_text.split(' ') if char not in (' ', '', '\n')]
        word_count = "{:,d}".format(len(word_list))
        self.word_var.set(word_count)


class TestWindow(tk.Tk):
    """A window used for testing the various module dialogs"""
    def __init__(self):
        super().__init__()
        self.title('Testing Window')
        self.text = tk.Text(self)
        self.text.pack(fill=tk.BOTH, expand=tk.YES)
        self.text.insert(tk.END, 'This is a test. This is only a test.')
        self.statusbar = StatusBar(self, self.text)

if __name__ == '__main__':

    w = TestWindow()
    w.mainloop()