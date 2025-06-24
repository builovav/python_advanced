from app import app_prod, create_app  # type: ignore

if __name__ == "__main__":
    app = create_app(app_prod)
    app.run(port=8080, debug=True)
