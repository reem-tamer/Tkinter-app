import json
import tkinter as tk
from tkinter import messagebox


class Pet:
    def __init__(self, pet_name, age, species, vaccine_rec):
        self.pet_name = pet_name
        self.age = age
        self.species = species
        self.vaccine_rec = [vaccine_rec]

    def adding_vac_rec(self, vaccine):
        self.vaccine_rec.append(vaccine)

    def pet_turn_dict(self):  # turn our object to a dict so json file can handle it(save)
        pet_dict = {"pet_name": self.pet_name, "age": self.age, "vaccination_records": self.vaccine_rec,"species":self.species}
        return pet_dict
    @staticmethod
    def pet_get_dict(owner_data): # returns the dict back to a class
        return Pet(owner_data["pet_name"],owner_data["age"],owner_data.get("vaccination_records",[]),owner_data["species"])


class Owner:
    def __init__(self, owner_name):
        self.owner_name = owner_name
        self.pets = []  # one owner have many pets

    def add_pet(self, pet):  # object pet
        self.pets.append(pet)

    def get_pet(self):  # (not sure) get pets list when owner want to make appointment
        return self.pets

    def owner_turn_dict(self):  # turns owner object to dictionary for json file and gets pet object after turning it into a dict
        owner_dict = {"owner_name": self.owner_name, "pets": [pet.pet_turn_dict() for pet in self.pets]}
        return owner_dict
    @staticmethod
    def get_dict(owner_data):
        owner=Owner(owner_data["owner_name"])
        owner.pets=[Pet.pet_get_dict(pet) for pet in owner_data["pets"]]

class Vet:
    def __init__(self, vet_name, available_appointments):
        self.vet_name = vet_name
        self.available_appointments = available_appointments
        # self.appointments=[]

    # def add_appointments(self,appointment):
    #     self.appointments.append(appointment) #if there is time add a view appointment feature


class Appointment:
    def __init__(self, owner, pet, vet, timeslot, date):
        self.owner = owner
        self.pet = pet
        self.vet = vet
        self.timeslot = timeslot
        self.date = date


class Inventory:
    def __init__(self):
        self.inventory = {"Food": 100, "Grooming tools": 50, "Medications": 150, "Pet toys": 30, "Pet clothes": 20}

    def display_inv(
            self):  # put the key and value in s atring format in a list then turn the list into a string using .join
        display_inv = "\n".join([f"{k}:{v}" for k, v in self.inventory.items()])
        messagebox.showinfo("Available Inventory", display_inv)  # put the .join string in a message box
        print(display_inv)

    def update_inv(self, item, sales):

        for key, value in self.inventory.items():
            if item == key:
                if sales < value:
                    self.inventory[item] -= sales
                else:
                    messagebox.showerror("Error", "Invalid sales amount, please revise")


class Receptionist:
    def __init__(self):
        self.appointments = []
        self.inventory = Inventory()

    def book_appointment(self, pet, owner, vet, timeslot):
        appointment = Appointment(pet, owner, vet, timeslot)
        self.appointments.append(appointment)  # appends the instance of class appointment in the appointments list
        vet.available_appointments.remove(timeslot)  # removes the taken timeslot from the vets available time slots
        messagebox.showinfo("Sucessful booking",
                            f"Appointment booked for {pet.pet_name} with {vet.vet_name} at {timeslot} ")

    def view_appointment(self):  # so the receptionist is able to view the appointments everyday
        if not self.appointments:  # if we have no appointments
            messagebox.showinfo("Appointment Details", "No appointments booked")
        else:
            appointment_view = "\n".join(
                [f'{appointment.pet.pet_name} with {appointment.vet.vet_name} at {appointment.timeslot}' for appointment
                 in self.appointments])
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
            if existing_owner is not None :  #to not causes the loop to break when it tries to access owner_name becuase of none
                if existing_owner.owner_name == owner_name:
                    owner = existing_owner
                    break
        # check if the owner is in the list
        # if its not it takes the name and makes and instance of it

        # then appends it to the class


        if owner is None:
            owner = Owner(owner_name)
            self.master.owners.append(owner)


        pet = Pet(pet_name, pet_age, species, vaccination_record)
        owner.add_pet(pet)
        self.master.owner_save_data()  #save data in the file
        messagebox.showinfo("Register successful", f"{pet_name} is registered succesfully")




class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")  # no instance for the window
        self.title("Fluffy Paws Clinic and Shop")
        self.vets = [Vet("DR. Ahmed Anwar", ["6:00pm", "7:00pm", "8:00pm"]),
                     Vet("DR. Alex Johns", ["6:00pm", "7:00pm", "8:00pm"])]
        self.owners = []
        self.owner_load_data()
        self.main_menu()

    def main_menu(self):
        register_pet_button = tk.Button(self, text="Register Pet", command=self.registration_button)
        register_pet_button.pack(pady=10)

    def registration_button(self):
        pet_registration(self)

    def owner_save_data(self):
        with open("owner_data.json", "r") as file:
            owner_data = json.load(file)
        owner_data["owners"].extend([owner.owner_turn_dict() for owner in self.owners if owner is not None])
#taking every owner object in the list of owners if it's not empty and turn them into an dict to enable saving them in json file
        with open("owner_data.json","w") as file:
            json.dump(owner_data,file, indent=4)

    def owner_load_data(self):
        with open("owner_data.json","r")as file:
            owner_data = json.load(file)
            self.owners = [Owner.get_dict(owner) for owner in owner_data.get("owners")]  #looping over the dictionary we have of the json file
            # and converting it into an object using the static method get_dict in the owner class

if __name__ == "__main__":
    app = App()
    app.mainloop()
