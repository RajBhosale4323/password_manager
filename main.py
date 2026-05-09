from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
starting_username = "starting mail/username"
path = "C:\Projects\pass_manager\logo.png"
file_path = "C:\Projects\pass_manager\data.json"
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def gen_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []
    pass_letters = [random.choice(letters) for char in range(random.randint(8, 10))]
    pass_symbols = [random.choice(symbols) for char in range(random.randint(2, 4))]
    pass_numbers = [random.choice(numbers) for char in range(random.randint(2, 4))]
    password_list = pass_letters + pass_symbols + pass_numbers

    random.shuffle(password_list)

    password = "".join(password_list)
    pyperclip.copy(password)

    return password_enter.insert(0, password)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def add():
    website = website_enter.get()
    username = username_enter.get()
    password = password_enter.get()
    new_data = {
        website : {
            "email" : username,
            "password" : password
        }
    }
    if len(website) > 0 and len(password) > 0 and len(username) > 0:
        ok = messagebox.askokcancel(title=website, message=f"Here are the details: \nEmail: {username} \npassword: {password}")
        if ok:
            try:
                with open(file_path, "r") as file:
                    data = json.load(file)
            except FileNotFoundError:
                with open(file_path, "w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                data.update(new_data)
                with open(file_path, "w") as file:
                    json.dump(data, file, indent=4)   
            finally:
                website_enter.delete(0, END)
                password_enter.delete(0, END)
        else:
            messagebox.showerror(title="Error", message="Please enter again")
    else:
        messagebox.showerror(title="Error", message="please enter details")

def search():
    website = website_enter.get()
    if website == 0:
        return messagebox.showerror(title="Error", message="please enter details")
    else:
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
            messagebox.showinfo(title=website, message=f"Email: {data[website]["email"]} \nPassword: {data[website]["password"]}")
            pyperclip.copy(f"{data[website]["email"]}:{data[website]["password"]}")
        except KeyError:
            messagebox.showerror(title="Error", message=f"No data found from {website}")
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(window, width=200, height=200)
img = PhotoImage(file=path)
canvas.create_image(100, 100, image=img)
canvas.grid(row=0, column=1)

#LB:
lb1 = Label(text= "Website:")
lb2 = Label(text= "Email/Username:")
lb3 = Label(text= "Password:")

lb1.grid(row=1, column=0)
lb2.grid(row=2, column=0)
lb3.grid(row=3, column=0)

#txt box:
website_enter = Entry(width=36)
website_enter.focus_set()
username_enter = Entry(width=55)
username_enter.insert(0, starting_username)
password_enter = Entry(width=36)

website_enter.grid(row=1, column=1)
username_enter.grid(row=2, column=1, columnspan=2)
password_enter.grid(row=3, column=1)

#buttons:
gen_pass_button = Button(text="Generate Password", command=gen_pass)
add_button = Button(text="Add", width=47, command=add)
search_button = Button(text="Search", command=search,  width=15)

gen_pass_button.grid(row=3, column=2)
add_button.grid(row=4, column=1, columnspan=2)
search_button.grid(row=1, column=2)


window.mainloop()