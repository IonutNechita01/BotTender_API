import tkinter as tk
from tkinter import messagebox, simpledialog
import json
from threading import Thread
from models.ingredient_model import IngredientModel
from utils.constants import Response
from bottender.bot_tender import BotTender

class BotTenderUI:
    def __init__(self, master):
        self.master = master
        master.title("BotTender")

        self.bot_tender = BotTender()

        # Status Label
        self.status_label = tk.Label(master, text="Status: Loading...", font=("Helvetica", 14))
        self.status_label.pack()

        # Refresh Button
        self.refresh_button = tk.Button(master, text="Refresh Status", command=self.refresh_status)
        self.refresh_button.pack()

        # Available Ingredients List
        self.ingredients_label = tk.Label(master, text="Available Ingredients", font=("Helvetica", 14))
        self.ingredients_label.pack()

        self.ingredients_listbox = tk.Listbox(master, width=50)
        self.ingredients_listbox.pack()

        # Add Ingredient Button
        self.add_ingredient_button = tk.Button(master, text="Add Ingredient", command=self.add_ingredient)
        self.add_ingredient_button.pack()

        # Remove Ingredient Button
        self.remove_ingredient_button = tk.Button(master, text="Remove Ingredient", command=self.remove_ingredient)
        self.remove_ingredient_button.pack()

        # Prepare Cocktail Button
        self.prepare_cocktail_button = tk.Button(master, text="Prepare Cocktail", command=self.prepare_cocktail)
        self.prepare_cocktail_button.pack()

        # Initial refresh
        self.refresh_status()

    def refresh_status(self):
        status = self.bot_tender.getStatus()
        self.status_label.config(text=f"Status: {status['status']}")
        self.update_ingredients_list()

    def update_ingredients_list(self):
        self.ingredients_listbox.delete(0, tk.END)
        for ingredient in self.bot_tender.availableIngredients:
            self.ingredients_listbox.insert(tk.END, f"{ingredient.name} - {ingredient.quantity}")

    def add_ingredient(self):
        name = simpledialog.askstring("Input", "Enter ingredient name:")
        quantity = simpledialog.askfloat("Input", "Enter ingredient quantity:")
        position = simpledialog.askinteger("Input", "Enter ingredient position:")

        if name and quantity is not None and position is not None:
            ingredient = IngredientModel(name=name, quantity=quantity, position=position)
            response = self.bot_tender.addIngredient(ingredient)
            if response["status"] == Response.SUCCESS:
                messagebox.showinfo("Success", "Ingredient added successfully.")
                self.refresh_status()
            else:
                messagebox.showerror("Error", "Failed to add ingredient.")

    def remove_ingredient(self):
        position = simpledialog.askinteger("Input", "Enter ingredient position to remove:")

        if position is not None:
            ingredient = IngredientModel(position=position)
            response = self.bot_tender.removeIngredient(ingredient)
            if response["status"] == Response.SUCCESS:
                messagebox.showinfo("Success", "Ingredient removed successfully.")
                self.refresh_status()
            else:
                messagebox.showerror("Error", "Failed to remove ingredient.")

    def prepare_cocktail(self):
        # Here you can implement a more detailed form for entering cocktail details
        cocktail_name = simpledialog.askstring("Input", "Enter cocktail name:")
        ingredients = []

        while True:
            name = simpledialog.askstring("Input", "Enter ingredient name (or leave empty to finish):")
            if not name:
                break
            quantity = simpledialog.askfloat("Input", "Enter ingredient quantity:")
            position = simpledialog.askinteger("Input", "Enter ingredient position:")
            if name and quantity is not None and position is not None:
                ingredients.append({"name": name, "quantity": quantity, "position": position})

        if ingredients:
            cocktail = {"name": cocktail_name, "ingredients": ingredients}
            response = self.bot_tender.prepareCocktail(cocktail)
            if response["status"] == Response.SUCCESS:
                messagebox.showinfo("Success", "Cocktail prepared successfully.")
                self.refresh_status()
            else:
                messagebox.showerror("Error", response["status"])

def run_ui():
    root = tk.Tk()
    app = BotTenderUI(root)
    root.mainloop()
