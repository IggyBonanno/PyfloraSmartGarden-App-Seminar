import sqlite3
import tkinter as tk
from tkinter import simpledialog
import matplotlib.pyplot as plt
import numpy as np
import requests


class LoginScreen(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="dark green")
        self.master.geometry("385x385")
        self.username_label = tk.Label(self, text="Username")
        self.username_label.pack(pady=10, padx=10)
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()
        self.username_entry.pack()

        self.password_label = tk.Label(self, text="Password")
        self.password_label.pack(pady=10, padx=10)
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="Login", command=self.check_login)
        self.login_button.pack(pady=10)

        self.add_user_button = tk.Button(self, text="Add New User", command=self.add_user_dialog)
        self.add_user_button.pack(pady=10, padx=10)

        self.notification_label = tk.Label(self, text="")
        self.notification_label.pack()

        self.users = {"admin": "admin"}



    def check_login(self):
        if self.username_entry.get() in self.users and self.password_entry.get() == self.users[self.username_entry.get()]:
            self.notification_label.config(text="Login successful", fg="green")
            import sqlite3

            # Create a database connection
            conn = sqlite3.connect('inventory.db')

            # Create a cursor
            c = conn.cursor()

            # Create items table
            c.execute("""CREATE TABLE IF NOT EXISTS items (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        quantity INTEGER NOT NULL
                        )""")
            
            # Create a Tkinter window
            root = tk.Tk()
            root.title("Plant Inventory")
            root.configure(background="green")

            # Create a label for the ID entry field
            id_label = tk.Label(root, text="ID:",  bg="green", fg="white")
            id_label.grid(row=0, column=0)

            # Create an entry field for the ID
            id_entry = tk.Entry(root, width=30)
            id_entry.grid(row=0, column=1)

            # Create a label for the name entry field
            name_label = tk.Label(root, text="Name:", bg="green", fg="white")
            name_label.grid(row=1, column=0)

            # Create an entry field for the name
            name_entry = tk.Entry(root, width=30)
            name_entry.grid(row=1, column=1)

            # Create a label for the name entry field
            name_label = tk.Label(root, text="Name:")
            name_label.grid(row=0, column=0)

            # Create an entry field for the name
            name_entry = tk.Entry(root, width=30)
            name_entry.grid(row=0, column=1)

            # Create a label for the quantity entry field
            quantity_label = tk.Label(root, text="Plant Info:", bg="green", fg="white")
            quantity_label.grid(row=2, column=0)

            # Create an entry field for the quantity
            quantity_entry = tk.Entry(root, width=30)
            quantity_entry.grid(row=2, column=1)

            
            def add():
                name = name_entry.get()
                quantity = (quantity_entry.get())

                c.execute("INSERT INTO items (name, quantity) VALUES (?, ?)", (name, quantity))
                conn.commit()

                

                name_entry.delete(0, tk.END)
                quantity_entry.delete(0, tk.END)

                show_all()

            def show_chart(item_name):
                temperature = np.random.randint(20, 30, size=3)
                rh = np.random.randint(40, 70, size=3)
                light = np.random.randint(100, 500, size=3)

                labels = ["Temperature", "RH", "Light"]
                values = [temperature, rh, light]

                fig, ax = plt.subplots()
                for i in range(len(labels)):
                    ax.bar(labels[i], values[i][0])  # use values[i][0] instead of values[i] to convert the array to a scalar
                ax.set_title(f"Random Plant Info for {item_name}")
                ax.set_xlabel("Category")
                ax.set_ylabel("Value")
                plt.show()

            def get_plant_temperature():
                api_key = "b89161cfb460703f1ced613fa93a7180" # replace with your OpenWeatherMap API key
                city = "Zagreb"
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    temperature = data["main"]["temp"]
                    return f"Plant Environment Temperature: {temperature} °C"
                else:
                    return "Error fetching data"
            
            def show_temperature():
                temperature_label.config(text=get_plant_temperature())

            temperature_button = tk.Button(root, text="Show Plant Temperature", command=show_temperature)
            temperature_button.grid(row=5, column=4)

            temperature_label = tk.Label(root, text="")
            temperature_label.grid(row=4, column=1)

            def update():
                selected_item = listbox.curselection()

                if not selected_item:
                    return

                item_id = int(listbox.get(selected_item).split()[0])
                name = name_entry.get()
                quantity = quantity_entry.get()

                c.execute("UPDATE items SET name=?, quantity=? WHERE id=?", (name, quantity, item_id))

                selected_name = listbox.get(selected_item).split()[1]
                conn.commit()

                name_entry.delete(0, tk.END)
                quantity_entry.delete(0, tk.END)

                show_all()

            # Create a function to delete the selected item from the listbox and the database
            def delete():
                selected_item = listbox.curselection()

                if not selected_item:
                    return

                item_id = int(listbox.get(selected_item).split()[0])

                c.execute("DELETE FROM items WHERE id=?", (item_id,))

                conn.commit()

                show_all()

            # Create a listbox to display the items
            listbox = tk.Listbox(root, height=10, width=50, bg="#ADD8E6", fg="#000000")
            listbox.grid(row=1, column=0, columnspan=4)

            # Create a function to retrieve all items from the database and display them in the listbox
            def show_all():
                listbox.delete(0, tk.END)

                items = c.execute("SELECT * FROM items").fetchall()

                for item in items:
                    listbox.insert(tk.END, f"{item[0]} - {item[1]} ({item[2]})")
            
            
            # Create a button to add an item
            add_button = tk.Button(root, text="Add Plant", command=add)
            add_button.grid(row=0, column=4)

            # Create a button to update an item
            update_button = tk.Button(root, text="Update Plant", command=update)
            update_button.grid(row=1, column=4)

            # Create a button to delete an item
            delete_button = tk.Button(root, text="Delete Plant", command=delete)
            delete_button.grid(row=2, column=4)

            # Create a button to show all items
            show_all_button = tk.Button(root, text="Show All Plants", command=show_all)
            show_all_button.grid(row=3, column=4)
            
            # Create a button to show plant info chart
            show_chart_button = tk.Button(root, text="Show Plant Chart", command=lambda: show_chart(listbox.get(listbox.curselection()).split()[1]))
            show_chart_button.grid(row=4, column=4)

            # Run the Tkinter event loop
            root.mainloop()

        else:
            self.notification_label.config(text="Invalid username or password", fg="red")

    def add_user_dialog(self):
        new_username = simpledialog.askstring("Add New User", "Enter a new username:")
        new_password = simpledialog.askstring("Add New User", "Enter a new password:")
        

        if new_username and new_password:
            if new_username in self.users:
                self.notification_label.config(text="Username already exists", fg="red")
            else:
                self.users[new_username] = new_password
                self.notification_label.config(text="User created successfully", fg="green")
                self.username_entry.delete(0, tk.END)
                self.password_entry.delete(0, tk.END)

                # Clear the login screen to its default state
                self.username_entry.focus_set()

    def clear_screen(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.notification_label.config(text="")
        self.username_entry.focus_set()


root = tk.Tk()
# Create a PhotoImage object from the PNG image file
bg_image = tk.PhotoImage(file=r"C:\Users\iggy\Desktop\plantpics\herbsflora.png")
# Set the background image to the Tkinter window
bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
root.title("PyFlora SmartGarden-Ingo Tolle ©2023")
login_screen = LoginScreen(root)
login_screen.pack()
root.mainloop()

'''GUI aplikacija razvijena korištenjem Tkinter biblioteke u Pythonu. 
Aplikacija je sustav za upravljanje inventarom biljaka koji omogućuje korisnicima prijavu, dodavanje novih stavki u inventar, pregled stavki u inventaru i pregled temperature okoline biljaka.
Aplikacija ima klasu LoginScreen koja stvara prijavni prozor s korisničkim imenom, poljem za lozinku i dvije gumbe, Prijava i Dodaj novog korisnika. 
Korisničko ime i lozinka su unaprijed upisani u kod. Nakon što se korisnik prijavi, aplikacija stvara novi prozor s grafičkim sučeljem za upravljanje inventarom biljaka.
Prozor upravljanja inventarom ima tri polja za unos ID-a, imena i informacija o biljkama. 
Također ima okvir za popis koji prikazuje stavke u inventaru. 
Korisnici mogu dodavati nove stavke u inventar unosom info te imena  klikom na gumb Dodaj. 
Kada se stavka odabere u okviru za popis, dostupan je gumb Prikaži sliku za prikaz slike odabrane stavke.
Aplikacija također ima gumb za prikaz temperature okoline biljaka. 
Dodatno, kada se stavka odabere u okviru za popis, korisnici mogu pregledati slučajne informacije o biljkama za odabranu stavku klikom na gumb Prikaži informacije o biljkama. 
Slučajne informacije o biljkama prikazuju se pomoću grafa s tri kategorije: temperatura, RH i svjetlo.'''