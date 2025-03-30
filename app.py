from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# מודל משתמשים
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

# יצירת טבלת המשתמשים והוספת משתמש admin אם לא קיים
with app.app_context():
    db.create_all()
    
    existing_user = User.query.filter_by(username="admin").first()
    if not existing_user:
        new_user = User(username="admin", password="password123")
        db.session.add(new_user)
        db.session.commit()
        print("User added successfully!")
    else:
        print("User already exists!")

# עמוד הבית – מפנה לדף ההתחברות
@app.route('/')
def home():
    return render_template('login.html')

# מסך התחברות – כולל קוד פגיע ל-SQL Injection
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 🔴 קוד פגיע ל-SQL Injection (התקפה עם: ' OR '1'='1)
        query = text(f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'")
        result = db.session.execute(query).fetchone()

        if result:
            return render_template('dashboard.html', username=username)
        else:
            return "Login Failed"

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
