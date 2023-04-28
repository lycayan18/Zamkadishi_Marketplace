from flask import Flask
from keys.config import load_config

from pkg import blueprint_login, blueprint_ipp, blueprint_user, login_manager


def main():
    app = Flask(__name__)
    config = load_config()
    app.config["SECRET_KEY"] = config.flask.secret_key

    login_manager.init_app(app)

    app.register_blueprint(blueprint_login)
    app.register_blueprint(blueprint_user)
    app.register_blueprint(blueprint_ipp)

    app.run(host="127.0.0.1", port=8080)


if __name__ == '__main__':
    main()
