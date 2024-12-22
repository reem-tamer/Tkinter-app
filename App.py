import json
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

class Pet :
    def __init__(self,pet_name,age,species,vaccine_rec):
        self.pet_name =pet_name
        self.age =age
        self.species =species
        self.vaccine_rec = [vaccine_rec]
    def adding_vac_rec(self,vaccine):
        self.vaccine_rec.append(vaccine)

    def pet_turn_dict(self):# turn our object to a dict so json file can handle it(save)
        pet_dict= {"pet_name": self.pet_name, "age": self.age,"vaccine record":self.vaccine_rec}
        return pet_dict




class Owner:
    def __init__(self,owner_name):
        self.owner_name=owner_name
        self.pets=[] #one owner have many pets

    def add_pet(self,pet): #object pet
        self.pet=pet
    def get_pet(self):    #(not sure) get pets list when owner want to make appointment
        return self.pets
    def owner_turn_dict(self): #turns owner object to dictionary for json file and gets pet object after turning it into a dict
        owner_dict= {"owner_name":self.owner_name, "pets": [pet.pet_turn_dict() for pet in self.pets]}
        return owner_dict
class Vet:
    def __init__(self,name,available_appointments):
        self.name=name
        self.available_appointments=available_appointments
        #self.appointments=[]

    # def add_appointments(self,appointment):
    #     self.appointments.append(appointment) #if there is time add a view appointment feature

class Appointment:
    def __init__(self,owner,pet,vet,timeslot,date):
        self.owner=owner
        self.pet=pet
        self.vet=vet
        self.timeslot=timeslot
        self.date=date


class Inventory:
    def __init__(self):
        self.inventory={"Food":100,"Grooming tools":50,"Medications":150,"Pet toys":30,"Pet clothes":20}

    def update_inv(self,item,sales):
        if sales<self.inventory:
            self.inventory[item]-=sales
        else:
            messagebox.showerror("Error","Invalid sales amount, please revise")

    def display_inv(self): #put the key and value in s atring format in a list then turn the list into a string using .join
        display_inv= "\n".join([f"{k}:{v}" for k,v in self.inventory.items()])
        messagebox.showinfo("Available Inventory",display_inv) # put the .join string in a message box


class Receptionist:
    pass



class App(tk.Tk):
    def __init__(self):
        super().__init__()
#hi
#hi nora