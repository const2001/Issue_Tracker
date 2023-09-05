# Issue_Tracker
## Clone and run project
```bash
git clone https://github.com/const2001/Issue_Tracker
python -m venv myvenv
source myvenv/bin/activate
pip install -r requirements.txt
```
## Modify the database url to your settings 
```vim
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:mysecretpassword@localhost:5432/postgres"
```
## Configure the mail server
```vim
app.config['MAIL_SERVER'] = 'mailhog-container'
app.config['MAIL_PORT'] = 1025  # MailHog SMTP port
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEBUG'] = True
```
# run flask server
```bash
python app.py
```
