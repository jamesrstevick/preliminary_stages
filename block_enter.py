import datetime
import os
import csv

from tkinter import *
from tkinter import messagebox
from os.path import expanduser


class EnterBlock:


    def __init__(self, master, dashboard):

        ### CUSTOMIZE PROGRAM ###
        # Property Names
        self.buildings = ['1716 Rose','1722 Walnut','1446 MLK','88 S Ocean', '100 Ocean']
        # Respective Units
        self.units = [5,9,10,7,1]


        # PERMANENT VARIABLES
        self.dashboard = dashboard
        self.filename=''
        self.base_path = expanduser("~") + '\\Desktop'
        self.me = expanduser("~").split("\\")[-1]
        self.default = 'Click to Select'
        self.fieldnames = ['First Name', 'Last Name', 'E-mail','Phone #', 'Building','Unit','Date In','Date Out','Rent']


        # WORKING FILE
        self.save_label = Label(master, text="Working File (CSV):   ")
        self.save_label.grid(row=0, column=0, sticky=E)

        self.save_addr_entry = Entry(master, width=30)
        self.save_addr_entry.grid(row=0, column=2, padx=4, pady=15)
        

        # ENTER DATA
        self.firstname_label = Label(master, text="First Name:   ")
        self.firstname_label.grid(row=3, column=0, sticky=E)

        self.firstname_entry = Entry(master, width=25)
        self.firstname_entry.grid(row=3, column=1, padx=4, pady=4)

        self.firstname_eg = Label(master, text="[ e.g. John ]")
        self.firstname_eg.grid(row=3, column=2, sticky=W)

        self.lastname_label = Label(master, text="Last Name:   ")
        self.lastname_label.grid(row=4, column=0, sticky=E)

        self.lastname_entry = Entry(master, width=25)
        self.lastname_entry.grid(row=4, column=1, padx=4, pady=4)

        self.lastname_eg = Label(master, text="[ e.g. Smith ]")
        self.lastname_eg.grid(row=4, column=2, sticky=W)

        self.email_label = Label(master, text="E-mail:   ")
        self.email_label.grid(row=5, column=0, sticky=E)

        self.email_entry = Entry(master, width=25)
        self.email_entry.grid(row=5, column=1, padx=4, pady=4)

        self.email_eg = Label(master, text="[ john@smith.com ]")
        self.email_eg.grid(row=5, column=2, sticky=W)

        self.phone_label = Label(master, text="Phone #:   ")
        self.phone_label.grid(row=6, column=0, sticky=E)

        self.phone_entry = Entry(master, width=25)
        self.phone_entry.grid(row=6, column=1, padx=4, pady=4)

        self.phone_eg = Label(master, text="[ 123-456-7890 ]")
        self.phone_eg.grid(row=6, column=2, sticky=W)

        self.building_label = Label(master, text="Building:   ")
        self.building_label.grid(row=7, column=0, sticky=E)

        self.build = StringVar()
        self.build.trace("w", self.get_building)
        self.build.set(self.default)
        self.building_entry = OptionMenu(master, self.build, *self.buildings)
        self.building_entry.grid(row=7, column=1, padx=4, pady=4)

        self.building_eg = Label(master, text="[ e.g. Carriage House ]")
        self.building_eg.grid(row=7, column=2, sticky=W)

        self.unit_label = Label(master, text="Unit:   ")
        self.unit_label.grid(row=8, column=0, sticky=E)

        self.unit_entry = Entry(master, width=25)
        self.unit_entry.grid(row=8, column=1, padx=4, pady=4)

        self.unit_eg = Label(master, text="[ e.g. 3 ]")
        self.unit_eg.grid(row=8, column=2, sticky=W)

        self.datein_label = Label(master, text="Date In:   ")
        self.datein_label.grid(row=9, column=0, sticky=E)

        self.datein_entry = Entry(master, width=25)
        self.datein_entry.grid(row=9, column=1, padx=4, pady=4)

        self.datein_eg = Label(master, text="[ mm/dd/yyyy ]")
        self.datein_eg.grid(row=9, column=2, sticky=W)

        self.dateout_label = Label(master, text="Date Out:   ")
        self.dateout_label.grid(row=10, column=0, sticky=E)

        self.dateout_entry = Entry(master, width=25)
        self.dateout_entry.grid(row=10, column=1, padx=4, pady=4)

        self.dateout_eg = Label(master, text="[ mm/dd/yyyy ]")
        self.dateout_eg.grid(row=10, column=2, sticky=W)

        self.rent_label = Label(master, text="Rent:   ")
        self.rent_label.grid(row=11, column=0, sticky=E)

        self.rent_entry = Entry(master, width=25)
        self.rent_entry.grid(row=11, column=1, padx=4, pady=4)

        self.rent_eg = Label(master, text="[ $/month ]")
        self.rent_eg.grid(row=11, column=2, sticky=W)

        self.enter_label = Label(master, text = "Tenant Entry:   ")
        self.enter_label.grid(row=12, column = 0, sticky = E)

        # BROWSE BUTTON
        self.browse_button = Button(
            master, text="Browse", width=8, command=self.select_folder)
        self.browse_button.grid(row=0, column=1, sticky=W, padx=4, pady=4)

        # ENTER BUTTON
        self.enter_button = Button(
            master, text="Enter", width=8, bg="green", command=self.enable_enter)
        self.enter_button.grid(row=12, column=1,
                             sticky=W, padx=4, pady=4)


    # ENTER DATA
    def enable_enter(self):
        self.enter = True
        while self.enter == True:

            # CHECK THAT FILE IS SELECTED
            if self.filename == '':
                messagebox.showerror("Error", "Browse for working file above")
                self.enter = False
                break

            # COLLECT, CHECK, AND ADJUST ENTRIES
            self.firstname = self.get_firstname()
            if self.firstname == '':
                messagebox.showerror("Error", "First Name Not Entered")
                self.enter = False
                break

            self.lastname = self.get_lastname()
            if self.lastname == '':
                messagebox.showerror("Error", "Last Name Not Entered")
                self.enter = False
                break

            self.email = self.get_email()
            if self.email == '':
                messagebox.showerror("Error", "Email Not Entered")
                self.enter = False
                break

            self.phone = self.get_phone()
            if '-' in self.phone:
                x = self.phone.split('-')
                self.phone = x[0]+x[1]+x[2]
            if self.phone.isdigit()==False:
                messagebox.showerror("Error", "Phone Number Error: Incorrect Format")
                self.enter = False
                break

            self.building = self.get_building()

            self.unit = self.get_unit()
            if self.unit == '':
                messagebox.showerror("Error", "Unit # Not Entered")
                self.enter = False
                break

            self.datein = self.get_datein()
            if self.datein == '':
                messagebox.showerror("Error", "Date In Not Entered")
                self.enter = False
                break
            if "/" in self.datein:    
                x = self.datein.split('/')
                if len(x[0]) == 1:
                    x[0] = '0' + x[0]
                if len(x[1]) == 1:
                    x[1] = '0' + x[1]
                self.datein = x[2] + x[0] + x[1]
                value = x[0] + '/' + x[1] + '/' + x[2]
                self.datein_entry.delete(0, END)
                self.datein_entry.insert(0, value)

            self.dateout = self.get_dateout()
            if self.dateout == '':
                messagebox.showerror("Error", "Date Out Not Entered")
                self.enter = False
                break
            if "/" in self.dateout: 
                x = self.dateout.split('/')
                if len(x[0]) == 1:
                    x[0] = '0' + x[0]
                if len(x[1]) == 1:
                    x[1] = '0' + x[1]
                self.dateout = x[2] + x[0] + x[1]
                value = x[0] + '/' + x[1] + '/' + x[2]
                self.dateout_entry.delete(0, END)
                self.dateout_entry.insert(0, value)

            self.rent = self.get_rent()
            if self.rent == '':
                messagebox.showerror("Error", "Rent Not Entered")
                self.enter = False
                break

            # CHECK ALL FORMATS
            if self.firstname.isalpha() == False:
                messagebox.showerror("Error", "First Name Error: Incorrect Format")
                self.enter = False
                break
            if self.firstname[0].isupper() == False:
                self.firstname_entry.delete(0, END)
                self.firstname = self.firstname.title()
                self.firstname_entry.insert(0, self.firstname)

            if self.lastname.isalpha() == False:
                messagebox.showerror("Error", "Last Name Error: Incorrect Format")
                self.enter = False
                break
            if self.lastname[0].isupper() == False:
                self.lastname_entry.delete(0, END)
                self.lastname = self.lastname.title()
                self.lastname_entry.insert(0, self.lastname)

            if "@" not in self.email:
                messagebox.showerror("Error", "Email Error: Incorrect Format")
                self.enter = False
                break

            if len(self.phone) != 10:
                messagebox.showerror("Error", "Phone Number Error: Must be 10 digits")
                self.enter = False
            
            if not self.building in self.buildings:
                messagebox.showerror("Error", "Building Error: Must be in list")
                self.enter = False

            if self.unit.isdigit()==False:
                messagebox.showerror("Error", "Unit Error: Must be a number")
                self.enter = False

            if self.datein.isdigit()==False:
                messagebox.showerror("Error", "Date In Error: Incorrect Format")
                self.enter = False
                break
            if len(self.datein) != 8:
                messagebox.showerror("Error", "Date In Error: Incorrect format")
                self.enter = False
                break
            if (int(self.datein[4:6]) > 12) or (int(self.datein[6:]) > 31):
                messagebox.showerror("Error", "Date In Error: Check month or day")
                self.enter = False
                break

            if self.dateout.isdigit()==False:
                messagebox.showerror("Error", "Date Out Error: Incorrect Format")
                self.enter = False
                break
            if len(self.dateout) != 8:
                messagebox.showerror("Error", "Date Out Error: Incorrect format")
                self.enter = False
                break
            if (int(self.dateout[4:6]) > 12) or (int(self.dateout[6:]) > 31):
                messagebox.showerror("Error", "Date Out Error: Check month or day")
                self.enter = False
                break

            if self.rent.isdigit() == False:
                messagebox.showerror("Error", "Rent Error: Incorrect Format")
                self.enter = False

            if self.enter == True:
                self.ow2file(self.filename,self.fieldnames,[self.firstname,self.lastname,self.email,self.phone,self.building,self.unit,self.datein,self.dateout,self.rent])
                self.firstname_entry.delete(0, END)
                self.lastname_entry.delete(0, END)
                self.email_entry.delete(0, END)
                self.phone_entry.delete(0, END)
                self.build.set(self.default)
                self.unit_entry.delete(0, END)
                self.datein_entry.delete(0, END)
                self.dateout_entry.delete(0, END)
                self.rent_entry.delete(0, END)
                self.enter = False
                self.dashboard.update_df()



### FUNCTIONS ###

    def set_path(self, value):
        self.save_addr_entry.delete(0, END)
        self.save_addr_entry.insert(0, value)

    def select_folder(self):
        folder_name = filedialog.askdirectory()
        if folder_name != '':
            self.set_path(folder_name)  
        self.create_csv(folder_name)    
        self.set_path(self.filename)
        self.dashboard.update_df()

    def create_csv(self, folder_name):
        self.filename = folder_name + "/"+ self.me + "_apt_database.csv"
        self.filename = self.filename.replace('\\/', '\\').replace('/', '\\')
        file_exists = os.path.isfile(self.filename)
        with open(self.filename, 'a') as file_to_write:
            if file_exists == FALSE:
                writer = csv.DictWriter(
                    file_to_write, fieldnames=self.fieldnames, lineterminator='\n')
                writer.writeheader()

    def ow2file(self, filename, fieldnames, data):
        # file_exists = os.path.isfile(filename)
        with open(filename, 'a') as file_to_update:
            updater = csv.DictWriter(
                file_to_update, fieldnames=fieldnames, lineterminator='\n')
            updater.writerow(dict(zip(fieldnames, data)))


    def get_firstname(self):
        self.firstname = self.firstname_entry.get()
        return self.firstname

    def get_lastname(self):
        self.lastname = self.lastname_entry.get()
        return self.lastname

    def get_email(self):
        self.email = self.email_entry.get()
        return self.email

    def get_phone(self):
        self.phone = self.phone_entry.get()
        return self.phone

    def get_building(self, *args):
        self.building = self.build.get()
        return self.building
        
    def get_unit(self):
        self.unit = self.unit_entry.get()
        return self.unit

    def get_datein(self):
        self.datein = self.datein_entry.get()
        return self.datein

    def get_dateout(self):
        self.dateout = self.dateout_entry.get()
        return self.dateout

    def get_rent(self):
        self.rent = self.rent_entry.get()
        return self.rent

    def get_folderpath(self):
        return self.save_addr_entry.get()


    

























