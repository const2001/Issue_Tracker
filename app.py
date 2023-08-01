from flask import Flask, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mysecretpassword@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "mykey"

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

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(50))
    status = db.Column(db.String(50))

def check_role(user, role_name):
    return user.role.name == role_name

      

# Routes and Views

@app.route('/')
def index():
    user_id = session.get('user_id')
    print(user_id)
    if user_id:
        user = User.query.get(user_id)
        if check_role(user, 'admin'):
            print("admin")
            return render_template('admin.html', username=user.username)
        elif check_role(user, 'user'):
            return render_template('user.html', username=user.username)
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        user = User(username=username, email=email, password=password, role_id=1)
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
            session['user_id'] = user.id  # Store the user's ID in the session
            flash('Login successful.')
            return redirect('/')
        else:
            flash('Invalid username or password.')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
