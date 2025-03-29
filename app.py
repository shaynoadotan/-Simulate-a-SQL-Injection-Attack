from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# טבלת משתמשים
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

# יצירת מסד הנתונים
with app.app_context():
    db.create_all()

# 🔹 מסך התחברות עם חולשת SQL Injection
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 🔴 קוד פגיע ל-SQL Injection
        query = f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'"
        result = db.session.execute(query).fetchone()

        if result:
            return render_template('dashboard.html', username=username)
        else:
            return "Login Failed"

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
