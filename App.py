import tkinter as tk
from tkinter import messagebox

class Pet :
    def __init__(self,name,age,species):
        self.name =name
        self.age =age
        self.species =species
        self.vaccination_rec = []
    def adding_vac_rec(self,vaccine):
        self.vaccination_rec.append(vaccine)



class Owner:
    def __init__(self):