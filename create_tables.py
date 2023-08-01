from app import app, db

# Create the tables
with app.app_context():
    db.create_all()