from flaskr.main.app import app_test, create_app  # type: ignore

if __name__ == "__main__":
    app = create_app(app_test)
    app.run(port=8080, debug=True)
