from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    session,
    jsonify,
    json,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:mysecretpassword@20.0.161.2:5432/postgres"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "mykey"

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'mailhog'
app.config['MAIL_PORT'] = 1025  # MailHog SMTP port
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEBUG'] = True

mail = Mail(app)

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
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    role = db.relationship("Role", backref=db.backref("users", lazy="dynamic"))

    def __init__(self, username, email, password, role_id):
        self.username = username
        self.email = email
        self.password = password
        self.role_id = role_id


class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    issue_description = db.Column(db.String(50))
    status = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('issues', lazy='dynamic'))
    

    def __init__(self, name, phone, issue_description, status,user_id):
        self.name = name
        self.phone = phone
        self.issue_description = issue_description
        self.status = status
        self.user_id = user_id


def check_role(user, role_name):
    return user.role.name == role_name


# Routes and Views


@app.route("/")
def index():
    user_id = session.get("user_id")

    if user_id:
        user = db.session.get(User, user_id)
        issues = get_issues()
        if user and check_role(user, "Supporter"):
            return render_template("supporter.html", username=user.username, issues=issues)
        elif user and check_role(user, "User"):
            return render_template("user.html", username=user.username,issues=issues)
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        role_id = request.form["role_id"]

        user = User(username=username, email=email, password=password, role_id=role_id)
        db.session.add(user)
        db.session.commit()

        msg = Message('Issue Tracker', sender='flask_mailhog@gmail.com', recipients=[email])
        msg.body = 'Hello, thanks for signing up!'
        mail.send(msg)

        flash("Registration successful. Please log in.")
        return redirect("/login")

    
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session["user_id"] = user.id
            flash("Login successful.")
            return redirect("/")
        else:
            error_message = "Invalid username or password."
            return render_template("login.html", error_message=error_message)

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/")
    

@app.route("/add_issue", methods=["POST", "GET"])
def add_issue():
    user_id = session.get("user_id")

    if user_id:
        user = db.session.get(User, user_id)

        if user and check_role(user, "User"):
            if request.method == "POST":
                name = request.form["name"]
                phone = request.form["phone"]
                issue_description = request.form["issue_description"]
                status = request.form["status"]

                issue = Issue(
                    name=name,
                    phone=phone,
                    issue_description=issue_description,
                    status=status,
                    user_id = int(user_id)
                )

                try:
                    db.session.add(issue)
                    db.session.commit()
                    return redirect("/")  # Redirect to the same page after adding
                except Exception as e:
                    db.session.rollback()
                    return jsonify({"error": str(e)})

            return render_template("add_issue.html")
        return "only users can add issues"
    return render_template("login.html")


@app.route("/get_issues", methods=["GET"])
def get_issues():
    user_id = session.get("user_id")

    if user_id:
        user = db.session.get(User, user_id)
        
        if user and (check_role(user, "User") or check_role(user, "Supporter")):
            issues = db.session.query(Issue).all()
            serialized_issues = []
            for issue in issues:
                user = db.session.query(User).filter_by(id=issue.user_id).first()
                serialized_issue = {
                    "id": issue.id,
                    "name": issue.name,
                    "phone": issue.phone,
                    "issue_description": issue.issue_description,
                    "user" : user.username,
                    "status": issue.status
                }
                serialized_issues.append(serialized_issue)

            return (serialized_issues)
        return("you dont have permission to see issues")
    return render_template("login.html")



@app.route("/update_issue/<int:issue_id>", methods=["POST", "GET"])
def update_issue(issue_id):
    user_id = session.get("user_id")

    if user_id:
        user = db.session.get(User, user_id)
        
        if user and check_role(user, "Supporter"):
           if request.method == 'GET':
            try:
                issue = db.session.query(Issue).get(issue_id)
                if issue is None:
                    return jsonify({"error": "Issue not found"}), 404
            
            except Exception as e:
             db.session.rollback()
             return jsonify({"error": str(e)}), 500    
            return render_template("change_status.html",issue=issue)
           elif request.method == 'POST':
            data = request.json
       
            new_status = data["status"]

            if new_status is None:
                return jsonify({"error": "New status not provided"}), 400

            try:
                issue = db.session.query(Issue).get(issue_id)
                if issue is None:
                    return jsonify({"error": "Issue not found"}), 404

                issue.status = new_status
                db.session.commit()

                return jsonify({"message": "Issue status updated successfully"})

            except Exception as e:
             db.session.rollback()
             return jsonify({"error": str(e)}), 500
        return("you dont have permission to change status")  
    return render_template("login.html")  


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
