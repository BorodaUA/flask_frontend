from flask_frontend import create_app

# app = create_app("development")
app = create_app("testing")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5600,
        debug=True,
        use_debugger=False,
        use_reloader=False,
        passthrough_errors=True,
    )
