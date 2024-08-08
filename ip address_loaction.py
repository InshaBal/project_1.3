import tkinter as tk
import tkintermapview
import phonenumbers
import sqlite3
from phonenumbers import geocoder
from phonenumbers import carrier
from tkinter import messagebox
from tkinter.ttk import Style, Button, Frame
from opencage.geocoder import OpenCageGeocode

# Assign your actual OpenCage API key
key = 'c43216dbcf764abf9b5f80a47309bd9a'

# Initialize the main window
root = tk.Tk()
root.geometry("500x700")
root.title("Phone Number Tracker")

# Create a SQLite database connection
conn = sqlite3.connect('search_history.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY,
        phone_number TEXT,
        location TEXT,
        service_provider TEXT,
        latitude REAL,
        longitude REAL,
        address TEXT
    )
''')
conn.commit()

# UI Elements
label1 = tk.Label(root, text="Phone Number Tracker", font=('calibri', 20, 'bold'))
label1.pack(pady=10)

number_label = tk.Label(root, text="Enter Phone Number:")
number_label.pack()

number = tk.Text(root, height=1, width=20)
number.pack()

frame = Frame(root)
frame.pack(pady=10)

style = Style()
style.configure("TButton", font=('calibri', 12, 'bold'), borderwidth='4')
style.map('TButton', foreground=[('active', '!disabled', 'green')],
                      background=[('active', 'black')])

def getResult():
    num = number.get("1.0", tk.END).strip()
    try:
        num1 = phonenumbers.parse(num)
        location = geocoder.description_for_number(num1, "en")
        service_provider = carrier.name_for_number(num1, "en")

        ocg = OpenCageGeocode(key)

        query = str(location)
        result = ocg.geocode(query)

        if result and len(result) > 0:
            lat = result[0]['geometry']['lat']
            lng = result[0]['geometry']['lng']
            formatted_address = result[0]['formatted']

            my_label = tk.LabelFrame(root)
            my_label.pack(pady=20)
            map_widget = tkintermapview.TkinterMapView(my_label, width=450, height=450, corner_radius=0)
            map_widget.set_position(lat, lng)
            map_widget.set_marker(lat, lng, text="Phone Location")
            map_widget.set_zoom(10)
            map_widget.pack()

            result_display.delete("1.0", tk.END)
            result_display.insert(tk.END, "The country of this number is: " + location)
            result_display.insert(tk.END, "\nThe sim card of this number is: " + service_provider)
            result_display.insert(tk.END, "\nLatitude is: " + str(lat))
            result_display.insert(tk.END, "\nLongitude is: " + str(lng))
            result_display.insert(tk.END, "\nStreet Address is: " + formatted_address)

            # Save to database
            c.execute('''
                INSERT INTO history (phone_number, location, service_provider, latitude, longitude, address)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (num, location, service_provider, lat, lng, formatted_address))
            conn.commit()
        else:
            messagebox.showerror("Error", "No results found for the location.")

    except phonenumbers.NumberParseException:
        messagebox.showerror("Invalid Number", "The phone number entered is not valid.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def view_history():
    history_window = tk.Toplevel(root)
    history_window.title("Search History")
    history_window.geometry("500x300")

    c.execute('SELECT * FROM history')
    rows = c.fetchall()

    history_text = tk.Text(history_window)
    history_text.pack(fill=tk.BOTH, expand=1)

    for row in rows:
        history_text.insert(tk.END, f"Phone Number: {row[1]}\nLocation: {row[2]}\nService Provider: {row[3]}\nLatitude: {row[4]}\nLongitude: {row[5]}\nAddress: {row[6]}\n\n")

button = Button(frame, text="Search", command=getResult, style="TButton")
button.pack(side=tk.LEFT, padx=10)

history_button = Button(frame, text="View History", command=view_history, style="TButton")
history_button.pack(side=tk.RIGHT, padx=10)

result_display = tk.Text(root, height=7)
result_display.pack(pady=10)

root.mainloop()