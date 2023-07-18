from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:mysecretpassword@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'

db = SQLAlchemy(app)

# Models

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    role = db.relationship('Role', backref=db.backref('users', lazy='dynamic'))

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128))

# Routes and Views

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role_id = request.form['role_id']
        
        user = User(username=username, email=email, password=password, role_id=role_id)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful. Please log in.')
        return redirect('/login')
    
    roles = Role.query.all()
    return render_template('register.html', roles=roles)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            flash('Login successful.')
            return redirect('/')
        else:
            flash('Invalid username or password.')
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
