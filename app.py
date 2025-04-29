from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Cambiala in produzione!

# Configurazione database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dr_plumcake:drplumcake@localhost/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# MODELLO USER
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)  # Idealmente hashata

@app.route('/')
def index():
    return render_template('forums.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        # Query vulnerabile a SQL Injection
        query = text(f"SELECT * FROM users WHERE username = '{user}' AND password = '{pwd}'")
        existing_user = db.session.execute(query).fetchone()

        #existing_user = User.query.filter_by(username=user, password=pwd).first()
        if existing_user:
            session['user'] = {
                'id': existing_user.id,
                'username': existing_user.username,
                'email': existing_user.email  # Assumendo che ci sia un campo email
            }
            return redirect('/profile')
        else:
            return "Login fallito"
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect('/login')
    user_data = session['user']
    return render_template('profile.html', user=user_data)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        path = os.path.join("static/uploads", file.filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        file.save(path)
        return "Upload riuscito!"
    return "Nessun file caricato"

@app.route('/detail')
def detail():
    return render_template('detail.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea le tabelle se non esistono
    app.run(host="192.168.56.100", debug=True)
