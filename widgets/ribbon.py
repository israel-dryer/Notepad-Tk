import tkinter as tk
from tkinter import ttk
import pathlib


class Ribbon(tk.Frame):
    """A tool ribbon for easy to access commands"""
    def __init__(self, master):
        super().__init__(master)
        self.images = {}
        for file in pathlib.os.listdir('./images/Medium/'):
            filepath = pathlib.Path() / 'images' / 'Medium' / file
            if filepath.suffix == '.png':
                self.images[filepath.stem] = tk.PhotoImage(file=filepath)

        # File Menu
        Button(self, self.images['new'], command=master.new_file).pack(side=tk.LEFT)
        Button(self, self.images['open'], command=master.open_file).pack(side=tk.LEFT)
        Button(self, self.images['save'], command=master.save_file).pack(side=tk.LEFT)
        Button(self, self.images['save_as'], command=master.save_file_as).pack(side=tk.LEFT)
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y)

        Button(self, self.images['undo'], command=master.undo_edit).pack(side=tk.LEFT)
        Button(self, self.images['redo'], command=master.redo_edit).pack(side=tk.LEFT)
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y)        

        Button(self, self.images['cut'], command=master.text_cut).pack(side=tk.LEFT)
        Button(self, self.images['copy'], command=master.text_copy).pack(side=tk.LEFT)
        Button(self, self.images['paste'], command=master.text_paste).pack(side=tk.LEFT)
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y)

        Button(self, self.images['find'], command=master.ask_find_next).pack(side=tk.LEFT)
        Button(self, self.images['replace'], command=master.ask_find_replace).pack(side=tk.LEFT)
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y)

        wrap_cb = tk.Checkbutton(self, image=self.images['wrap'], indicatoron=False, bd=0,
                                 variable=master.wrap_var, command=master.word_wrap)
        wrap_cb.pack(side=tk.LEFT)
        block_cb = tk.Checkbutton(self, image=self.images['block'], indicatoron=False, bd=0,
                                  variable=master.block_var, command=master.block_cursor)
        block_cb.pack(side=tk.LEFT)

        Button(self, self.images['font'], command=master.ask_font_select).pack(side=tk.LEFT)
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y)

        Button(self, self.images['datetime'], command=master.get_datetime).pack(side=tk.LEFT)        
        Button(self, self.images['about'], command=master.about_me).pack(side=tk.LEFT)
        Button(self, self.images['exit'], command=master.quit_application).pack(side=tk.LEFT)        

        self.pack(side=tk.TOP, fill=tk.X)

        # add overrelief to checkbuttons
        wrap_cb.bind("<Enter>", self.on_enter)
        wrap_cb.bind("<Leave>", self.on_leave)
        block_cb.bind("<Enter>", self.on_enter)
        block_cb.bind("<Leave>", self.on_leave)

    @staticmethod
    def on_enter(event):
        """Execute on mouse enter"""
        widget = event.widget
        widget.configure(relief=tk.RIDGE, bd=1, highlightthickness=0)

    @staticmethod
    def on_leave(event):
        """Execute on mouse leave"""
        widget = event.widget
        widget.configure(relief=tk.FLAT, bd=0, highlightthickness=1)

class Button(tk.Button):
    """Ribbon Button"""
    def __init__(self, master, image, **kwargs):
        super().__init__(master, **kwargs)
        self.image = image
        self['image'] = self.image
        self['relief'] = tk.FLAT
        self['overrelief'] = tk.RIDGE


# class TestWindow(tk.Tk):
#     """A window used for testing the various module dialogs"""
#     def __init__(self):
#         super().__init__()
#         self.title('Testing Window')
#         self.ribbon = Ribbon(self)
#         self.text = tk.Text()
#         self.text.pack(fill=tk.BOTH, expand=tk.YES)
#         self.text.insert(tk.END, 'This is a test. This is onlyatest.')

# if __name__ == '__main__':

#     w = TestWindow()
#     w.mainloop()