from flask_front_1 import create_app
from flask_jwt_extended import JWTManager

app = create_app("development")


if __name__ == "__main__":
    app.run(
        port=5000,
        debug=True,
        use_debugger=False,
        use_reloader=False,
        passthrough_errors=True,
    )
