import datetime
import os

import block_enter
from tkinter import *
from os.path import expanduser
import Dashboard
import csv
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import matplotlib.dates
from matplotlib.dates import DAILY,WEEKLY,MONTHLY, YEARLY, DateFormatter, rrulewrapper, RRuleLocator, DayLocator, WeekdayLocator, MonthLocator



class TimelineBlock:
    
    def __init__(self, master, dashboard):
        self.ploton = FALSE
        self.dashboard = dashboard

# Setup Timeline Plot
        self.fig = Figure(figsize=(6, 3.4), dpi=100)
        self.tl = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
        self.themaster = dashboard

# Get todays date as yyyymmdd and as integer value
        self.today = dt.datetime.today().strftime("%m/%d/%Y")
        month,day,year = self.today.split('/')
        self.today = int(year + month + day) # yyyymmdd
        self.today_tl = self.create_date(self.today) # integer


    def UpdateGanttChart(self):
        self.tl.clear()

        # Default or selected building
        if self.dashboard.s.build == self.dashboard.e.default:
            self.selected_building = self.dashboard.e.buildings[1]
        else:
            self.selected_building = self.dashboard.s.build
        
        # Default or selected timeframe
        if self.dashboard.s.time == self.dashboard.e.default:
            self.selected_time = self.dashboard.s.times[1]
        else:
            self.selected_time = self.dashboard.s.time

        # Adjust data set to reflect selected building
        self.unit_data = self.dashboard.data.loc[self.dashboard.data['Building'] == self.selected_building]
        self.data = self.unit_data.sort_values(by = ['Unit'])

        # Set end date
        if self.dashboard.s.time == self.dashboard.s.times[0]:
            self.end_date = self.today_tl+14
        elif self.dashboard.s.time == self.dashboard.s.times[1]:
            self.end_date = self.today_tl+30
        elif self.dashboard.s.time == self.dashboard.s.times[2]:
            self.end_date = self.today_tl+90
        elif self.dashboard.s.time == self.dashboard.s.times[3]:
            self.end_date = self.today_tl+round(365/2.0)
        elif self.dashboard.s.time == self.dashboard.s.times[4]:
            self.end_date = self.today_tl+365
        elif self.dashboard.s.time == self.dashboard.s.times[5]:
            self.end_date = self.today_tl+365*3

        # Prepare timeline
        ylabels = []
        for index, row in self.data.iterrows():
            ylabels.append(row['Unit'])
        labels = set(ylabels)
        entries = len(labels)
        pos = np.arange(0.5,entries*0.5+0.5,0.5)
        bar = []

        # Units in building ([ unit, date_in, date_out ])
        for index, row in self.data.iterrows():
            bar.append([row['Unit'],self.create_date(row['Date In']),self.create_date(row['Date Out'])])
        
        # Place bars on timeline
        iter = 0
        for i in range(len(ylabels)):
            if i == 0:
                self.tl.barh((iter*0.5)+0.5, bar[i][2] - bar[i][1], left=bar[i][1], height=0.3, align='center', edgecolor='black', color='orange', alpha = 0.8)
            elif ylabels[i] == ylabels[i-1]:
                self.tl.barh((iter*0.5)+0.5, bar[i][2] - bar[i][1], left=bar[i][1], height=0.3, align='center', edgecolor='black', color='orange', alpha = 0.8)
            else:
                iter += 1
                self.tl.barh((iter*0.5)+0.5, bar[i][2] - bar[i][1], left=bar[i][1], height=0.3, align='center', edgecolor='black', color='orange', alpha = 0.8) 

        # Fromat timeline
        self.tl.set_yticks(pos)
        self.tl.set_yticklabels(labels)
        self.tl.set_ylim(ymin = -0.1, ymax = entries*0.5+0.5)
        self.tl.grid(color = 'g', linestyle = ':')
        self.tl.xaxis_date()

        # Set ticks on timeline
        if self.dashboard.s.time == self.dashboard.s.times[0]:
            rule = rrulewrapper(DAILY, interval=2)
            loc = RRuleLocator(rule)
            self.tl.set_xlim(xmin = self.today_tl - 1 , xmax = self.end_date + 1)
        elif self.dashboard.s.time == self.dashboard.s.times[1]:
            loc = WeekdayLocator(byweekday=0, interval=1, tz=None)
            self.tl.set_xlim(xmin = self.today_tl - 1 , xmax = self.end_date + 1)
        elif self.dashboard.s.time == self.dashboard.s.times[2]:
            loc = WeekdayLocator(byweekday=0, interval=2, tz=None)
            self.tl.set_xlim(xmin = self.today_tl - 3 , xmax = self.end_date + 3)
        elif self.dashboard.s.time == self.dashboard.s.times[3]:
            loc = DayLocator(bymonthday=1, interval=1, tz=None)
            self.tl.set_xlim(xmin = self.today_tl - 7 , xmax = self.end_date + 7)
        elif self.dashboard.s.time == self.dashboard.s.times[4]:
            loc = MonthLocator(bymonth = {1,3,5,7,9,11} , bymonthday=1, interval=1, tz=None)
            self.tl.set_xlim(xmin = self.today_tl - 14 , xmax = self.end_date + 14)
        elif self.dashboard.s.time == self.dashboard.s.times[5]:
            loc = MonthLocator(bymonth = {1,4,7,10} , bymonthday=1, interval=1, tz=None)
            self.tl.set_xlim(xmin = self.today_tl - 31 , xmax = self.end_date + 31)

        formatter = DateFormatter("%d-%b '%y")
        # formatter = DateFormatter("%d-%b")
        # formatter = DateFormatter("%d")

        self.tl.xaxis.set_major_locator(loc)
        self.tl.xaxis.set_major_formatter(formatter)
        # for tick in self.tl.get_xticklabels():
        #     tick.set_rotation(55)
        # labelsx = self.tl.get_xticklabels()
        #         # self.tl.setp(labelsx, rotation=30, fontsize=10) ##
        font = font_manager.FontProperties(size='small')
        self.tl.legend(loc=1,prop=font)
        self.tl.set_title(self.selected_building + '  -  ' + self.selected_time)
        self.tl.invert_yaxis()
        self.fig.autofmt_xdate()
        self.canvas.draw()

    # Outputs date as integer
    def create_date(self,datetxt):
        # Takes in yyyymmdd as string or int
        datetxt = str(datetxt)
        tmp_date = dt.datetime(int(datetxt[0:4]), int(datetxt[4:6]), int(datetxt[6:8]))
        date = matplotlib.dates.date2num(tmp_date) 
        return date

    def read_in_data(self):
        self.filename = self.get_working_addr()
        if self.filename != '':
            self.data = pd.read_csv(self.filename, delimiter=',')
            print(self.data)
            self.ploton = TRUE

    def get_working_addr(self):
        addr = self.dashboard.e.filename
        self.addr = addr
        return self.addr










