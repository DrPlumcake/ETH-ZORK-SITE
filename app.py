from flask import Flask, render_template, request, redirect, session, render_template_string, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.utils import secure_filename
import os
import stat
from jinja2 import Template


app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Cambiala in produzione!

# Configurazione database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://zorkadmin:zorkadmin@localhost/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# MODELLO USER
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=True)
    profile_pic = db.Column(db.String(200))

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
                'email': existing_user.email,
                'profile_pic': existing_user.profile_pic
            }
            return redirect('/profile')
        else:
            return "Login fallito"
    return render_template('login.html')


@app.route('/upload-photo', methods=['POST'])
def upload_photo():
    if 'user' not in session:
        return redirect('/login')

    file = request.files.get('profile_pic')
    if not file or file.filename == '':
        return "Nessun file selezionato", 400

    # Sanitize del filename
    filename = secure_filename(file.filename)

    # Crea la cartella se non esiste
    upload_folder = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)

    # Salva il file
    save_path = os.path.join(upload_folder, filename)
    file.save(save_path)
    
    # Assegna permessi di esecuzione (chmod 755, lettura, scrittura ed esecuzione per il proprietario, lettura ed esecuzione per gli altri)
    os.chmod(save_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

    # (Opzionale) Aggiorna il campo profile_pic dell’utente in sessione e DB
    user_session = session['user']
    user = User.query.get(user_session['id'])
    user.profile_pic = f'uploads/{filename}'
    db.session.commit()
    print('DEBUG session updated with:', user.profile_pic)
    print('DEBUG actual file saved at:', save_path)

    # Aggiorna la sessione per mostrare subito la nuova foto
    session['user']['profile_pic'] = user.profile_pic
    
    return redirect('/profile')


@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect('/login')
    user = User.query.get(session['user']['id'])
    rendered_username = render_template_string(user.username)

    return render_template('profile.html', user={
        'id': user.id,
        'username': rendered_username,
        'email': getattr(user, 'email', ''),
        'profile_pic': user.profile_pic
    })


# @app.route('/formUpdateUser', methods=['GET', 'POST'])
# @login_required
# def form_update_user():
#     user = current_user
#
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form.get('email')
#         password = request.form.get('password')  # può essere vuoto
#
#         user.username = username
#         if email:
#             user.email = email
#
#         if password:
#             user.set_password(password)  # usa il metodo corretto
#
#         db.session.commit()
#         flash('Profilo aggiornato con successo.')
#         return redirect(url_for('profile'))
#
#     return render_template('formUpdateUser.html', user=user)


@app.route('/thread-1')
def thread_1():
    return render_template('thread-1.html')

@app.route('/thread-2')
def thread_2():
    return render_template('thread-2.html')

@app.route('/thread-3')
def thread_3():
    return render_template('thread-3.html')

@app.route('/thread-4')
def thread_4():
    return render_template('thread-4.html')

@app.route('/thread-5')
def thread_5():
    return render_template('thread-5.html')




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

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/update-profile', methods=['GET', 'POST'])
def update_profile():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        user = User.query.get(session['user']['id'])
        user.username = request.form['username']
        user.password = request.form['password'] 
        template = Template(user.username)
        rendered = template.render()

        db.session.commit()
        session['user']['username'] = rendered
        return redirect('/profile')
    return render_template('profile.html')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea le tabelle se non esistono
    app.run(host="127.0.0.1", port=5000, debug=True)




