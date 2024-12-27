import json
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
from tkinter import Canvas
import smtplib                                      #transfer sending emails from server to another
from email.mime.text import MIMEText                #represent email body as email text
from email.mime.multipart import MIMEMultipart      #create from: to:  message:subject
from dotenv import load_dotenv                      #read key-value pairs from env file
import os                                           #to interact with the file system

load_dotenv()



class Pet:
    def __init__(self, pet_name, age, species, vaccine_rec):
        self.pet_name = pet_name
        self.age = age
        self.species = species
        self.vaccine_rec = [vaccine_rec]

    def adding_vac_rec(self, vaccine):
        self.vaccine_rec.append(vaccine)

    def pet_turn_dict(self):  # turn our object to a dict so json file can handle it(save)
        pet_dict = {"pet_name": self.pet_name, "age": self.age, "vaccination_records": self.vaccine_rec,
                    "species": self.species}
        return pet_dict

    @staticmethod
    def pet_get_dict(owner_data):  # returns the dict back to a class
        pet = Pet(owner_data["pet_name"], owner_data["age"], owner_data.get("vaccination_records", []),
                  owner_data["species"])

        return pet


class Owner:
    def __init__(self, owner_name):
        self.owner_name = owner_name
        self.pets = []  # one owner have many pets

    def add_pet(self, pet):  # object pet
        self.pets.append(pet)

    def get_pet(self):  # (not sure) get pets list when owner want to make appointment
        return self.pets

    def owner_turn_dict(
            self):  # turns owner object to dictionary for json file and gets pet object after turning it into a dict
        owner_dict = {"owner_name": self.owner_name, "pets": [pet.pet_turn_dict() for pet in self.pets]}
        return owner_dict

    @staticmethod
    def get_dict(owner_data):
        owner = Owner(owner_data["owner_name"])
        owner.pets = [Pet.pet_get_dict(pet) for pet in owner_data["pets"]]
        return owner


class Vet:
    def __init__(self, vet_name, available_appointments,email):
        self.vet_name = vet_name
        self.available_appointments = available_appointments
        self.email = email


class Appointment:
    def __init__(self, owner, pet, vet, timeslot):
        self.owner = owner
        self.pet = pet
        self.vet = vet
        self.timeslot = timeslot



class Inventory:
    def __init__(self):
        self.inventory= self.load_inv()

    def display_inv(self):  # put the key and value in s atring format in a list then turn the list into a string using .join
        display_inv = "\n".join([f"{k}:{v}" for k, v in self.inventory.items()])
        messagebox.showinfo("Available Inventory", display_inv)  # put the .join string in a message box


    def save_inv(self):
        with open("inventory.json", "w") as file:
            json.dump(self.inventory, file, indent=4)

    def load_inv(self):
        with open("inventory.json", "r") as file:
            return json.load(file)

    def update_inv(self, item, sales):
        for key, value in self.inventory.items():
            if item == key:
                if sales <= value:
                    self.inventory[item] -= sales
                    self.save_inv()
                    messagebox.showinfo("Update Succesful","Inventory updated")

                else:
                    messagebox.showerror("Error", "Invalid sales amount, please revise")



class Receptionist:
    def __init__(self):
        self.appointments = []
        self.inventory = Inventory()

    def book_appointment(self, owner, pet, vet, timeslot):
        appointment = Appointment(owner, pet, vet, timeslot)
        self.appointments.append(appointment)  # appends the instance of class appointment in the appointments list
        vet.available_appointments.remove(timeslot)  # removes the taken timeslot from the vets available time slots
        messagebox.showinfo("Sucessful booking",
                            f"Appointment booked for {pet.pet_name} with {vet.vet_name} at {timeslot} ")
    def save_appointments(self):
        # Save appointments to JSON
        appointment_data = [
            {
                "owner_name": appointment.owner.owner_name,
                "pet_name": appointment.pet.pet_name,
                "vet_name": appointment.vet.vet_name,
                "timeslot": appointment.timeslot,
            }
            for appointment in self.appointments
        ]
        with open("appointments.json", "w") as file:
            json.dump(appointment_data, file, indent=4)
        messagebox.showinfo("Save Successful", "Appointments have been saved successfully.")

    def load_appointments(self, owners, vets):

        with open("appointments.json", "r") as file:
            appointment_data = json.load(file)

                # Clear existing appointments
            self.appointments = []

            for data in appointment_data:
                    # Find the owner
                owner = None
                for o in owners:
                    if o.owner_name == data["owner_name"]:
                        owner = o


                    # Find the pet
                pet = None
                if owner:
                    for p in owner.pets:
                        if p.pet_name == data["pet_name"]:
                            pet = p


                    # Find the vet
                vet = None
                for v in vets:
                    if v.vet_name == data["vet_name"]:
                        vet = v


                    # Add the appointment if all components are found
                if owner and pet and vet:
                    self.appointments.append(Appointment(owner, pet, vet, data["timeslot"]))



    def view_appointment(self):
        if not self.appointments:
            messagebox.showinfo("Appointment Details", "No appointments booked")
        else:
            appointment_view = "\n".join([
                f'Appointment for {appointment.pet.pet_name} (Owner: {appointment.owner.owner_name}) with {appointment.vet.vet_name} at {appointment.timeslot}'
                for appointment in self.appointments
            ])
            messagebox.showinfo("Appointment Details", appointment_view)




class pet_registration(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Pet Registration")
        self.geometry("800x600")
        self.master = master
        ownerlabel = tk.Label(self, text="Owner Name: ")
        ownerlabel.pack(pady=5)
        self.owner_box = tk.Entry(self)
        self.owner_box.pack(pady=5)

        petlabel = tk.Label(self, text="Pet Name: ")
        petlabel.pack(pady=5)
        self.pet_box = tk.Entry(self)
        self.pet_box.pack(pady=5)

        agelabel = tk.Label(self, text="Pet Age: ")
        agelabel.pack(pady=5)
        self.age_box = tk.Entry(self)
        self.age_box.pack(pady=5)

        recordlabel = tk.Label(self, text="Vaccination Records: ")
        recordlabel.pack(pady=5)
        self.record_box = tk.Entry(self)
        self.record_box.pack(pady=5)

        specieslabel = tk.Label(self, text="Species: ")
        specieslabel.pack(pady=5)
        self.species_box = tk.Entry(self)
        self.species_box.pack(pady=5)

        registerbutton = tk.Button(self, text="Register Pet", command=self.register_pet)
        registerbutton.pack(pady=10)

        back_button = tk.Button(self, text="Back To Main Menu", command= self.back_to_menu)
        back_button.pack(pady=20)



    def register_pet(self):
        owner_name = self.owner_box.get()
        pet_name = self.pet_box.get()

        vaccination_record = self.record_box.get().split(",")
        species = self.species_box.get()
        pet_age = self.age_box.get()

        try:
            pet_age = int(pet_age)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid integer for the pet's age.")
            return

        owner = None
        for existing_owner in self.master.owners:
            if existing_owner is not None:  # to not causes the loop to break when it tries to access owner_name becuase of none
                if existing_owner.owner_name == owner_name:
                    owner = existing_owner

        # check if the owner is in the list
        # if its not it takes the name and makes and instance of it
        # then appends it to the class

        if owner is None:
            owner = Owner(owner_name)
            self.master.owners.append(owner)

        pet = Pet(pet_name, pet_age, species, vaccination_record)
        owner.add_pet(pet)
        self.master.owner_save_data()  # save data in the file
        messagebox.showinfo("Register successful", f"{pet_name} is registered succesfully")

    def back_to_menu (self):
        self.destroy()            #destroy the new window
        self.master.deiconify()   #return the main menu window




class AppointmentBooking(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Appointment Booking")
        self.geometry("800x600")
        self.master = master
        print(self.master.owners)

        owner_label = tk.Label(self, text="Owner Name: ")
        owner_label.pack(pady=5)
        self.owner_choice = tk.StringVar(
            self)  # when we make the drag down menu in the booking appointment window this will show which option was chosen from the drag down

        owner_list_names = [owner.owner_name for owner in self.master.owners if owner is not None]
        if not owner_list_names:
            owner_list_names = ["No Owners Available"]
        self.owner_menu = tk.OptionMenu(self, self.owner_choice,
                                        *owner_list_names)  # *args is syntactical in the menu choice to display all the owners in the list

        self.owner_menu.pack(pady=5)
        self.owner_choice.trace_add("write",
                                    self.update_pet_menu)  # it traces back the owner choice and gives us the chosen owners pets

        pet_label = tk.Label(self, text="Pet Name: ")
        pet_label.pack(pady=5)
        self.pet_choice = tk.StringVar(
            self)  # when we make the drag down menu in the booking appointment window this will show which option was chosen from the drag down
        self.pet_menu = tk.OptionMenu(self, self.pet_choice,
                                      "")  # the value is an empty string because this field will be empty until an owner is chosen
        self.pet_menu.pack(pady=5)

        vet_label = tk.Label(self, text="Vet: ")
        vet_label.pack(pady=5)
        self.vet_choice = tk.StringVar(self)
        self.vet_menu = tk.OptionMenu(self, self.vet_choice, *[vet.vet_name for vet in
                                                               self.master.vets])  # *option menue doesnt read a list and the * so it views it as one value
        self.vet_menu.pack(pady=5)
        self.vet_choice.trace_add("write", self.update_time_slots)

        timeslot_label = tk.Label(self, text=" Timeslot: ")
        timeslot_label.pack(pady=5)
        self.timeslot_choice = tk.StringVar(self)
        self.timeslot_menu = tk.OptionMenu(self, self.timeslot_choice,
                                           "")  # the value is an empty string since the timelsots wont appear except when the vet is chosen
        self.timeslot_menu.pack(pady=5)

        booking_button = tk.Button(self, text="Book Appointment", command=self.booking_appointment)
        booking_button.pack(pady=10)

        back_button = tk.Button(self, text="Back To Main Menu", command=self.back_to_menu)
        back_button.pack(pady=20)



    def update_pet_menu(self,
                        *_):  # using args the _ it helps us ignore the rest of the unneded values lile species,age,vaccination
        chosen_owner = self.owner_choice.get()  # get the chosen owner
        chosen_owner_name = None
        for x in self.master.owners:
            if x.owner_name == chosen_owner:  # compare the owner objects in the list of owners with the string owner choice
                chosen_owner_name = x
                break  # for efficiency to break the loop as solon as owner is found and continue iterating
        if chosen_owner_name:
            pet_names = [pet.pet_name for pet in chosen_owner_name.pets]  # getting the names of an owners pets

            # if after choosing an owner wanting to change our minds and choose another one
            # this is how the pets will be removed to allow space for the new owners pets to be chosen
            self.pet_choice.set(
                "")  # if the owner selection changes this line resets the pet selection and doesnt show the previously selected pet
            # set deletes the pet on the choice bar
            self.pet_menu["menu"].delete(0, "end")  # .delete removes the unwanted pets from the drag down
            for x in pet_names:
                self.pet_menu["menu"].add_command(label=x, command=tk._setit(self.pet_choice,
                                                                             x))  # automatically updates with selected pet name when the user selects the pet from the option menu

    def update_time_slots(self, *_):
        vet_chosen = self.vet_choice.get()
        chosen_vet_name = None
        for x in self.master.vets:
            if x.vet_name == vet_chosen:
                chosen_vet_name = x
                break
        if chosen_vet_name:
            self.timeslot_choice.set("")
            self.timeslot_menu["menu"].delete(0, "end")
            for x in chosen_vet_name.available_appointments:
                self.timeslot_menu["menu"].add_command(label=x, command=tk._setit(self.timeslot_choice, x))

    def booking_appointment(self):
        # get selected choice of everything (final choice)
        selected_owner = self.owner_choice.get()
        selected_pet = self.pet_choice.get()
        selected_vet = self.vet_choice.get()
        selected_timeslot = self.timeslot_choice.get()

        # searches through the list self.master.owners (which holds all the owner objects)
        # to find the one that matches the selected_owner name.
        owner = None
        for x in self.master.owners:
            if x.owner_name == selected_owner:
                owner = x
                break

        # After finding the owner, the code searches through
        # the owner's pets list to find the pet_name that matches the selected pet.
        pet = None
        for y in owner.pets:
            if y.pet_name == selected_pet:
                pet = y
                break

        vet = None
        for z in self.master.vets:
            if z.vet_name == selected_vet:
                vet = z
                break

        # finalizing the appointment and storing it with entered
        # data in the func book_appointmet of receptionist class
        # self.master.receptionist.book_appointment(pet, owner, vet, selected_timeslot)

        # If any of the fields are missing, it shows an error message
        if not selected_owner or not selected_pet or not selected_vet or not selected_timeslot:
            messagebox.showerror("Missing Fields", "All fields must be filled.")
            return

        # update the available timeslots after the appointment is booked
        self.master.receptionist.book_appointment(owner, pet, vet, selected_timeslot)
        self.update_time_slots()
        self.send_email_notification(pet.pet_name,owner.owner_name,selected_timeslot,vet.vet_name)

    def send_email_notification (self,pet_name,owner_name,timeslot,vet_name):
        try:
            email_host = "smtp.gmail.com"                   #server
            email_port = 587                                #standard port for sending email
            sender_email = os.getenv("SENDER_EMAIL")        #sender email is the one who send the email (clinic)
            email_password = os.getenv("EMAIL_PASSWORD")    #SMTP password
            recipient_email =os.getenv("EMAIL_ADDRESS")     #who will recive the email (vet)
            #we save the file into .emv format (all files to not save as a text file)

            if not sender_email or not email_password or not recipient_email:
                raise ValueError("Email credentials or recipient email are not set properly")

            email_subject = "Appointment Reminder"
            email_body = f"""
            Dear {vet_name},
            
            You have a new appointment scheduled :
            Pet Name : {pet_name}
            Owner Name : {owner_name}
            Time : {timeslot}
            
            Regards,
            Fluffy Paws Clinic 
            """


            #intialize email msg that can hold multiple parts
            msg = MIMEMultipart()                               #instance from mumemultipart class
            msg["From"] = sender_email                          #set from field in the email header
            msg["To"] = recipient_email                         #set to field in the email header
            msg["Subject"] = email_subject                      #set subject field in the email header
            msg.attach(MIMEText(email_body,"plain"))    #create mimetext object using email body string
                                                                # and specify the dormat as plain(not HTML)


            #enable commmunication with an email server
            with smtplib.SMTP(email_host,email_port) as server :    #create a connection to the SMTP server
                server.starttls()                                   #secure the communication
                server.login(sender_email,email_password)           #send the email and password to SMTP server
                server.send_message(msg)                            #send the email msg to reciever

            print(f"Email sen successfully to {recipient_email}")
        except Exception as error :
            print(f"Error sending email: {error}")



    def back_to_menu(self):
        self.destroy()             #distroy the new window
        self.master.deiconify()    #return the main menu window



class Inventory_management(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Inventory Management")
        self.geometry("800x600")
        self.master = master

        items_label = tk.Label(self, text="Select Item:")
        items_label.pack(pady=5)
        self.item_choice = tk.StringVar(self)
        self.item_menu = tk.OptionMenu(self, self.item_choice, *self.master.receptionist.inventory.inventory.keys())
        self.item_menu.pack(pady=5)

        quantitysold_label = tk.Label(self, text="Quantity Sold:")
        quantitysold_label.pack(pady=5)
        self.quantity_entry = tk.Entry(self)
        self.quantity_entry.pack(pady=5)

        update_button= tk.Button(self, text="Update Inventory", command=lambda: self.update_inventory())
        update_button.pack(pady=10)

                                                                        #instance from receptionist class and inside the
                                                                        #receptionist class we made instance from inventory class to
                                                                        #get the func display_inv from inventory class
        view_button = tk.Button(self, text="View Inventory", command=lambda: self.master.receptionist.inventory.display_inv())
        view_button.pack(pady=10)

        back_button = tk.Button(self, text="Back To Main Menu", command=self.back_to_menu)
        back_button.pack(pady=20)


    def update_inventory(self):
        try:
            item = self.item_choice.get()
            sales = int(self.quantity_entry.get())
            self.master.receptionist.inventory.update_inv(item, sales)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for Quantity Sold.")

    def back_to_menu(self):
        self.destroy()             #distroy the new window
        self.master.deiconify()    #return the main menu window



class App(tk.Tk):
    def __init__(self):

        super().__init__()
        self.geometry("800x670")  # no instance for the window
        self.title("Fluffy Paws Clinic and Shop")

        self.background_image_path = "Wallpaper.png"  # Replace with your image file path
        self.background_image = Image.open(self.background_image_path)
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.background_photo)

        icon= PhotoImage(file="pet_icon.png")
        self.iconphoto(True,icon)

        self.vets = [Vet("DR. Ahmed Anwar", ["6:00pm", "7:00pm", "8:00pm"],"ahmed.anwer@example.com"),
                     Vet("DR. Alex Johns", ["6:00pm", "7:00pm", "8:00pm"],"alex.johns@example.com")]
        self.owners = []
        self.owner_load_data()
        self.main_menu()
        self.receptionist = Receptionist()
        self.receptionist.load_appointments(self.owners, self.vets)  # Load appointments


    def main_menu(self):
        register_pet_button = tk.Button(self, text="Register Pet", command=self.registration_button)
        register_pet_button.pack(pady=10)
        self.canvas.create_window(400,100,window=register_pet_button)

        appointment_booking_button = tk.Button(self, text="Book Appointment", command=self.appointment_booking_button)
        appointment_booking_button.pack(pady=10)
        self.canvas.create_window(400, 160, window=appointment_booking_button)

        save_appointments_button = tk.Button(self, text="Save Appointment",
                                            command=lambda: self.receptionist.save_appointments())
        save_appointments_button.pack(pady=10)
        self.canvas.create_window(400, 230, window=save_appointments_button)

        view_appointments_button = tk.Button(self, text="View Appointments", command=self.view_appointments_button)
        view_appointments_button.pack(pady=10)
        self.canvas.create_window(400, 280, window=view_appointments_button)

        inventory_button= tk.Button(self, text="Inventory Management", command=self.inventory_button)
        inventory_button.pack(pady=10)
        self.canvas.create_window(400, 340, window=inventory_button)

        exit_button = tk.Button(self, text="Exit", command=self.quit)
        exit_button.pack(pady=10)
        self.canvas.create_window(400, 400, window=exit_button)



    def registration_button(self):
        self.withdraw()      #hide the main menu window
        pet_registration(self)

    def appointment_booking_button(self):
        self.withdraw()
        AppointmentBooking(self)

    def view_appointments_button(self):
        # self.withdraw()
        self.receptionist.view_appointment()

    def inventory_button(self):
        self.withdraw()
        Inventory_management(self)



    def owner_save_data(self):
        with open("owner_data.json", "r") as file:
            owner_data = json.load(file)
        owner_data["owners"].extend([owner.owner_turn_dict() for owner in self.owners if owner is not None])
        # taking every owner object in the list of owners if it's not empty as  a dict and append it in the json file
        with open("owner_data.json", "w") as file:
            json.dump(owner_data, file, indent=4)

    def owner_load_data(self):
        with open("owner_data.json", "r") as file:
            owner_data = json.load(file)
            cumilative_owner_list = [Owner.get_dict(owner) for owner in owner_data.get("owners")]
            self.owners.extend(cumilative_owner_list)
            # looping over the dictionary we have of the json file
            # and converting it into an object using the static method get_dict in the owner class
            # and append it in the owner list





if __name__ == "__main__":
    app = App()
    app.mainloop()
