from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)
CONTACTS_FILE = "contacts.json"

# Load contacts from JSON file
def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as file:
            return json.load(file)
    return {}

# Save contacts to JSON file
def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as file:
        json.dump(contacts, file, indent=4)

@app.route('/')
def index():
    contacts = load_contacts()
    return render_template("index.html", contacts=contacts)

@app.route('/add', methods=['POST'])
def add_contact():
    name = request.form.get("name").strip()
    phone = request.form.get("phone").strip()
    
    if not name or not phone:
        return jsonify({"error": "Name and phone number cannot be empty!"}), 400
    
    contacts = load_contacts()
    if name in contacts:
        return jsonify({"error": "Contact already exists!"}), 400
    
    contacts[name] = phone
    save_contacts(contacts)
    return redirect(url_for('index'))

@app.route('/delete/<name>', methods=['POST'])
def delete_contact(name):
    contacts = load_contacts()
    if name in contacts:
        del contacts[name]
        save_contacts(contacts)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
