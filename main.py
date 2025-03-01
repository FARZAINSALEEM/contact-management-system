from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            name TEXT, 
                            phone TEXT)''')
        conn.commit()

@app.route('/')
def index():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()
    conn.close()
    return render_template('index.html', contacts=contacts)

@app.route('/add', methods=['POST'])
def add_contact():
    name = request.form['name']
    phone = request.form['phone']
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", (name, phone))
    conn.commit()
    conn.close()
    
    return redirect('/')

@app.route('/delete/<int:contact_id>', methods=['POST'])
def delete_contact(contact_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    conn.close()
    
    return redirect('/')

if __name__ == '__main__':
    init_db()  # Initialize database on first run
    app.run(debug=True)
