from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import datetime


def phase_error():
    messagebox.showerror('Error', 'Failed to receive Lunar Phase info')


def time_error():
    messagebox.showerror('Error', 'Failed to receive Lunar Time info')

class Gui:
    def __init__(self, window):
        self.window = window
        self.window.title('Lunar Phase')

        window_width = self.window.winfo_reqwidth()
        window_height = self.window.winfo_reqheight()
        win_pos_x = int(self.window.winfo_screenwidth() / 2 - window_width)
        win_pos_y = int(self.window.winfo_screenheight() / 2 - window_height)
        self.window.geometry('+{}+{}'.format(win_pos_x, win_pos_y))

        self.month_options = [str(m) for m in range(1, 12 + 1)]
        self.day_options = [str(d) for d in range(1, 31 + 1)]

        self.date = {}

        today = datetime.datetime.today()
        today_y = today.strftime('%Y')
        today_m = today.strftime('%m')
        if today_m[0] == '0':
            today_m = today_m[1]
        today_d = today.strftime('%d')
        if today_d[0] == '0':
            today_d = today_d[1]

        self.choice_var = [StringVar(), StringVar()]

        self.e = Entry(self.window, width=10)
        self.e.insert(0, today_y)
        self.e.grid(row=0, column=0, padx=15, pady=5, sticky='ew')

        self.m1 = OptionMenu(self.window, self.choice_var[0], today_m, *self.month_options)
        self.m1.grid(row=0, column=1, padx=15, pady=5, sticky='ew')

        self.m2 = OptionMenu(self.window, self.choice_var[1], today_d, *self.day_options)
        self.m2.grid(row=0, column=2, padx=15, pady=5, sticky='ew')

        self.enterButton = self.enter_button()
        self.cancelButton = self.cancel_button()

        self.cancel = False

        self.window.mainloop()

    def enter(self):
        self.date['year'] = self.e.get()
        self.date['month'] = self.choice_var[0].get()
        self.date['day'] = self.choice_var[1].get()
        self.check_date()

    def cancel(self):
        self.cancel = True
        self.window.destroy()

    def check_date(self):
        if self.cancel:
            self.window.quit()
            return None
        try:
            datetime.datetime(
                year=int(self.date['year']),
                month=int(self.date['month']),
                day=int(self.date['day'])
            )
            self.window.quit()
            if len(self.date['month']) == 1:
                self.date['month'] = '0' + self.date['month']
            if len(self.date['day']) == 1:
                self.date['day'] = '0' + self.date['day']
            return self.date
        except ValueError:
            messagebox.showwarning('Warning', 'Invalid date input')

    def enter_button(self):
        return Button(self.window, text='Enter', command=self.enter).grid(row=1, column=1, pady=10, padx=5)

    def cancel_button(self):
        return Button(self.window, text='Cancel', command=self.cancel).grid(row=1, column=2, pady=10, padx=5)


def main():
    root = Tk()
    g = Gui(root)


if __name__ == '__main__':
    main()
