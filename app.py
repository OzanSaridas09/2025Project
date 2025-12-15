from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Hello, Flask Web Application!</h1><p>The server is running.</p>"

@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(debug=True)

