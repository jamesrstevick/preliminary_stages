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

        











#     # ENTER DATA
#     def enable_enter(self):
#         self.enter = True
#         while self.enter == True:

#             self.building = self.get_building()

#             self.datein = self.get_datein()
#             if self.datein == '':
#                 messagebox.showerror("Error", "Date In Not Entered")
#                 self.enter = False
#                 break
#             if "/" in self.datein:    
#                 x = self.datein.split('/')
#                 if len(x[0]) == 1:
#                     x[0] = '0' + x[0]
#                 if len(x[1]) == 1:
#                     x[1] = '0' + x[1]
#                 self.datein = x[2] + x[0] + x[1]
#                 value = x[0] + '/' + x[1] + '/' + x[2]
#                 self.datein_entry.delete(0, END)
#                 self.datein_entry.insert(0, value)

#             self.dateout = self.get_dateout()
#             if self.dateout == '':
#                 messagebox.showerror("Error", "Date Out Not Entered")
#                 self.enter = False
#                 break
#             if "/" in self.dateout: 
#                 x = self.dateout.split('/')
#                 if len(x[0]) == 1:
#                     x[0] = '0' + x[0]
#                 if len(x[1]) == 1:
#                     x[1] = '0' + x[1]
#                 self.dateout = x[2] + x[0] + x[1]
#                 value = x[0] + '/' + x[1] + '/' + x[2]
#                 self.dateout_entry.delete(0, END)
#                 self.dateout_entry.insert(0, value)


            
#             if not self.building in self.buildings:
#                 messagebox.showerror("Error", "Building Error: Must be in list")
#                 self.enter = False


#             if self.datein.isdigit()==False:
#                 messagebox.showerror("Error", "Date In Error: Incorrect Format")
#                 self.enter = False
#                 break
#             if len(self.datein) != 8:
#                 messagebox.showerror("Error", "Date In Error: Incorrect format")
#                 self.enter = False
#                 break
#             if (int(self.datein[4:6]) > 12) or (int(self.datein[6:]) > 31):
#                 messagebox.showerror("Error", "Date In Error: Check month or day")
#                 self.enter = False
#                 break

#             if self.dateout.isdigit()==False:
#                 messagebox.showerror("Error", "Date Out Error: Incorrect Format")
#                 self.enter = False
#                 break
#             if len(self.dateout) != 8:
#                 messagebox.showerror("Error", "Date Out Error: Incorrect format")
#                 self.enter = False
#                 break
#             if (int(self.dateout[4:6]) > 12) or (int(self.dateout[6:]) > 31):
#                 messagebox.showerror("Error", "Date Out Error: Check month or day")
#                 self.enter = False
#                 break

#             if self.enter == True:
#                 self.ow2file(self.filename,self.fieldnames,[self.firstname,self.lastname,self.email,self.phone,self.building,self.unit,self.datein,self.dateout,self.rent])
#                 self.firstname_entry.delete(0, END)
#                 self.lastname_entry.delete(0, END)
#                 self.email_entry.delete(0, END)
#                 self.phone_entry.delete(0, END)
#                 self.build.set("Click to Select")
#                 self.unit_entry.delete(0, END)
#                 self.datein_entry.delete(0, END)
#                 self.dateout_entry.delete(0, END)
#                 self.rent_entry.delete(0, END)
#                 self.dashboard.update_pd()



# ### FUNCTIONS ###

#     def set_path(self, value):
#         self.save_addr_entry.delete(0, END)
#         self.save_addr_entry.insert(0, value)

#     def select_folder(self):
#         folder_name = filedialog.askdirectory()
#         if folder_name != '':
#             self.set_path(folder_name)  
#         self.create_csv(folder_name)    
#         self.set_path(self.filename)
#         self.dashboard.update_pd()

#     def create_csv(self, folder_name):
#         self.filename = folder_name + "/"+ self.me + "_apt_database.csv"
#         self.filename = self.filename.replace('\\/', '\\').replace('/', '\\')
#         file_exists = os.path.isfile(self.filename)
#         with open(self.filename, 'a') as file_to_write:
#             if file_exists == FALSE:
#                 writer = csv.DictWriter(
#                     file_to_write, fieldnames=self.fieldnames, lineterminator='\n')
#                 writer.writeheader()

#     def ow2file(self, filename, fieldnames, data):
#         # file_exists = os.path.isfile(filename)
#         with open(filename, 'a') as file_to_update:
#             updater = csv.DictWriter(
#                 file_to_update, fieldnames=fieldnames, lineterminator='\n')
#             updater.writerow(dict(zip(fieldnames, data)))


        



























