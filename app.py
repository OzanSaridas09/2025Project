import os
import sqlite3  
from flask import Flask, render_template, request, redirect, url_for
from db import db_session

app = Flask(__name__)

UPLOAD_FOLDER = 'static/audio'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def index():
    query = request.args.get('search')
    
    # 1. Open the DB Connection
    with db_session('instance/names.db') as conn:
        # 2. Convert rows to dictionaries so we can use name.name instead of name[1]
        conn.row_factory = sqlite3.Row 
        
        if query:
            # Search Logic
            results = conn.execute(
                "SELECT * FROM names WHERE name LIKE ? ORDER BY created_at DESC", 
                ('%' + query + '%',)
            ).fetchall()
        else:
            # Default: Show recent 12 names
            results = conn.execute("SELECT * FROM names ORDER BY created_at DESC LIMIT 12").fetchall()
            
    # 3. Send the 'results' list to the HTML template
    return render_template('index.html', names=results, query=query)

@app.route('/addname', methods=['GET', 'POST'])
def addname():
    if request.method == 'POST':
        # 1. Grab the text data from the HTML form names
        name = request.form.get('name')
        phonetic = request.form.get('phonetic')
        origin = request.form.get('origin')
        comments = request.form.get('comments')
        
        # 2. Handle the Audio File Upload
        audio_file = request.files.get('audio_file')
        filename = None
        
        if audio_file and audio_file.filename != '':
            # Clean the filename: 'Siobhan_recording.mp3'
            filename = f"{name}_{audio_file.filename}"
            # Save it to static/audio/
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            audio_file.save(filepath)

        # 3. Insert into Database
        with db_session('instance/names.db') as conn:
            conn.execute('''
                INSERT INTO names (name, phonetic, origin, comments, audio_path)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, phonetic, origin, comments, filename))
            
        # 4. Redirect to the home page after success
        return redirect(url_for('index'))
    
    # If it's a GET request, just show the form page
    return render_template('addname.html')

@app.route('/favorites')
def favorites():
    return render_template("favorites.html")

@app.route('/history')
def history():
    return render_template("history.html")

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/delete/<int:id>')
def delete_name(id):
    with db_session('instance/names.db') as conn:
        # Use sqlite3.Row to access columns by name
        conn.row_factory = sqlite3.Row
        
        # 1. Get the filename so we can delete the actual audio file
        row = conn.execute("SELECT audio_path FROM names WHERE id = ?", (id,)).fetchone()
        
        if row and row['audio_path']:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], row['audio_path'])
            if os.path.exists(file_path):
                os.remove(file_path) # Deletes the physical .mp3 file
        
        # 2. Delete the record from the database
        conn.execute("DELETE FROM names WHERE id = ?", (id,))
        
    return redirect(url_for('index'))
