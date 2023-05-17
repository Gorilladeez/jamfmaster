import tkinter as tk
import requests
import csv
import os
import time
import datetime


class JamMaster:

    def __init__(self):

        self.cpu_speed = None
        self.os_data = None
        self.storage_data = None
        self.hardware_data = None
        self.data_dump = None
        self.user_data = None
        self.usable_data = None
        self.token = ""
        self.token_expire = ""
        self.response = ""
        self.location = ""
        self.category = ""
        self.name = ""
        self.desc = ""
        self.brand = ""
        self.model = ""
        self.year = ""
        self.screen_size = ""
        self.storage = ""
        self.ram = ""
        self.cpu = ""
        self.os = ""
        self.final_data = ()

        self.window = tk.Tk()
        self.window.title("JAMF Master v1.0")
        self.window.geometry("820x300")
        self.window.resizable(height=0, width=0)
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        self.frame1 = tk.Frame(self.window)
        self.frame2 = tk.Frame(self.window)

        for frame in (self.frame1, self.frame2):
            frame.grid(row=0, column=0, sticky="nsew")

        # ============================== LOGIN PAGE ===============================================
        # Username/Password
        self.username_box = tk.Entry(self.frame1)
        self.username_box.place(relx=0.5, rely=0.4, anchor="center")
        self.username_box.insert(0, "username")
        self.username_box.bind("<Button-1>", self.delete_placeholder)

        self.password_box = tk.Entry(self.frame1, show="*")
        self.password_box.place(relx=0.5, rely=0.5, anchor="center")
        self.password_box.insert(0, "password")
        self.password_box.bind("<Button-1>", self.delete_placeholder)

        # login button
        self.btn_login = tk.Button(self.frame1, text="Log In", font=("Arial", 16), command=self.get_bearer_token)
        self.btn_login.place(relx=0.5, rely=0.6, anchor="center")

        self.lbl_login = tk.Label(self.frame1, text="", font=("Arial", 16))
        self.lbl_login.place(relx=0.5, rely=0.7, anchor="center")

        # ============================= RESULTS PAGE =========================================

        # Searchbar
        self.search_box = tk.Entry(self.frame2)
        self.search_box.place(relx=0.3)

        self.search_btn = tk.Button(self.frame2, text="Search", font=("Arial", 16), command=self.generate_search_results)
        self.search_btn.grid(row=0, column=5, columnspan=2)

        # Labels
        self.lbl_results = tk.Label(self.frame2, text="", font=("Arial", 16, "bold"), width=14)
        self.lbl_results.grid(row=1, column=4, pady=5)

        self.lbl_desc = tk.Label(self.frame2, text="Desc", font=("Arial", 16, "bold", "underline"), width=11)
        self.lbl_desc.grid(row=2, column=0)
        self.lbl_desc_value = tk.Label(self.frame2, text="", font=("Arial", 16))
        self.lbl_desc_value.grid(row=3, column=0, pady=5)

        self.lbl_brand = tk.Label(self.frame2, text="Brand", font=("Arial", 16, "bold", "underline"), width=5)
        self.lbl_brand.grid(row=2, column=1)
        self.lbl_brand_value = tk.Label(self.frame2, text="", font=("Arial", 16))
        self.lbl_brand_value.grid(row=3, column=1, pady=5)

        self.lbl_model = tk.Label(self.frame2, text="Model", font=("Arial", 16, "bold", "underline"), width=6)
        self.lbl_model.grid(row=2, column=2)
        self.lbl_model_value = tk.Label(self.frame2, text="", font=("Arial", 16))
        self.lbl_model_value.grid(row=3, column=2, pady=5)

        self.lbl_year = tk.Label(self.frame2, text="Year", font=("Arial", 16, "bold", "underline"), width=4)
        self.lbl_year.grid(row=2, column=3)
        self.lbl_year_value = tk.Label(self.frame2, text="", font=("Arial", 16))
        self.lbl_year_value.grid(row=3, column=3, pady=5)

        self.lbl_screen_size = tk.Label(self.frame2, text="Screen size", font=("Arial", 16, "bold", "underline"), width=14)
        self.lbl_screen_size.grid(row=2, column=4)
        self.lbl_screen_size_value = tk.Label(self.frame2, text="", font=("Arial", 16))
        self.lbl_screen_size_value.grid(row=3, column=4, pady=5)

        self.lbl_storage = tk.Label(self.frame2, text="Storage", font=("Arial", 16, "bold", "underline"), width=7)
        self.lbl_storage.grid(row=2, column=5)
        self.lbl_storage_value = tk.Label(self.frame2, text="", font=("Arial", 16))
        self.lbl_storage_value.grid(row=3, column=5, pady=5)

        self.lbl_ram = tk.Label(self.frame2, text="RAM", font=("Arial", 16, "bold", "underline"), width=5)
        self.lbl_ram.grid(row=2, column=6)
        self.lbl_ram_value = tk.Label(self.frame2, text="", font=("Arial", 16))
        self.lbl_ram_value.grid(row=3, column=6, pady=5)

        self.lbl_cpu = tk.Label(self.frame2, text="CPU", font=("Arial", 16, "bold", "underline"), width=24)
        self.lbl_cpu.grid(row=2, column=7)
        self.lbl_cpu_value = tk.Label(self.frame2, text="", font=("Arial", 16))
        self.lbl_cpu_value.grid(row=3, column=7, pady=5)

        self.lbl_os = tk.Label(self.frame2, text="OS", font=("Arial", 16, "bold", "underline"), width=14)
        self.lbl_os.grid(row=4, column=4)
        self.lbl_os_value = tk.Label(self.frame2, text="", font=("Arial", 16))
        self.lbl_os_value.grid(row=5, column=4, pady=5)

        self.lbl_serial = tk.Label(self.frame2, text="Serial", font=("Arial", 16, "bold", "underline"), width=14)
        self.lbl_serial.grid(row=4, column=5)
        self.lbl_serial_value = tk.Label(self.frame2, text="", font=("Arial", 16))
        self.lbl_serial_value.grid(row=5, column=5, pady=5)

        self.expire_label = tk.Label(self.frame2, text=self.token_expire, font=("Arial", 16, "bold"), fg="red")
        self.expire_label.place(relx=0.35, rely=0.7)

        self.clipboard_btn = tk.Button(self.frame2, text="Copy Clipboard", font=("Arial", 16), command=self.copy_clipboard)
        self.export_btn = tk.Button(self.frame2, text="Export to CSV", font=("Arial", 16), command=self.export_csv)
        self.clipboard_btn.place(relx=0.3, rely=0.87)
        self.export_btn.place(relx=0.5, rely=0.87)

        self.show_frame(self.frame1)
        self.window.mainloop()

    # ****************************************** END MAIN WINDOW ***************************************************#

    # ******************************************** FUNCTIONS *******************************************************#
    def show_frame(self, frame):
        frame.tkraise()

    def delete_placeholder(self, arg):
        if self.username_box.get() == "username":
            self.username_box.delete(0, tk.END)
        elif self.username_box.get() != "username" and self.password_box.get() == "password":
            self.password_box.delete(0, tk.END)

    def convert_expiration_to_local_time(self, expiration):

        utc_time_str = expiration
        utc_time = datetime.datetime.strptime(utc_time_str[:-1], "%Y-%m-%dT%H:%M:%S.%f")

        utc_timestamp = time.mktime(utc_time.timetuple())
        local_timestamp = utc_timestamp + time.timezone
        local_time = datetime.datetime.fromtimestamp(local_timestamp)

        local_hour = local_time.hour
        local_minute = local_time.minute

        print(local_hour)
        print(local_minute)

        if local_hour >= 12:
            local_hour -= 12
            am_pm = "AM"
        else:
            am_pm = "PM"

        local_time_hour_min = f"{local_hour:02d}:{local_minute:02d} {am_pm}"
        return f"Token Expires: {local_time_hour_min}"

    def get_bearer_token(self):
        username = self.username_box.get()
        password = self.password_box.get()

        url = "https://jamf-gcp.lucasfilm.com/api/v1/auth/token"

        response = requests.post(url, verify=False, auth=(username, password))
        match response.status_code:
            case 200:
                b_token = response.json().get("token")
                expiration = response.json().get("expires")
                self.token = b_token
                self.token_expire = self.convert_expiration_to_local_time(expiration)
                self.expire_label.config(text=self.token_expire)
                self.frame2.tkraise()
            case 401:
                self.lbl_login.config(text="Invalid username/password", fg="red")

    def generate_usable_data(self, data_dump):
        try:
            self.usable_data = []
            self.user_data = data_dump["results"][0]

            for data in self.user_data.items():
                self.usable_data.append(data)

            self.lbl_results.config(text="Results found!", fg="green")
            return self.usable_data
        except:
            self.lbl_results.config(text="No results found!", fg="red")

    def get_model_number(self, identifier):

        model_numbers = {
            # M1/M2 Pros
            "Mac14,10": "A2780",
            "Mac14,6": "A2780",
            "Mac14,9": "A2779",
            "Mac14,5": "A2779",
            "Mac14,7": "A2338",
            "MacBookPro17,1": "A2338",
            "MacBookPro18,1": "A2485",
            "MacBookPro18,2": "A2485",
            "MacBookPro18,3": "A2442",
            "MacBookPro18,4": "A2442",
            # Intel Pros
            "MacBookPro16,1": "A2141",
            "MacBookPro16,4": "A2141",
            "MacBookPro16,2": "A2251",
            "MacBookPro16,3": "A2289",
            "MacBookPro15,4": "A2159",
            "MacBookPro15,3": "A1990",
            "MacBookPro15,1": "A1990",
            "MacBookPro15,2": "A1989",
            "MacBookPro14,3": "A1707",
            "MacBookPro13,3": "A1707",
            "MacBookPro14,2": "A1706",
            "MacBookPro13,2": "A1706",
            "MacBookPro14,1": "A1708",
            "MacBookPro13,1": "A1708",
            "MacBookPro10,1": "A1398",
            "MacBookPro11,2": "A1398",
            "MacBookPro11,3": "A1398",
            "MacBookPro11,4": "A1398",
            "MacBookPro11,5": "A1398",
            "MacBookPro11,1": "A1502",
            "MacBookPro12,1": "A1502",
            "MacBookPro10,2": "A1425",
            "MacBookPro9,2": "A1278",

            # M1/M2 Airs
            "Mac14,2": "A2681",
            "MacBookAir10,1": "A2337",

            # Intel Airs
            "MacBookAir9,1": "A2179",
            "MacBookAir8,2": "A1932",
            "MacBookAir8,1": "A1932",
            "MacBookAir7,2": "A1466",
            "MacBookAir6,2": "A1466",
            "MacBookAir5,2": "A1466",
            "MacBookAir7,1": "A1465",
            "MacBookAir6,1": "A1465",
            "MacBookAir5,1": "A1465",

            # M1/M2 Mac Mini
            "Mac14,12": "A2816",
            "Mac14,3": "A2686",
            "Macmini9,1": "A2348",

            # Intel Mac Mini
            "Macmini8,1": "A1993",
            "Macmini7,1": "A1347",

            # Mac Studio
            "Mac13,2": "A2615",
            "Mac13,1": "A2615",

            # M1 iMac
            "iMac21,2": "A2439",
            "iMac21,1": "A2438",

            # Intel iMac
            "iMac20,2": "A2115",
            "iMac20,1": "A2115",
            "iMac19,1": "A2115",
            "iMac19,2": "A2116",
            "iMacPro1,1": "A1862",
            "iMac18,3": "A1419",
            "iMac17,1": "A1419",
            "iMac15,1": "A1419",
            "iMac14,2": "A1419",
            "iMac13,2": "A1419",
            "iMac18,2": "A1418",
            "iMac18,1": "A1418",
            "iMac16,2": "A1418",
            "iMac16,1": "A1418",
            "iMac14,4": "A1418",
            "iMac14,3": "A1418",
            "iMac14,1": "A1418",
            "iMac13,1": "A1418",

        }

        model = model_numbers.get(identifier)

        return model

    def generate_search_results(self):

        self.serial = self.search_box.get()
        url = f"https://jamf-gcp.lucasfilm.com/api/v1/computers-inventory?section=STORAGE&section=HARDWARE&section" \
              f"=OPERATING_SYSTEM&filter=hardware.serialNumber%3D%3D%22{self.serial}%22 "

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        self.response = requests.get(url, headers=headers, verify=False)

        self.data_dump = self.response.json()
        self.usable_data = self.generate_usable_data(self.data_dump)
        self.hardware_data = self.usable_data[13][1]
        self.storage_data = self.usable_data[7][1]["disks"]
        if len(self.storage_data) > 1:
            self.storage_data = self.compare_storage_disks()
        else:
            self.storage_data = self.usable_data[7][1]["disks"][0]
        self.os_data = self.usable_data[19][1]

        # Description
        self.desc = self.hardware_data["modelIdentifier"].lower()
        if "macbookpro" in self.desc or "14,5" in self.desc or "14,6" in self.desc or "14,7" in self.desc \
                or "14,9" in self.desc or "14,10" in self.desc:
            self.desc = "MacBook Pro"
        elif "macbookair" in self.desc or "14,2" in self.desc:
            self.desc = "MacBook Air"
        elif "imac" in self.desc:
            self.desc = "iMac"
        elif "macmini" in self.desc:
            self.desc = "MacMini"
        elif "mac13,2" in self.desc:
            self.desc = "Mac Studio"
        elif "macpro" in self.desc:
            self.desc = "Mac Pro"

        # Brand
        self.brand = self.hardware_data["make"]

        # Model
        self.model = self.get_model_number(self.hardware_data["modelIdentifier"])

        # Year    
        self.year = self.hardware_data["model"]
        if self.model == "A2779" or self.model == "A2780":
            self.year = "2023"
        elif "2022" in self.year or self.model == "A2338" or self.model == "A2681" or self.model == "A2615":
            self.year = "2022"
        elif "2021" in self.year:
            self.year = "2021"
        elif "2020" in self.year:
            self.year = "2020"
        elif "2019" in self.year:
            self.year = "2019"
        elif "2018" in self.year:
            self.year = "2018"
        elif "2017" in self.year:
            self.year = "2017"
        elif "2016" in self.year:
            self.year = "2016"
        elif "2015" in self.year:
            self.year = "2015"
        elif "2014" in self.year:
            self.year = "2014"
        else:
            self.year = "2013"

        # Screen Size
        if "27-Inch" in self.hardware_data["model"] or "27-inch" in self.hardware_data["model"]:
            self.screen_size = "27\""
        elif "16-Inch" in self.hardware_data["model"] or "16-inch" in self.hardware_data["model"] or \
                "14,6" in self.hardware_data["model"] or "14,10" in self.hardware_data["model"]:
            self.screen_size = "16\""
        elif "15-Inch" in self.hardware_data["model"] or "15-inch" in self.hardware_data["model"]:
            self.screen_size = "15\""
        elif "14-Inch" in self.hardware_data["model"] or "14-inch" in self.hardware_data["model"] or \
                "14,5" in self.hardware_data["model"] or "14,9" in self.hardware_data["model"]:
            self.screen_size = "14\""
        elif "13-Inch" in self.hardware_data["model"] or "13-inch" in self.hardware_data["model"]:
            self.screen_size = "13\""
        elif "MacBook Air" in self.hardware_data["model"] and "Apple M1" in self.hardware_data["processorType"]:
            self.screen_size = "13\""
        else:
            self.screen_size = None

        # Storage size
        if self.storage_data["sizeMegabytes"] >= 1900000:
            self.storage = "2TB"
        elif self.storage_data["sizeMegabytes"] >= 1000000:
            self.storage = "1TB"
        elif self.storage_data["sizeMegabytes"] >= 500000:
            self.storage = "512GB"
        elif self.storage_data["sizeMegabytes"] >= 250000:
            self.storage = "256GB"

        # RAM
        self.ram = self.hardware_data["totalRamMegabytes"]
        if 100000 <= self.ram <= 132000:
            self.ram = "128GB"
        elif 60000 <= self.ram <= 66000:
            self.ram = "64GB"
        elif 30000 <= self.ram <= 33000:
            self.ram = "32GB"
        elif 16000 <= self.ram <= 16600:
            self.ram = "16GB"
        elif 12000 <= self.ram <= 12200:
            self.ram = "12GB"
        elif 8000 <= self.ram <= 8200:
            self.ram = "8GB"
        else:
            self.ram = "4GB"

        # CPU
        self.cpu = self.hardware_data["processorType"]
        self.cpu_speed = self.hardware_data["processorSpeedMhz"]
        if "M1" in self.cpu or "M2" in self.cpu:
            self.cpu = self.cpu[6:].title()
        else:
            self.cpu = f"{self.cpu_speed / 1000:.1f} GHz {self.cpu}"

        # OS
        self.os = self.os_data["version"]
        if self.os.startswith("13"):
            self.os = f"Ventura {self.os}"
        elif self.os.startswith("12"):
            self.os = f"Monterey {self.os}"
        elif self.os.startswith("11"):
            self.os = f"Big Sur {self.os}"
        elif "10.15" in self.os:
            self.os = f"Catalina {self.os}"
        elif "10.14" in self.os:
            self.os = f"Mojave {self.os}"
        elif "10.13" in self.os:
            self.os = f"High Sierra {self.os}"
        elif "10.12" in self.os:
            self.os = f"Sierra {self.os}"

        values_dict = {
            self.lbl_desc_value: self.desc,
            self.lbl_brand_value: self.brand,
            self.lbl_model_value: self.model,
            self.lbl_year_value: self.year,
            self.lbl_screen_size_value: self.screen_size,
            self.lbl_storage_value: self.storage,
            self.lbl_ram_value: self.ram,
            self.lbl_os_value: self.os,
            self.lbl_cpu_value: self.cpu,
            self.lbl_serial_value: self.serial
        }

        for key, value in values_dict.items():
            key.config(text="")
            key.config(text=value)

        self.final_data = (
            self.location, self.category, self.name, self.desc, self.brand, self.model, self.year, self.screen_size,
            self.storage, self.ram, self.cpu, self.os, self.serial)

    def compare_storage_disks(self):
        disk1 = self.usable_data[7][1]["disks"][0]
        disk2 = self.usable_data[7][1]["disks"][1]

        if disk1["sizeMegabytes"] > disk2["sizeMegabytes"]:
            return disk1
        else:
            return disk2

    def copy_clipboard(self):
        clip = ",".join(self.final_data)
        self.window.clipboard_clear()
        self.window.clipboard_append(clip)

    def export_csv(self):
        # write/append to csv file
        documents_path = os.path.expanduser("~/Documents")

        csv_path = os.path.join(documents_path, "cheqroom.csv")
        with open(csv_path, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(self.final_data)


JamMaster()
