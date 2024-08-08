import tkinter as tk
import tkintermapview
import phonenumbers

from phonenumbers import geocoder
from phonenumbers import carrier
from tkinter import messagebox
from opencage.geocoder import OpenCageGeocode

# Assign your actual OpenCage API key
key = 'c43216dbcf764abf9b5f80a47309bd9a'

root = tk.Tk()
root.geometry("500x700")

label1 = tk.Label(root, text="Phone Number Tracker")
label1.pack()

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
        else:
            messagebox.showerror("Error", "No results found for the location.")

    except phonenumbers.NumberParseException:
        messagebox.showerror("Invalid Number", "The phone number entered is not valid.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

number = tk.Text(root, height=1)
number.pack()

button = tk.Button(root, text="Search", command=getResult)
button.pack(pady=10, padx=100)

result_display = tk.Text(root, height=7)
result_display.pack()

root.mainloop()