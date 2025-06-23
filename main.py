from app import app
from VzrdClothing import models_db

with app.app_context():
    models_db.db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
