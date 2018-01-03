import datetime
import os
import csv
import time

from tkinter import *
from tkinter import messagebox
from os.path import expanduser


class AvailabilityBlock:


    def __init__(self, master, dashboard):

        # PERMANENT FILES
        self.dashboard = dashboard

        # ENTER DATA

        self.date_range_1 = StringVar()
        self.date_range_2 = StringVar()

        self.date_range_1_label = Label(master, textvariable=self.date_range_1)
        self.date_range_1_label.grid(row=0, column=0, padx=0, pady=8, sticky=N+E+S+W)
        self.date_range_1_label.config(font=("Times", 12))

        # self.to_label = Label(master, text="to")
        # self.to_label.grid(row=1, column=0, padx=0, pady=0, sticky=N+E+S+W)
        # self.to_label.config(font=("Times", 8))

        self.date_range_2_label = Label(master, textvariable=self.date_range_2)
        self.date_range_2_label.grid(row=0, column=1, padx=0, pady=8, sticky=N+E+S+W)
        self.date_range_2_label.config(font=("Times", 12))




        self.building1_label = Label(master, text=str(dashboard.e.buildings[0]))
        self.building1_label.grid(row=1, column=0, padx=18, pady=2, sticky=N+E+S+W)
        self.building1_label.config(font=("Courier", 12))

        self.building2_label = Label(master, text=str(dashboard.e.buildings[1]))
        self.building2_label.grid(row=1, column=1, padx=18, pady=2, sticky=N+E+S+W)
        self.building2_label.config(font=("Courier", 12))

        self.building3_label = Label(master, text=str(dashboard.e.buildings[2]))
        self.building3_label.grid(row=1, column=2, padx=18, pady=2, sticky=N+E+S+W)
        self.building3_label.config(font=("Courier", 12))

        self.building4_label = Label(master, text=str(dashboard.e.buildings[3]))
        self.building4_label.grid(row=1, column=3, padx=18, pady=2, sticky=N+E+S+W)
        self.building4_label.config(font=("Courier", 12))

        self.building5_label = Label(master, text=str(dashboard.e.buildings[4]))
        self.building5_label.grid(row=1, column=4, padx=18, pady=2, sticky=N+E+S+W)
        self.building5_label.config(font=("Courier", 12))


        self.avail1 = StringVar()
        self.avail2 = StringVar()
        self.avail3 = StringVar()
        self.avail4 = StringVar()
        self.avail5 = StringVar()

        self.avail1_label = Label(master, textvariable=self.avail1)
        self.avail1_label.grid(row=2, column=0, padx=25, pady=15, sticky=N+E+W)
        self.avail1_label.config(font=("Times", 12))

        self.avail2_label = Label(master, textvariable=self.avail2)
        self.avail2_label.grid(row=2, column=1, padx=25, pady=15, sticky=N+E+W)
        self.avail2_label.config(font=("Times", 12))

        self.avail3_label = Label(master, textvariable=self.avail3)
        self.avail3_label.grid(row=2, column=2, padx=25, pady=15, sticky=N+E+W)
        self.avail3_label.config(font=("Times", 12))

        self.avail4_label = Label(master, textvariable=self.avail4)
        self.avail4_label.grid(row=2, column=3, padx=25, pady=15, sticky=N+E+W)
        self.avail4_label.config(font=("Times", 12))

        self.avail5_label = Label(master, textvariable=self.avail5)
        self.avail5_label.grid(row=2, column=4, padx=25, pady=15, sticky=N+E+W)
        self.avail5_label.config(font=("Times", 12))