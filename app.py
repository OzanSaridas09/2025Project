from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Hello, Flask Web Application!</h1><p>The server is running.</p>"

if __name__ == '__main__':
    app.run(debug=True)