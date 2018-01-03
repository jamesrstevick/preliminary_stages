# import datetime
import _thread
import csv
import os
import sys
import serial

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog


from block_enter import *
from block_timeline import *
from block_settings import *
from block_asettings import *
from block_availability import *


class Dashboard_GUI(Tk):

    def __init__(self):

        Tk.__init__(self)

        # Settings
        self.log2master = False
        self.iconbitmap('me.ico')

        self.topleft_frame = Frame(self)
        self.topleft_frame.grid(row=0, column=0, sticky= N + W, padx=5, pady=5)

        self.topright_frame = Frame(self)
        self.topright_frame.grid(row=0, column=1, sticky= N + W, padx=5, pady=5)

        # self.bottom_frame = Frame(self)
        # self.bottom_frame.grid(row=1, column=0, sticky=W, padx=5, pady=5)

        # filename = ''

        # self.running = False
        # self.data = []

        # self.port_found = []

        # self.all_sensors = []
        # self.all_connected_sensors = []
        # self.n_connected_sensors = 0


        # Enter Frame
        self.enter_frame = LabelFrame(self.topleft_frame, text="Reservation Spreadsheet")
        self.enter_frame.grid(row=0, column=0, sticky=N +
                            S + W + E, padx=4, pady=4)
        self.e = EnterBlock(self.enter_frame, self)

        # Timeline Settings Frame
        self.tl_settings_frame = LabelFrame(self.topright_frame, text="Calendar View Settings")
        self.tl_settings_frame.grid(row=0, column=0, sticky=N +
                            S + W + E, padx=4, pady=4)
        self.s = TLSettingsBlock(self.tl_settings_frame, self)

        # Timeline Frame
        self.timeline_frame = LabelFrame(self.topright_frame)
        self.timeline_frame.grid(row=1, column=0, sticky=N +
                            S + W + E, padx=4, pady=4)
        self.t = TimelineBlock(self.timeline_frame, self)

        # Availability Settings
        self.a_settings_frame = LabelFrame(self.topright_frame, text="Availability Dates")
        self.a_settings_frame.grid(row=2, column=0, sticky=N +
                            S + W + E, padx=4, pady=4)
        self.a = ASettingsBlock(self.a_settings_frame, self)

        # Availability
        self.availability_frame = LabelFrame(self.topright_frame, text="Available Apartments")
        self.availability_frame.grid(row=3, column=0, sticky=N +
                            S + W + E, padx=4, pady=5)
        self.o = AvailabilityBlock(self.availability_frame, self)





    # dashboard.data always holds the data

    # Load CSV to Data Frame
    def update_df(self):
        self.filename = self.get_working_addr()
        if self.filename != '':
            self.data = pd.read_csv(self.filename, delimiter=',')

    # Get the address of the CSV File
    def get_working_addr(self):
        addr = self.e.filename
        self.addr = addr
        return self.addr
















    def run_all_sensors(self):

        if not os.path.isdir(self.r.get_folderpath()):
            messagebox.showerror(
                'Invalid Path', 'Please choose a folder for data logging.')
            return

        self.connect_all_sensors()

        if len(self.all_connected_sensors) == 0:
            messagebox.showerror(
                'No sensor selected or found', 'Please check settings.')
            return

        self.r.add_sub_folder()
        self.r.interface_disable()
        self.running = True

        print("Running all sensors.")
        for s_block, funhandle in self.all_connected_sensors:
            s_block.interface_disable()
            s_block.write2edf = self.write2edf
            if not s_block.set_filename(self.r.full_path):
                s_block.stop()
                self.n_connected_sensors -= 1
                continue
            _thread.start_new_thread(funhandle, (s_block,))
        _thread.start_new_thread(self.DashboardManager, (1,))
        if self.log2master:
            _thread.start_new_thread(self.PlotManager, (self,))

    def DashboardManager(self, something):
        while self.n_connected_sensors > 0:
            time.sleep(1)
            if not self.running:
                break
        if self.running:
            self.stop_all_sensors()

    def PlotManager(self, master):
        datalimit = 200 * 3600
        if len(self.data) > datalimit:
            del self.data[:-datalimit]
        while self.running:
            time.sleep(5)
            self.plotb.update(master)

    def c_read_one_sensor(self, block):
        try:
            block.sensor_obj.reset_input_buffer()
        except:
            pass
        while self.running:
            if not block.run(self):
                self.n_connected_sensors -= 1
                break
        return

    def tsi_read_one_sensor(self, block):
        while self.running:
            if not block.run(self):
                self.n_connected_sensors -= 1
                break
            time.sleep(1.47)
        return

    def pt_read_one_sensor(self, block):
        try:
            block.sensor_obj.reset_input_buffer()
        except:
            pass
        while self.running:
            if not block.run(self):
                self.n_connected_sensors -= 1
                break
        return

    def hv_read_one_sensor(self, block):
        try:
            block.sensor_obj.reset_input_buffer()
        except:
            pass
        while self.running:
            if not block.run(self):
                self.n_connected_sensors -= 1
                break
        return

    def cb_read_one_sensor(self, block):
        try:
            block.sensor_obj.reset_input_buffer()
        except:
            pass
        while self.running:
            if not block.run(self):
                self.n_connected_sensors -= 1
                break
        return

    def sye_read_one_sensor(self, block):
        try:
            block.sensor_obj.reset_input_buffer()
        except:
            pass
        while self.running:
            if not block.run(self):
                self.n_connected_sensors -= 1
                break
        return

    def sharp_read_one_sensor(self, block):
        try:
            block.sensor_obj.reset_input_buffer()
        except:
            pass
        while self.running:
            if not block.run(self):
                self.n_connected_sensors -= 1
                break
        return

    def stop_all_sensors(self):

        if self.running:
            self.running = False
            time.sleep(1.5)
            for s, funhandle in self.all_connected_sensors:
                s.stop()
            self.all_connected_sensors = list()
        self.r.interface_enable()

if __name__ == "__main__":
    window = Dashboard_GUI()
    window.wm_title("Unit Management System Beta")
    window.resizable(0, 0)
    window.mainloop()
