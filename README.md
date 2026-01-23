ClearName is a Flask-based web application designed to help users learn the correct pronunciation of names. It features a searchable database of names with phonetic spellings, origins, and audio playback. It supports both automated Text-to-Speech (TTS) and custom user-uploaded audio recordings.

## Features

* **Database Search:** Search a library of names to find phonetic spellings and origins.
* **Audio Playback:**
    * **Auto-TTS:** Uses Google Text-to-Speech (gTTS) for names without custom audio.
    * **Custom Audio:** Users can upload their own recordings, which override the automated voice.
* **Favorites System:** Save frequently used names for quick access.
* **Search History:** Keeps track of recently viewed names.
* **Preference Customization:**
    * **Dark/Light Mode:** Toggle between themes.
    * **Accessibility:** Adjust playback speed (Slow, Normal, Fast) and voice preference (Male/Female).
* **User Contributions:** Add new names, phonetic breakdowns, and custom audio files to the database.

## Technologies Used

* **Backend:** Python, Flask
* **Database:** SQLite3
* **Frontend:** HTML5, CSS3, Bootstrap 5, Jinja2
* **Audio:** gTTS (Google Text-to-Speech)

## Installation & Setup

1.  **Prerequisites:** Ensure you have Python installed.

2.  **Install Dependencies:**
    ```bash
    pip install flask gTTS
    ```

3.  **Initialize the Database:**
    Run the seed script to create the database and populate it with the initial 200+ names.
    ```bash
    python seed.py
    ```

4.  **Run the Application:**
    ```bash
    python app.py
    ```

5.  **Access the App:**
    Open your web browser and navigate to: `http://127.0.0.1:5000/`

## How to Use

1.  **Search:** Enter a name in the search bar (e.g., "Siobhan" or "Nguyen").
2.  **Play Audio:** Click the audio player controls. If a custom recording exists, it plays that; otherwise, it generates the pronunciation.
3.  **Add a Name:** Navigate to "Add Name" to input a new name, origin, phonetic spelling, and upload an MP3/WAV file.
4.  **Preferences:** Click "Preferences" in the menu to change the color theme or audio speed.

## Project Structure

* `app.py`: Main Flask application logic and routes.
* `db.py`: Database connection and initialization logic.
* `seed.py`: Script to populate the database with initial data.
* `templates/`: HTML files for the user interface.
* `static/audio/`: Directory where custom uploaded audio files are stored.
* `instance/`: Directory where the SQLite database (`names.db`) is stored.