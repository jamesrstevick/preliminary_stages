import datetime
import os
import csv
import time
import pandas as pd

from tkinter import *
from tkinter import messagebox
from os.path import expanduser


class ASettingsBlock:


    def __init__(self, master, dashboard):

        # PERMANENT FILES
        self.dashboard = dashboard

        # ENTER DATA
        self.entertime1_label = Label(master, text="Enter Timeframe:   ")
        self.entertime1_label.grid(row=0, column=0, padx=4, sticky=E)

        self.entertime1_entry = Entry(master, width=19)
        self.entertime1_entry.grid(row=0, column=1, padx=4, pady=4)

        self.entertime2_label = Label(master, text="to")
        self.entertime2_label.grid(row=0, column=2, padx=4, sticky=E)

        self.entertime2_entry = Entry(master, width=19)
        self.entertime2_entry.grid(row=0, column=3, padx=4, pady=4)

        
        self.update_button = Button(
            master, text="Update", width=8, bg = "green", command=self.available_rooms)
        self.update_button.grid(row=0, column=4, sticky=W, padx=25, pady=10)


    def get_entertime1(self):
        self.entertime1 = self.entertime1_entry.get()
        return self.entertime1

    def get_entertime2(self):
        self.entertime2 = self.entertime2_entry.get()
        return self.entertime2

    def date_swap(self,date):
        date = str(date)
        return int(date[4:8]+date[0:2]+date[2:4])

    def available_rooms(self):
        data = self.dashboard.data.copy()
        self.availability = True
        while self.availability == True:

            self.starttime = self.get_entertime1()
            if self.starttime == '':
                messagebox.showerror("Error", "Date In Not Entered")
                self.availability = False
                break
            elif "/" in self.starttime:    
                x = self.starttime.split('/')
                if len(x[0]) == 1:
                    x[0] = '0' + x[0]
                if len(x[1]) == 1:
                    x[1] = '0' + x[1]
                self.starttime = x[2] + x[0] + x[1]
                self.format_date_1 = x[0] + '/' + x[1] + '/' + x[2]
                self.entertime1_entry.delete(0, END)
                self.entertime1_entry.insert(0, self.format_date_1)

            self.endtime = self.get_entertime2()
            if self.endtime == '':
                messagebox.showerror("Error", "Date Out Not Entered")
                self.availability = False
                break
            elif "/" in self.endtime:    
                x = self.endtime.split('/')
                if len(x[0]) == 1:
                    x[0] = '0' + x[0]
                if len(x[1]) == 1:
                    x[1] = '0' + x[1]
                self.endtime = x[2] + x[0] + x[1]
                self.format_date_2 = x[0] + '/' + x[1] + '/' + x[2]
                self.entertime2_entry.delete(0, END)
                self.entertime2_entry.insert(0, self.format_date_2)

            # Set date range variable for AvailabilityBlock
            self.dashboard.o.date_range_1.set("From :  {}".format(self.format_date_1))
            self.dashboard.o.date_range_2.set("To :  {}".format(self.format_date_2))

            # Turn start and end into integer dates
            self.starttime = self.dashboard.t.create_date(self.starttime)
            self.endtime = self.dashboard.t.create_date(self.endtime)

            if self.starttime >= self.endtime:
                messagebox.showerror("Error", "End date must be after start date")
                self.availability = False
                break


            # self.avail_data = []
            # for build in self.dashboard.e.buildings:
            #     self.avail_data.append(self.dashboard.data.loc[self.dashboard.data['Building'] == build])
            # for idx,df in enumerate(self.avail_data):
            #     print(df['Date In'])
            #     if df['Date In'][0] != '':
            #         self.avail_data[idx] = df.loc[(self.dashboard.t.create_date(df['Date In']) >= self.dashboard.t.create_date(self.starttime))]

            # Add two columns to data frame with dates as integers
            date1 = data['Date In'].tolist()
            for idx,date in enumerate(date1):
                date1[idx] = self.dashboard.t.create_date(date)
            date2 = data['Date Out'].tolist()
            for idx,date in enumerate(date2):
                date2[idx] = self.dashboard.t.create_date(date)

            data['Date1'] = pd.Series(date1).values    
            data['Date2'] = pd.Series(date2).values 
        

            # Apts with out data
            total_1 = data[data['Building']==self.dashboard.e.buildings[0]].sort_values(by = ['Unit'])
            total_2 = data[data['Building']==self.dashboard.e.buildings[1]].sort_values(by = ['Unit'])
            total_3 = data[data['Building']==self.dashboard.e.buildings[2]].sort_values(by = ['Unit'])
            total_4 = data[data['Building']==self.dashboard.e.buildings[3]].sort_values(by = ['Unit'])
            total_5 = data[data['Building']==self.dashboard.e.buildings[4]].sort_values(by = ['Unit'])

            all_apts_1 = list(range(1,self.dashboard.e.units[0]+1))
            all_apts_2 = list(range(1,self.dashboard.e.units[1]+1))
            all_apts_3 = list(range(1,self.dashboard.e.units[2]+1))
            all_apts_4 = list(range(1,self.dashboard.e.units[3]+1))
            all_apts_5 = list(range(1,self.dashboard.e.units[4]+1))

            no_data_1 = set(all_apts_1) - set(total_1['Unit'].tolist())
            no_data_2 = set(all_apts_2) - set(total_2['Unit'].tolist())
            no_data_3 = set(all_apts_3) - set(total_3['Unit'].tolist())
            no_data_4 = set(all_apts_4) - set(total_4['Unit'].tolist())
            no_data_5 = set(all_apts_5) - set(total_5['Unit'].tolist())



            # Dataframe of available apartments
            data1 = data[(data['Date1'] >= self.endtime)]
            data2 = data[(data['Date2'] <= self.starttime)]
            data = pd.concat([data1, data2], axis=0)

            avail_1 = data[data['Building']==self.dashboard.e.buildings[0]].sort_values(by = ['Unit'])
            avail_2 = data[data['Building']==self.dashboard.e.buildings[1]].sort_values(by = ['Unit'])
            avail_3 = data[data['Building']==self.dashboard.e.buildings[2]].sort_values(by = ['Unit'])
            avail_4 = data[data['Building']==self.dashboard.e.buildings[3]].sort_values(by = ['Unit'])
            avail_5 = data[data['Building']==self.dashboard.e.buildings[4]].sort_values(by = ['Unit'])

            avail_1 = set(avail_1['Unit'].tolist()).union(no_data_1)
            avail_2 = set(avail_2['Unit'].tolist()).union(no_data_2)
            avail_3 = set(avail_3['Unit'].tolist()).union(no_data_3)
            avail_4 = set(avail_4['Unit'].tolist()).union(no_data_4)
            avail_5 = set(avail_5['Unit'].tolist()).union(no_data_5)


            # Create display strings
            str1=''
            str2=''
            str3=''
            str4=''
            str5=''

            apt_lists = [avail_1,avail_2,avail_3,avail_4,avail_5]
            apt_strings = [str1,str2,str3,str4,str5]

            for idx,lists in enumerate(apt_lists):
                for elem in lists:
                    apt_strings[idx]+= str(elem) + '\n'

            # Set display strings
            self.dashboard.o.avail1.set(apt_strings[0])
            self.dashboard.o.avail2.set(apt_strings[1])
            self.dashboard.o.avail3.set(apt_strings[2])
            self.dashboard.o.avail4.set(apt_strings[3])
            self.dashboard.o.avail5.set(apt_strings[4])

            self.entertime1_entry.delete(0, END)
            self.entertime2_entry.delete(0, END)
            self.availability = False