from flask import Flask
from secret.key import SECRET_KEY
from api.user import user_blueprint

app = Flask(__name__)

app.register_blueprint(user_blueprint)

app.config["SECRET_KEY"] = SECRET_KEY

if __name__ == '__main__':
    app.run(debug=True)