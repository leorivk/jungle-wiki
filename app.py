from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/login")
def loginPage():
    return render_template("login.html")


@app.route("/signup")
def signUpPage():
    return render_template("signup.html")

if __name__ == '__main__':
    app.run(debug=True)