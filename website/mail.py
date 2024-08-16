from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import json
import os

app = Flask(__name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'priscillaloi2020@gmail.com'  # Your email
app.config['MAIL_PASSWORD'] = 'Pris2020'   # Your email password
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail.com'

mail = Mail(app)

# Load inventory
if os.path.exists('inventory.json'):
    with open('inventory.json', 'r') as f:
        inventory = json.load(f)
else:
    inventory = {
        "Cola": 30,
        "Water": 30,
        "Orange Juice": 30,
        "Energy Drink": 30,
        "Iced Tea": 30,
        "Lemonade": 30
    }

def check_stock():
    low_stock_items = [drink for drink, stock in inventory.items() if stock < 15]
    if low_stock_items:
        drinks_info = ", ".join(low_stock_items)
        send_email(drinks_info)

def send_email(low_stock_items):
    msg = Message('Low Stock Alert',
                  recipients=['priscillaloi2020@gmail.com'])
    msg.body = f"Dear Smart Vending Machine Technician,\n\nThe following drinks are low on stock: {low_stock_items}.\nPlease restock the machine."
    mail.send(msg)

@app.route('/update_stock', methods=['POST'])
def update_stock():
    data = request.json
    for item, change in data.items():
        if item in inventory:
            inventory[item] += change
            # Check stock after update
            check_stock()

    with open('inventory.json', 'w') as f:
        json.dump(inventory, f)

    return jsonify(inventory)

@app.route('/check_stock', methods=['GET'])
def check_inventory():
    return jsonify(inventory)

if __name__ == '__main__':
    app.run(debug=True)

import os
path = os.path.expanduser('~/.yagmail')
if not os.path.isfile(path):
    print("YAGMAIL FILE NOT FOUND!")
    # print(os.path.abspath("/home/pi/.yagmail"))
    open(path, "w").write("")

import yagmail, os

email = os.getenv("MAIL_ADDR")
pw = os.getenv("MAIL_PW")
yag = yagmail.SMTP(email, pw, host="smtppro.zoho.com", port=465)


def send_mail(to: str, subject: str, message_list: list) -> bool:
    mail = yag.send(to=to, subject=subject, contents=message_list)
    return not not mail
