"""
    Font Selector popup dialogue for text widget

    Author: Israel Dryer
    Modified: 2020-06-07
"""
import tkinter as tk
from tkinter.ttk import Combobox
from tkinter import font

class FontSelector(tk.Toplevel):
    """A font selector popup"""
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.font = master.font
        self.title('Font')
        self.transient(self.master)
        self.resizable(False, False)
        self.wm_attributes('-topmost', 'true', '-toolwindow', 'true')
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.focus_set()

        # get sorted list of fonts families
        fonts = sorted(font.families())
        sizes = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 36, 38, 72]
        
        # create widgets
        self.family = Combobox(self, values=fonts, width=30)
        self.family.set(self.master.font['family'])
        self.size = Combobox(self, values=sizes, width=2)
        self.size.set(self.master.font['size'])
        self.weight = tk.StringVar()
        self.weight.set(self.font['weight'])
        self.weight_cb = tk.Checkbutton(self, text='Bold', anchor=tk.W, variable=self.weight, onvalue='bold', offvalue='normal')
        self.slant = tk.StringVar()
        self.slant.set(self.font['slant'])
        self.slant_cb = tk.Checkbutton(self, text='Slant', anchor=tk.W, variable=self.slant, onvalue='italic', offvalue='roman')
        self.underline = tk.IntVar()
        self.underline.set(self.font['underline'])
        self.underline_cb = tk.Checkbutton(self, text='Underline', anchor=tk.W, variable=self.underline)
        self.overstrike = tk.IntVar()
        self.overstrike.set(self.font['overstrike'])
        self.overstrike_cb = tk.Checkbutton(self, text='Overstrike', anchor=tk.W, variable=self.overstrike)
        self.ok_btn = tk.Button(self, text='OK', command=self.change_font)
        self.cancel_btn = tk.Button(self, text='Cancel', command=self.cancel)

        # arrange widgets on grid
        self.family.grid(row=0, column=0, columnspan=4, sticky=tk.EW, padx=15, pady=15, ipadx=2, ipady=2)
        self.size.grid(row=0, column=4, sticky=tk.EW, padx=15, pady=15, ipadx=2, ipady=2)
        self.weight_cb.grid(row=1, column=0, sticky=tk.EW, padx=15)
        self.slant_cb.grid(row=1, column=1, sticky=tk.EW, padx=15)
        self.underline_cb.grid(row=2, column=0, sticky=tk.EW, padx=15)
        self.overstrike_cb.grid(row=2, column=1, sticky=tk.EW, padx=15)
        self.ok_btn.grid(row=1, column=3, columnspan=2, sticky=tk.EW, ipadx=15, padx=15)
        self.cancel_btn.grid(row=2, column=3, columnspan=2, sticky=tk.EW, ipadx=15, padx=15, pady=(5, 15))

    def change_font(self):
        """Apply font changes to the main text widget"""
        self.font['family'] = self.family.get()
        self.font['size'] = self.size.get()
        self.font['weight'] = self.weight.get()
        self.font['underline'] = self.underline.get()
        self.font['slant'] = self.slant.get()
        self.font['overstrike'] = self.overstrike.get()
        self.master.text.focus()
        self.destroy()

    def cancel(self):
        """Cancel the request and return control to main window"""
        self.master.text.focus()
        self.destroy()


class TestWindow(tk.Tk):
    """A window used for testing the various module dialogs"""
    def __init__(self):
        super().__init__()
        self.title('Testing Window')
        self.font = font.Font(family='Courier New', size=14, weight=font.BOLD, slant=font.ROMAN, underline=False, overstrike=False)
        self.text = tk.Text(self, font=self.font)
        self.text.pack(fill=tk.BOTH, expand=tk.YES)
        self.text.insert(tk.END, 'This is a test. This is only a test.')

if __name__ == '__main__':

    w = TestWindow()
    FontSelector(w)
    w.mainloop()