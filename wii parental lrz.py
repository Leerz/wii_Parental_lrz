#!/usr/bin/python
# Wii parental control password reset tool (Windows Forms version)
#
# Copyright 2008-2009 Hector Martin Cantero <hector@marcansoft.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 or version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import Tkinter as tk
import tkMessageBox

class CRC32:
    def __init__(self):
        self.gentable()

    def crc32(self, input, crc=0xffffffff):
        count = len(input)
        i = 0
        while count != 0:
            count -= 1
            temp1 = (crc >> 8) & 0xFFFFFF
            temp2 = self.table[(crc ^ ord(input[i])) & 0xFF]
            crc = temp1 ^ temp2
            i += 1
        return crc

    def gentable(self):
        self.table = []
        for i in range(256):
            crc = i
            for j in range(8):
                if crc & 1:
                    crc = (crc >> 1) ^ 0xEDB88320
                else:
                    crc >>= 1
            self.table.append(crc)

class WiiPasswordResetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wii Parental Control Password Resetter")

        # Confirmation Number
        tk.Label(root, text="Confirmation Number:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.number_entry = tk.Entry(root, width=20)
        self.number_entry.grid(row=0, column=1, padx=10, pady=5)

        # Year Input
        tk.Label(root, text="Year (YY):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.year_var = tk.StringVar()
        self.year_combobox = tk.OptionMenu(root, self.year_var, *["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24"])
        self.year_combobox.grid(row=1, column=1, padx=10, pady=5)
        self.year_var.set("01")

        # Month Input
        tk.Label(root, text="Month (MM):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.month_var = tk.StringVar()
        self.month_combobox = tk.OptionMenu(root, self.month_var, *["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"])
        self.month_combobox.grid(row=2, column=1, padx=10, pady=5)
        self.month_var.set("01")

        # Day Input
        tk.Label(root, text="Day (DD):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.day_var = tk.StringVar()
        self.day_combobox = tk.OptionMenu(root, self.day_var, *["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"])
        self.day_combobox.grid(row=3, column=1, padx=10, pady=5)
        self.day_var.set("01")

        # Submit Button
        self.submit_button = tk.Button(root, text="Get Reset Code", command=self.get_reset_code)
        self.submit_button.grid(row=4, column=0, columnspan=2, pady=10)

    def get_reset_code(self):
        number = self.number_entry.get()
        year = self.year_var.get()
        month = self.month_var.get()
        day = self.day_var.get()

        # Validation
        if not number.isdigit() or len(number) != 8:
            tkMessageBox.showerror("Error", "Please provide a valid 8-digit confirmation number")
            return
        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            tkMessageBox.showerror("Error", "Please provide valid values for year, month, and day")
            return

        # Generate Unlock Code
        date = month + day  # MMDD format
        fullnum = date + number[4:8]
        crc = CRC32().crc32(fullnum)
        code = ((crc ^ 0xaaaa) + 0x14c1) % 100000
        tkMessageBox.showinfo("Reset Code", "Your unlock code: %05d" % code)

if __name__ == "__main__":
    root = tk.Tk()
    app = WiiPasswordResetApp(root)
    root.mainloop()
