from flask import Flask, session, render_template, request, redirect, url_for, g
import sqlite3, time
from werkzeug.security import generate_password_hash, check_password_hash

# -------------------- Flask App Setup --------------------

app = Flask(__name__)
app.secret_key = 'dev_secret_key_1234567890'  
app.config["TEMPLATES_AUTO_RELOAD"] = True

DATABASE = 'quiz.db'

# -------------------- Database Connection --------------------

def get_db():
    """Connect to SQLite and store it in Flask's `g` for reuse."""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    """Close DB connection after each request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

# -------------------- Routes --------------------

@app.route('/')
def index():
    return render_template('index.html')

# -------------------- Authentication --------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login and verify credentials."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        elif not username or not password:
            return render_template('login.html', error='Username and password are required.')
        elif not user:
            return render_template('login.html', error='Username does not exist.', username=username)
        elif not check_password_hash(user['password'], password):
            return render_template('login.html', error='Incorrect password.', username=username)
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Create a new account with hashed password."""
    if request.method == 'POST':
        fullname = request.form['fullname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        db = get_db()

        if not all([fullname, username, email, password, confirm_password]):
            return render_template('register.html', error='All fields are required.', fullname=fullname, username=username, email=email)
        elif password != confirm_password:
            return render_template('register.html', error='Passwords do not match.', fullname=fullname, username=username, email=email)
        elif len(password) < 6:
            return render_template('register.html', error='Password too short.', fullname=fullname, username=username, email=email)
        elif db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone():
            return render_template('register.html', error='Username already exists.', fullname=fullname, email=email)
        elif db.execute('SELECT * FROM user WHERE email = ?', (email,)).fetchone():
            return render_template('register.html', error='Email already exists.', fullname=fullname, username=username)
        else:
            hashed = generate_password_hash(password, method='pbkdf2:sha256')
            db.execute('INSERT INTO user (fullname, username, email, password) VALUES (?, ?, ?, ?)',
                       (fullname, username, email, hashed))
            db.commit()
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """User dashboard with quiz mode selection."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        mode = request.form.get('mode')
        user_id = session['user_id']
        session.clear()
        session['user_id'] = user_id
        if mode in ['rapid', 'survival', 'standard']:
            return redirect(url_for('quiz', mode=mode))
    return render_template('dashboard.html')

@app.route('/settings')
def settings():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('settings.html')

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = get_db()
    if request.method == 'POST':
        current = request.form.get('current_password')
        new = request.form.get('new_password')
        confirm = request.form.get('confirm_password')
        user = db.execute('SELECT * FROM user WHERE id = ?', (session['user_id'],)).fetchone()

        if not check_password_hash(user['password'], current):
            return render_template('change_password.html', error='Incorrect current password.')
        if new != confirm:
            return render_template('change_password.html', error='Passwords do not match.')
        if len(new) < 6:
            return render_template('change_password.html', error='Password too short.')
        if new == current:
            return render_template('change_password.html', error='New password cannot be the same as current password.')
        if not new or not confirm:
            return render_template('change_password.html', error='All fields are required.')

        hashed = generate_password_hash(new, method='pbkdf2:sha256')
        db.execute('UPDATE user SET password = ? WHERE id = ?', (hashed, session['user_id']))
        db.commit()
        return redirect(url_for('settings'))
    return render_template('change_password.html')

@app.route('/delete_account')
def delete_account():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = get_db()
    db.execute('DELETE FROM user WHERE id = ?', (session['user_id'],))
    db.commit()
    session.clear()
    return redirect(url_for('register'))

# -------------------- Quiz Route --------------------

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    mode = request.form.get('mode') if request.method == 'POST' else request.args.get('mode', 'standard')
    feedback = ''
    selected = None

    # Initialize quiz state
    if 'started' not in session:
        session['started'] = True
        session['asked_ids'] = []
        session['score'] = 0
        if mode == 'rapid':
            session['start_time'] = time.time()

    # Adjust time based on hidden input from frontend
    if mode == 'rapid':
        if request.method == 'POST':
            try:
                remaining = int(request.form.get('remaining', '300'))
            except ValueError:
                remaining = 0
            session['start_time'] = time.time() - (300 - remaining)
        elapsed = int(time.time() - session.get('start_time', time.time()))
        remaining = max(0, 300 - elapsed)

        if remaining <= 0:
            score = session['score']
            for key in ['started', 'asked_ids', 'score', 'start_time', 'correct_option', 'current_question', 'submitted']:
                session.pop(key, None)
            return render_template('quiz.html', mode=mode, question=None, feedback=f"Time's up! Score: {score}")
    else:
        remaining = None

    # Process form submission
    if request.method == 'POST':
        action = request.form.get('action')
        selected = request.form.get('answer')
        correct = session.get('correct_option')
        q_data = session.get('current_question')

        if not q_data:
            return redirect(url_for('quiz', mode=mode))

        option_map = {
            'A': q_data['option_a'],
            'B': q_data['option_b'],
            'C': q_data['option_c'],
            'D': q_data['option_d'],
        }

        if action == 'submit':
            if selected:
                session['submitted'] = True
                if selected == correct:
                    session['score'] += 1
                    feedback = "Correct!"
                else:
                    feedback = f"Incorrect! Correct option was {correct}) {option_map.get(correct)}"
                    if mode == 'survival':
                        score = session['score']
                        for key in ['started', 'asked_ids', 'score', 'start_time', 'correct_option', 'current_question', 'submitted']:
                            session.pop(key, None)
                        return render_template('quiz.html', mode=mode, question=None, feedback=f"Game over! Score: {score}")
            else:
                feedback = "Please select an answer."

            options = [
                {'id': 'A', 'text': q_data['option_a']},
                {'id': 'B', 'text': q_data['option_b']},
                {'id': 'C', 'text': q_data['option_c']},
                {'id': 'D', 'text': q_data['option_d']},
            ]
            question = {'text': q_data['question_text'], 'options': options}
            return render_template('quiz.html', mode=mode, question=question, feedback=feedback, selected=selected, remaining=remaining)

        elif action == 'next':
            if not session.get('submitted'):
                feedback = "Please submit your answer before going to the next question."
                options = [
                    {'id': 'A', 'text': q_data['option_a']},
                    {'id': 'B', 'text': q_data['option_b']},
                    {'id': 'C', 'text': q_data['option_c']},
                    {'id': 'D', 'text': q_data['option_d']},
                ]
                question = {'text': q_data['question_text'], 'options': options}
                return render_template('quiz.html', mode=mode, question=question, feedback=feedback, selected=selected, remaining=remaining)

            session['asked_ids'].append(q_data['id'])
            session.pop('submitted', None)

    # Load new question
    q = db.execute(
        'SELECT * FROM question WHERE id NOT IN ({seq}) ORDER BY RANDOM() LIMIT 1'.format(
            seq=','.join(['?'] * len(session['asked_ids'])) if session['asked_ids'] else '0'),
        session['asked_ids'] if session['asked_ids'] else []
    ).fetchone()

    if not q:
        score = session['score']
        for key in ['started', 'asked_ids', 'score', 'start_time', 'correct_option', 'current_question', 'submitted']:
            session.pop(key, None)
        return render_template('quiz.html', mode=mode, question=None, feedback=f"You've finished all questions! Score: {score}")

    session['correct_option'] = q['correct_option']
    session['current_question'] = dict(q)

    options = [
        {'id': 'A', 'text': q['option_a']},
        {'id': 'B', 'text': q['option_b']},
        {'id': 'C', 'text': q['option_c']},
        {'id': 'D', 'text': q['option_d']},
    ]
    question = {'text': q['question_text'], 'options': options}

    return render_template(
        'quiz.html',
        mode=mode,
        question=question,
        feedback=feedback,
        selected=selected,
        remaining=remaining
    )

# -------------------- User Profile --------------------

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = get_db()
    user = db.execute('SELECT * FROM user WHERE id = ?', (session['user_id'],)).fetchone()
    if not user:
        return redirect(url_for('login'))
    return render_template('profile.html', user=user, fullname=user['fullname'], email=user['email'])

@app.route('/questions')
def questions():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = get_db()
    questions = db.execute('SELECT * FROM question').fetchall()
    return render_template('questions.html', questions=questions)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# -------------------- Start Server --------------------

if __name__ == '__main__':
    app.run(debug=True)
