import tkinter as tk
import requests
import csv
import os

# test serial - YDWKV9MCQ6
# test imac - D25RD0PMGQ18
# test air - C02DR4YTQ6LT
# test mini - C07Y51GDJYW0

class MyGUI():

    def __init__(self):

        self.token = ""
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
        self.window.geometry("760x300")
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

        # Searchbox
        self.searchbox = tk.Entry(self.frame2)
        self.searchbox.place(relx=0.3)
        #self.searchbox.grid(row=0, column=2, columnspan=2, pady=10)

            
        self.search_btn = tk.Button(self.frame2, text="Search", font=("Arial", 16), command=self.authorize_b_token)
        self.search_btn.grid(row=0,column=6, columnspan=2)

        self.lbl_results = tk.Label(self.frame2, text="", font= ("Arial", 16, "bold"), width=14)
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

        self.lbl_storage = tk.Label(self.frame2, text="Storage", font=("Arial", 16, "bold", "underline"),width=7)
        self.lbl_storage.grid(row=2, column=5)
        self.lbl_storage_value = tk.Label(self.frame2, text="", font=("Arial", 16))
        self.lbl_storage_value.grid(row=3, column=5, pady=5)

        self.lbl_ram = tk.Label(self.frame2, text="RAM", font=("Arial", 16, "bold", "underline"), width=5)
        self.lbl_ram.grid(row=2, column=6)
        self.lbl_ram_value = tk.Label(self.frame2, text="", font=("Arial", 16))
        self.lbl_ram_value.grid(row=3, column=6, pady=5)

        self.lbl_cpu = tk.Label(self.frame2, text="CPU", font=("Arial", 16, "bold", "underline"), width=5)
        self.lbl_cpu.grid(row=2, column=7)
        self.lbl_cpu_value = tk.Label(self.frame2, text="", font=("Arial", 16))
        self.lbl_cpu_value.grid(row=3, column=7, pady=5)

        self.lbl_os = tk.Label(self.frame2, text="OS", font=("Arial", 16, "bold", "underline"), width=7)
        self.lbl_os.grid(row=2, column=8)
        self.lbl_os_value = tk.Label(self.frame2, text="", font=("Arial", 16))
        self.lbl_os_value.grid(row=3, column=8, pady=5)

        self.lbl_serial = tk.Label(self.frame2, text="Serial", font=("Arial", 16, "bold", "underline"), width=14)
        self.lbl_serial.grid(row=2, column=9)
        self.lbl_serial_value = tk.Label(self.frame2, text="", font=("Arial", 16))
        self.lbl_serial_value.grid(row=3, column=9, pady=5)

        self.clipboard_btn = tk.Button(self.frame2, text="Copy Clipboard", font=("Arial", 16), command=self.copy_clipboard)
        self.export_btn = tk.Button(self.frame2, text="Export to CSV", font=("Arial", 16), command=self.export_csv)
        self.clipboard_btn.place(relx=0.6, rely=0.87)
        self.export_btn.place(relx=0.8, rely=0.87)


        
        self.show_frame(self.frame1)
        self.window.mainloop()

    #****************************************** END MAIN WINDOW ***************************************************#

    #******************************************** FUNCTIONS *******************************************************#
    def show_frame(self, frame):
        self.frame1.tkraise()
       
    def delete_placeholder(self, arg):
        if self.username_box.get() == "username":
            self.username_box.delete(0, tk.END)
        elif self.username_box.get() != "username" and self.password_box.get() == "password":
            self.password_box.delete(0, tk.END)

    def get_bearer_token(self):
        username = self.username_box.get()
        password = self.password_box.get()

        url = "https://jamf-gcp.lucasfilm.com/api/v1/auth/token"

        response = requests.post(url, verify=False, auth=(username, password))
        match response.status_code:
            case 200:
                b_token = response.json().get("token")
                self.token = b_token
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


    def authorize_b_token(self):

        self.serial = self.searchbox.get()
        url = f"https://jamf-gcp.lucasfilm.com/api/v1/computers-inventory?section=STORAGE&section=HARDWARE&section=OPERATING_SYSTEM&filter=hardware.serialNumber%3D%3D%22{self.serial}%22"

        headers = {
        "accept": "application/json", 
        "Authorization": f"Bearer {self.token}"
        }
        self.response = requests.get(url, headers=headers, verify=False)

       
        self.data_dump = self.response.json()
        self.usable_data = self.generate_usable_data(self.data_dump)
        self.hardware_data = self.usable_data[13][1]
        self.storage_data = self.usable_data[7][1]["disks"][0]
        self.os_data = self.usable_data[19][1]

        values = (self.lbl_desc_value, self.lbl_brand_value, self.lbl_model_value, self.lbl_year_value, self.lbl_screen_size_value, self.lbl_storage_value,
                  self.lbl_ram_value, self.lbl_cpu_value, self.lbl_os_value, self.lbl_serial_value)
        

        # Description
        self.desc = self.hardware_data["modelIdentifier"].lower()
        if "macbookpro" in self.desc:
            self.desc = "MacBook Pro"
        elif "macbookair" in self.desc:
            self.desc = "MacBook Air"
        elif "imac" in self.desc:
            self.desc = "iMac"
        elif "macmini" in self.desc:
            self.desc = "MacMini"
    
        # Brand
        self.brand = self.hardware_data["make"]

        # Model
        self.model = self.hardware_data["processorType"]
        if "M1 Pro" in self.model:
            self.model = "M1 Pro"
        elif "Apple M1" in self.model and "Air" in self.hardware_data["model"]:
            self.model = "M1 Air"
        elif "iMac" in self.hardware_data["model"]:
            self.model = "iMac"
        else:
            self.model = "Intel"

        # Year    
        self.year = self.hardware_data["model"]
        if "2022" in self.year:
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
        else:
            self.year = "OLD"

        # Screen Size
        if "27-Inch" in self.hardware_data["model"] or "27-inch" in self.hardware_data["model"]:
            self.screen_size = "27\""
        elif "16-Inch" in self.hardware_data["model"] or "16-inch" in self.hardware_data["model"]:
            self.screen_size = "16\""
        elif "14-Inch" in self.hardware_data["model"] or "14-inch" in self.hardware_data["model"]:
            self.screen_size = "14\""
        elif "13-Inch" in self.hardware_data["model"] or "13-inch" in self.hardware_data["model"]:
            self.screen_size = "13\""
        elif "MacBook Air" in self.hardware_data["model"] and "Apple M1" in self.hardware_data["processorType"]:
            self.screen_size = "13\""

        # Storage size
        if self.storage_data["sizeMegabytes"] >= 1000000:
            self.storage = "1TB"
        elif self.storage_data["sizeMegabytes"] >= 500000:
            self.storage = "512GB"
        elif self.storage_data["sizeMegabytes"] >= 250000:
            self.storage = "256GB"
            
        # RAM
        self.ram = self.hardware_data["totalRamMegabytes"]
        if self.ram >= 100000 and self.ram <= 130000:
            self.ram = "128GB"
        elif self.ram >= 60000 and self.ram <= 66000:
            self.ram = "64GB"
        elif self.ram >= 30000 and self.ram <= 33000:
            self.ram = "32GB"
        elif self.ram >= 16000 and self.ram <= 16600:
            self.ram = "16GB"
        elif self.ram >= 12000 and self.ram <= 12200:
            self.ram = "12GB"
        elif self.ram >= 8000 and self.ram <= 8200:
            self.ram = "8GB"
        else:
            self.ram = "4GB"

        self.cpu = "CPU"
        self.os = self.os_data["version"]
        self.serial = self.serial

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

        self.final_data = (self.location, self.category, self.name, self.desc, self.brand, self.model, self.year, self.screen_size, self.storage, self.ram, self.cpu, self.os, self.serial)


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
MyGUI()
