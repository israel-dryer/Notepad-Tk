"""
    AboutMe popup window to be used in notepad program

    Author: Israel Dryer
    Modified: 2020-06-07
"""
import tkinter as tk
from tkinter.ttk import Separator
import pathlib

class AboutMe(tk.Toplevel):
    """About Me popup widow to display general application description"""

    def __init__(self, master):
        super().__init__(master)
        self.transient(master)
        self.title('About Notepad')
        self.resizable(False, False)
        self.wm_attributes('-topmost', 'true', '-toolwindow', 'true')
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.focus_set()

        # image and application name
        self.img = tk.PhotoImage(file='images/Notepad_32.png')
        self.top_frame = tk.Frame(self)
        lbl1 = tk.Label(self.top_frame, image=self.img, anchor=tk.W)
        lbl2 = tk.Label(self.top_frame, text='Notepad', font=('Arial Black', 16, 'bold'), fg='#444')
        sep = Separator(self, orient=tk.HORIZONTAL)

        # license text widget
        self.gnu = tk.Frame(self)
        self.yscroll = tk.Scrollbar(self.gnu, orient='vertical', command=self.yscroll_callback)
        self.text = tk.Text(self.gnu, wrap='word', width=50, height=10, yscrollcommand=self.yscroll.set)
        mylicense = pathlib.Path('license.txt').read_text()
        self.text.insert(tk.END, mylicense)
        lbl3 = tk.Label(self, text='GNU General Public License')

        # pack widgets to window
        lbl1.pack(side=tk.LEFT, padx=(15, 5), pady=15)
        lbl2.pack(side=tk.LEFT, padx=(5, 15), pady=15)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, expand=tk.YES)
        sep.pack(side=tk.TOP, fill=tk.X, expand=tk.YES)
        lbl3.pack(pady=(10, 0))
        self.text.pack(side=tk.LEFT, padx=(15, 0), pady=15, ipadx=10, ipady=10)
        self.yscroll.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 15), pady=15, expand=tk.YES)
        self.gnu.pack(pady=(0, 0))

        # make text widget 'read-only'
        self.text.configure(state=tk.DISABLED)

    def yscroll_callback(self, event, *args):
        """Move scrollbar when slider is dragged or pointers are clicked"""
        if event == 'moveto':
            self.text.yview_moveto(*args)
        else:
            self.text.yview_scroll(*args)

    def close(self):
        """Close window"""
        self.master.focus_set()
        self.destroy()

class TestWindow(tk.Tk):
    """A window used for testing the various module dialogs"""
    def __init__(self):
        super().__init__()
        self.title('Testing Window')
        self.text = tk.Text(self)
        self.text.pack(fill=tk.BOTH, expand=tk.YES)
        self.text.insert(tk.END, 'This is a test. This is only a test.')


if __name__ == '__main__':

    w = TestWindow()
    AboutMe(w)
    w.mainloop()        