import datetime
import os
import csv

from tkinter import *
from tkinter import messagebox
from os.path import expanduser


class TLSettingsBlock:


    def __init__(self, master, dashboard):

        # PERMANENT FILES
        self.dashboard = dashboard
        self.times = ["2 Weeks","1 Month","3 Months","6 Months","1 Year","3 Years"]

        # ENTER DATA

        self.timeframe_label = Label(master, text="Select Timeframe:   ")
        self.timeframe_label.grid(row=0, column=0, padx=4, sticky=E)

        self.timeframe_menu = StringVar()
        self.timeframe_menu.trace("w", self.get_timeframe)
        self.timeframe_menu.set(dashboard.e.default)
        self.timeframe_entry = OptionMenu(master, self.timeframe_menu, *self.times)
        self.timeframe_entry.grid(row=0, column=1, padx=2, pady=4, sticky=W)

        self.space_label = Label(master, text="            ")
        self.space_label.grid(row=0, column=2, sticky=E)

        self.building_label = Label(master, text="Select Building:   ")
        self.building_label.grid(row=0, column=3, padx=2, sticky=E)

        self.building_menu = StringVar()
        self.building_menu.trace("w", self.get_building)
        self.building_menu.set(dashboard.e.default)
        self.build = dashboard.e.buildings
        self.building_entry = OptionMenu(master, self.building_menu, *self.build)
        self.building_entry.grid(row=0, column=4, pady=4 ,sticky=W)

        
        self.update_button = Button(
            master, text="Update", width=8, bg = "green", command=self.save_parameters)
        self.update_button.grid(row=0, column=5, sticky=N+E+S+W, padx=25, pady=10)





    def get_timeframe(self, *args):
        self.timeframe = self.timeframe_menu.get()
        return self.timeframe

    def get_building(self, *args):
        self.building = self.building_menu.get()
        return self.building

    def save_parameters(self):
        self.time = self.get_timeframe()
        self.build = self.get_building()

        self.dashboard.t.UpdateGanttChart()

        self.timeframe_menu.set(self.dashboard.e.default)
        self.building_menu.set(self.dashboard.e.default)




















