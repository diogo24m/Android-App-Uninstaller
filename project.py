from tkinter import StringVar, Tk
from design import Design
import platform
import os
import tkinter as tk

root = Tk()
design = Design(root)

serial_number = ""
apps = []

def main():
    # global app_list
    app_list = []

    list_devices()

    # file = open("sample-data.txt")
    # for line in file:
    #     app_list.append(line.splitlines())
    #     design.app_list_listbox.insert("end", line.splitlines())
    
    root.mainloop()
    
# detect user's OS
def get_OS():
    return platform.system().lower()

def get_adb_folder():
    return os.path.join(os.getcwd(), ("adb\\" + get_OS() + "\\platform-tools"))

def run_command(directory, command):
    command = f"cd {directory} & {command}" 
    p = os.popen(command)
    return p.read()

# get search key
def Scankey(event):
    global apps
    # global app_list
    data = []
    val = event.widget.get()
    # print(val)

    if val == "":
        for app in apps:
            data.append(app)
    else:
        for item in apps:
            if val.lower() in str(item).lower():
                data.append(item)

    Update(data)


design.search_box.bind("<KeyRelease>", Scankey)


# update the listbox
def Update(data):
    global app_list
    design.app_list_listbox.delete(0, "end")

    # put new data
    for item in data:
        design.app_list_listbox.insert("end", item)


def list_devices():
    if run_command(get_adb_folder(), "adb devices").splitlines()[1] == "":
        design.device_chose_cmb.set("No device connected!")
    else:
        response = run_command(get_adb_folder(), "adb devices")
        devices = response.replace("\tdevice", "").splitlines()
        for device in devices:
            if "\tunauthorized" in device:
                device = device.replace('\tunauthorized', '')
                print(f"{device} Nolu cihazın USB hata ayıklama yetkisi yok! Lütfen yetki verin.")
        
        devices = response.splitlines()[1:-1]
        device_numbers = []
        for item in devices:
            if "\tunauthorized" in item:
                device_numbers.append(item.replace("\tunauthorized", ""))
            elif "\tdevice" in item:
                device_numbers.append(item.replace("\tdevice", ""))
        # print(devices)
        # print(device_numbers)
        design.device_chose_cmb['values'] = tuple(device_numbers)
    
design.refresh_devices_btn.config(command=list_devices)


def list_apps():
    global apps
    global serial_number

    design.search_box.delete(0, tk.END)  # Clear existing text
    design.search_box.insert(0, "")  # Insert new text

    if design.device_chose_cmb.get() in ["No device connected!", "Select Your Device"]:
        print("SELECT DEVİCE!!!!!")
    else:
        serial_number = design.device_chose_cmb.get()
        # print(serial_number)
        command = f"adb -s {serial_number} shell pm list packages"
        apps = run_command(get_adb_folder(), command).splitlines()
        for app in apps:
            design.app_list_listbox.insert("end", app)
    
design.refresh_app_list_btn.config(command=list_apps)


def modified_cmb(event):
    global serial_number
    if design.device_chose_cmb.get() not in ["No device connected!", "Select Your Device"]:
        serial_number = design.device_chose_cmb.get()
    list_apps()

design.device_chose_cmb.bind('<<ComboboxSelected>>', modified_cmb)


if __name__ == "__main__":
    main()