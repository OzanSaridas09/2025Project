from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/addname')
def addname():
    return render_template("addname.html")

@app.route('/favorites')
def favorites():
    return render_template("favorites.html")

@app.route('/history')
def history():
    return render_template("history.html")

if __name__ == '__main__':
    app.run(debug=True)

