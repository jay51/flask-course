from app import app

DEVELOPMENT_ENV  = True

if __name__ == "__main__":
    app.run("0.0.0.0", 8080, debug=DEVELOPMENT_ENV)
