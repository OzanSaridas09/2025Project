import os
import sqlite3 
import io 
from gtts import gTTS
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from db import db_session, init_db, get_db_connection

app = Flask(__name__)

app.secret_key = 'Come-Blood-Detail-Pine-Nation4-Since'

UPLOAD_FOLDER = 'static/audio'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    # 1. Grab the search term from the URL
    search_query = request.args.get('search', '')

    # 2. Decide what to show
    if search_query:
        with db_session('instance/names.db') as conn:
            # Look for names that match
            conn.execute("UPDATE names SET last_viewed = CURRENT_TIMESTAMP WHERE name LIKE ?",('%' + search_query + '%',))
            results = conn.execute("SELECT * FROM names WHERE name LIKE ?", ('%' + search_query + '%',)).fetchall()
    else:
        # Show nothing on the home page by default
        results = []

    # 3. Send the results to the HTML
    return render_template('index.html', names=results, search_query=search_query)

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
        flash(f"Successfully added {name}!", "success")
        return redirect(url_for('index'))
    
    # If it's a GET request, just show the form page
    return render_template('addname.html')

@app.route('/favorites')
def favorites():
    with db_session('instance/names.db') as conn:
        fav_names = conn.execute('SELECT * FROM names WHERE is_favorite = 1').fetchall()
        return render_template("index.html", names=fav_names, title='Favorited Names', page_type='favorites')

@app.route('/history')
def history():
    search_query = request.args.get('search', '')
    with db_session('instance/names.db') as conn:
        if search_query:
            history_results = conn.execute(
                "SELECT * FROM names WHERE last_viewed IS NOT NULL AND name LIKE ? ORDER BY last_viewed DESC", 
                ('%' + search_query + '%',)
            ).fetchall()
        else:
            history_results = conn.execute(
                "SELECT * FROM names WHERE last_viewed IS NOT NULL ORDER BY last_viewed DESC"
            ).fetchall()
            
    return render_template('history.html', history=history_results, search_query=search_query)

@app.route('/clear_history')
def clear_history():
    with db_session('instance/names.db') as conn:
        conn.execute("UPDATE names SET last_viewed = NULL")
    return redirect(url_for('history'))

@app.route('/delete_history/<int:id>')
def delete_history(id):
    with db_session('instance/names.db') as conn:
        conn.execute("UPDATE names SET last_viewed = NULL WHERE id = ?", (id,))
    return redirect(url_for('history'))

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

@app.route('/toggle_favorite/<int:id>')
def toggle_favorite(id):
    with db_session('instance/names.db') as conn:
        conn.execute("UPDATE names SET is_favorite = 1-is_favorite WHERE id = ?", (id,))
    return redirect(request.referrer or url_for('index'))

@app.route('/pronounce/<name>')
def pronounce(name):
    # Get the voice from session, default to 'us' (Female)
    # 'com.au' acts as the Male voice in gTTS
    voice_tld = session.get('tts_voice', 'us')
    
    tts = gTTS(text=name, lang='en', tld=voice_tld)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return send_file(fp, mimetype='audio/mpeg')

@app.route('/preferences', methods=['POST'])
def preferences():
    session['theme'] = request.form.get('theme', 'light')
    session['tts_speed'] = float(request.form.get('speed', 1.0))
    session['tts_voice'] = request.form.get('voice', 'us')
    return redirect(request.referrer or url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)