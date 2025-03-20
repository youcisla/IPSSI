import os
from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_bcrypt import Bcrypt
from functools import wraps
from datetime import datetime, timedelta
from sqlalchemy import text
from random import choice

app = Flask(__name__, instance_relative_config=True)
# Ensure instance folder exists.
try:
    os.makedirs(app.instance_path)
except OSError:
    pass
# Using a local SQLite database located in the instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'admin'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Define models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  # new field
    password = db.Column(db.String(128), nullable=False)
    reward_points = db.Column(db.Integer, default=0)  # added for admin-updated rewards
    isAdmin = db.Column(db.Boolean, default=False)  # new field
    tasks = db.relationship('Task', backref='user', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.String(256), nullable=False)
    done = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(10), default='Normal')
    created_time = db.Column(db.DateTime, default=datetime.now)
    last_updated = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    due_time = db.Column(db.DateTime, nullable=False)
    reward_given = db.Column(db.Boolean, default=False)  # new field added

# Add new model for reset phrases (seeded if table empty)
class Phrase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(256), nullable=False)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Add admin_required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = User.query.filter_by(id=session['user_id']).first()
        if not user or not user.isAdmin:
            flash("Admin access required.")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Update login to use db query
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['isAdmin'] = user.isAdmin
            return redirect(url_for('index'))
        flash("Invalid username or password", "danger")
    return render_template('auth/login.html')

# New registration route using db
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        is_admin = True if request.form.get('isAdmin')=='on' else False
        if User.query.filter_by(username=username).first():
            flash("Username already taken", "danger")
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash("Email already used", "danger")
            return redirect(url_for('register'))
        if password != confirm:
            flash("Passwords do not match", "danger")
            return redirect(url_for('register'))
        new_user = User(username=username,
                        email=email,
                        password=bcrypt.generate_password_hash(password).decode('utf-8'),
                        isAdmin=is_admin)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for('login'))
    return render_template('auth/register.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('user_id')
    session.pop('username')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    user_id = session['user_id']
    tasks = Task.query.filter_by(user_id=user_id).all()
    priority_order = {"High": 3, "Normal": 2, "Low": 1}
    priority_filter = request.args.get('priority')
    status_filter = request.args.get('status')
    updated_after = request.args.get('updated_after')
    updated_before = request.args.get('updated_before')
    if priority_filter:
        tasks = [t for t in tasks if t.priority == priority_filter]
    if status_filter:
        if status_filter == 'done':
            tasks = [t for t in tasks if t.done]
        elif status_filter == 'pending':
            tasks = [t for t in tasks if not t.done]
    if updated_after:
        try:
            after_dt = datetime.fromisoformat(updated_after)
            tasks = [t for t in tasks if t.last_updated >= after_dt]
        except:
            pass
    if updated_before:
        try:
            before_dt = datetime.fromisoformat(updated_before)
            tasks = [t for t in tasks if t.last_updated <= before_dt]
        except:
            pass
    tasks.sort(key=lambda t: (priority_order.get(t.priority, 0), t.created_time), reverse=True)
    return render_template('tasks/index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
@login_required
def add_task():
    user_id = session['user_id']
    task_text = request.form.get('task')
    priority = request.form.get('priority', 'Normal')
    if task_text:
        now = datetime.now()
        # Enforce daily creation limits per priority
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        count = Task.query.filter(Task.user_id==user_id,
                                  Task.priority==priority,
                                  Task.created_time >= today_start,
                                  Task.created_time < today_end).count()
        limits = {"Low":20, "Normal":10, "High":5}
        if count >= limits.get(priority, 10):
            flash(f"Daily limit reached for {priority} priority tasks.", "danger")
            return redirect(url_for('index'))
        new_task = Task(user_id=user_id,
                        text=task_text,
                        done=False,
                        priority=priority,
                        created_time=now,
                        last_updated=now,
                        due_time=now + timedelta(hours=24))
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/toggle_task/<int:task_id>', methods=['POST'])
@login_required
def toggle_task(task_id):
    user_id = session['user_id']
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if task:
        original_status = task.done
        task.done = not task.done
        # If now finished and not already rewarded, add reward points based on priority.
        if not original_status and task.done and not task.reward_given:
            points_mapping = {"Low": 1, "Normal": 5, "High": 10}
            reward = points_mapping.get(task.priority, 5)
            user = User.query.filter_by(id=user_id).first()
            user.reward_points += reward
            task.reward_given = True
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/update_task', methods=['POST'])
@login_required
def update_task():
    user_id = session['user_id']
    task_id = int(request.form.get('id'))
    new_text = request.form.get('text')
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if task:
        task.text = new_text
        task.last_updated = datetime.now()
        db.session.commit()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(success=True, text=new_text)
    return redirect(url_for('index'))

# New route to update task priority
@app.route('/update_priority', methods=['POST'])
@login_required
def update_priority():
    user_id = session['user_id']
    task_id = int(request.form.get('id'))
    new_priority = request.form.get('priority')
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if task:
        task.priority = new_priority
        task.last_updated = datetime.now()
        db.session.commit()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(success=True, priority=new_priority)
    return redirect(url_for('index'))

@app.route('/finished_tasks')
@login_required
def finished_tasks():
    user_id = session['user_id']
    finished = Task.query.filter_by(user_id=user_id, done=True).all()
    return render_template('tasks/finished_tasks.html', tasks=finished)

@app.route('/delayed_tasks')
@login_required
def delayed_tasks():
    user_id = session['user_id']
    now = datetime.now()
    delayed = Task.query.filter(Task.user_id==user_id, Task.done==False, Task.due_time < now).all()
    return render_template('tasks/delayed_tasks.html', tasks=delayed)

@app.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    user_id = session['user_id']
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))

# Modify inject_user_rewards to use manual reward_points from User model
@app.context_processor
def inject_user_rewards():
    user_id = session.get('user_id')
    reward_points = 0
    is_admin = False
    if user_id:
        user = User.query.filter_by(id=user_id).first()
        if user:
            reward_points = user.reward_points
            is_admin = user.isAdmin
    return dict(current_user=session.get('username'), reward_points=reward_points, is_admin=is_admin)

# New admin panel routes

@app.route('/admin')
@admin_required
def admin_panel():
    # Render admin panel with links to other admin functions
    return render_template('admin/admin_panel.html')

@app.route('/admin/tasks')
@admin_required
def admin_tasks():
    tasks = Task.query.all()
    return render_template('admin/admin_tasks.html', tasks=tasks)

@app.route('/admin/export_tasks')
@admin_required
def export_tasks():
    import csv
    from io import StringIO
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['Task ID', 'Username', 'Text', 'Done', 'Priority', 'Created_time', 'Last_updated', 'Due_time'])
    tasks = Task.query.all()
    for t in tasks:
        writer.writerow([t.id, t.user.username, t.text, t.done, t.priority, t.created_time, t.last_updated, t.due_time])
    output = si.getvalue()
    from flask import Response
    return Response(output, mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=tasks.csv"})

@app.route('/admin/import_tasks', methods=['GET', 'POST'])
@admin_required
def import_tasks():
    if request.method == 'POST' and 'file' in request.files:
        file = request.files['file']
        import csv
        from io import StringIO
        stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        next(csv_input)  # skip header
        for row in csv_input:
            # Expected CSV: Task ID, Username, Text, Done, Priority, Created_time, Last_updated, Due_time
            username = row[1]
            user = User.query.filter_by(username=username).first()
            if user:
                new_task = Task(
                    user_id=user.id,
                    text=row[2],
                    done=(row[3].strip().lower()=='true'),
                    priority=row[4],
                    created_time=datetime.fromisoformat(row[5]),
                    last_updated=datetime.fromisoformat(row[6]),
                    due_time=datetime.fromisoformat(row[7])
                )
                db.session.add(new_task)
        db.session.commit()
        flash("Tasks imported successfully.")
        return redirect(url_for('admin_panel'))
    return render_template('admin/import_tasks.html')

@app.route('/ranking')
def ranking():
    users = User.query.order_by(User.reward_points.desc()).all()
    return render_template('admin/ranking.html', users=users)

@app.route('/admin/update_rewards', methods=['GET', 'POST'])
@admin_required
def update_rewards():
    if request.method == 'POST':
        # Expect form fields named "user_<user_id>" for reward update
        for user in User.query.all():
            new_reward = request.form.get(f'user_{user.id}')
            if new_reward is not None:
                try:
                    user.reward_points = int(new_reward)
                except ValueError:
                    pass
        db.session.commit()
        flash("Rewards updated.", "success")
        return redirect(url_for('admin_panel'))
    users = User.query.all()
    return render_template('admin/update_rewards.html', users=users)

# New route for mot de passe oublié
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form.get('username')
        phrase_input = request.form.get('phrase_input')
        new_password = request.form.get('new_password')
        confirm = request.form.get('confirm')
        user = User.query.filter_by(username=username).first()
        if not user:
            flash("User not found")
            return redirect(url_for('forgot_password'))
        # Verify phrase matches session stored phrase
        if phrase_input != session.get('reset_phrase'):
            flash("Phrase incorrect")
            return redirect(url_for('forgot_password'))
        if new_password != confirm:
            flash("Passwords do not match")
            return redirect(url_for('forgot_password'))
        if bcrypt.check_password_hash(user.password, new_password):
            flash("Cannot reuse the old password")
            return redirect(url_for('forgot_password'))
        user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        db.session.commit()
        flash("Password updated. Please log in.")
        return redirect(url_for('login'))
    # On GET, fetch a random phrase from Phrase table
    phrases = Phrase.query.all()
    if not phrases:
        # Seed some phrases if empty
        phrases_list = ["La pluie et le beau temps", "Chat échaudé craint l'eau froide", "Il ne faut pas vendre la peau de l'ours"]

        for p in phrases_list:
            db.session.add(Phrase(text=p))
        db.session.commit()
        phrases = Phrase.query.all()
    chosen = choice(phrases).text
    session['reset_phrase'] = chosen
    return render_template('auth/forgot_password.html', phrase=chosen)

# New admin users listing route
@app.route('/admin/users')
@admin_required
def admin_users():
    users = User.query.all()
    return render_template('admin/admin_users.html', users=users)

# New bulk upload route (for adding many users at once)
@app.route('/bulk_upload', methods=['GET', 'POST'])
@admin_required
def bulk_upload():
    if request.method == 'POST' and 'file' in request.files:
        file = request.files['file']
        import csv
        from io import StringIO
        stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        next(csv_input)  # skip header
        count = 0
        for row in csv_input:
            # Expect CSV columns: username, email, password, [isAdmin], [reward_points]
            if len(row) >= 3:
                new_user = User(
                    username=row[0],
                    email=row[1],
                    password=bcrypt.generate_password_hash(row[2]).decode('utf-8'),
                    isAdmin=(row[3].strip().lower()=='true') if len(row) > 3 else False,
                    reward_points=int(row[4]) if len(row) > 4 and row[4].isdigit() else 0
                )
                db.session.add(new_user)
                count += 1
        db.session.commit()
        flash(f"Bulk upload successful: {count} users added", "success")
        return redirect(url_for('admin_panel'))
    return render_template('admin/bulk_upload.html')

# Seed DB on first request with users id 0 and 1 and tasks
@app.before_request
def initialize_database():
    db.create_all()
    with db.engine.begin() as conn:
        result = conn.execute(text("PRAGMA table_info(user)"))
        columns = [row[1] for row in result.fetchall()]
        if "reward_points" not in columns:
            conn.execute(text("ALTER TABLE user ADD COLUMN reward_points INTEGER DEFAULT 0"))
        if "email" not in columns:
            conn.execute(text("ALTER TABLE user ADD COLUMN email TEXT DEFAULT ''"))
        if "isAdmin" not in columns:
            conn.execute(text("ALTER TABLE user ADD COLUMN isAdmin BOOLEAN DEFAULT 0"))
        
        # Check and add missing reward_given column in task table
        result = conn.execute(text("PRAGMA table_info(task)"))
        task_columns = [row[1] for row in result.fetchall()]
        if "reward_given" not in task_columns:
            conn.execute(text("ALTER TABLE task ADD COLUMN reward_given BOOLEAN DEFAULT 0"))
    # Create user with id=0 if not exists
    user0 = User.query.filter_by(id=0).first()
    if not user0:
        user0 = User(id=0, username='user0', email='user0@example.com',
                     password=bcrypt.generate_password_hash('password').decode('utf-8'))
        db.session.add(user0)
    # Create user with id=1 if not exists
    user1 = User.query.filter_by(id=1).first()
    if not user1:
        user1 = User(id=1, username='user1', email='user1@example.com',
                     password=bcrypt.generate_password_hash('password').decode('utf-8'))
        db.session.add(user1)
    # Create admin account if not exists
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin_user = User(username='admin',
                          email='admin@example.com',
                          password=bcrypt.generate_password_hash('admin').decode('utf-8'),
                          reward_points=100, isAdmin=True)
        db.session.add(admin_user)
    db.session.commit()
    # Seed tasks for user0 and user1 if none exist
    for user in [user0, user1]:
        if Task.query.filter_by(user_id=user.id).count() == 0:
            priorities = ['Low', 'Normal', 'High']
            now = datetime.now()
            # To-do tasks: not done and due in future
            for i in range(5):
                task = Task(user_id=user.id,
                            text=f"Task {i+1} to do",
                            done=False,
                            priority=priorities[i % len(priorities)],
                            created_time=now,
                            last_updated=now,
                            due_time=now + timedelta(hours=24))
                db.session.add(task)
            # Finished tasks: done tasks
            for i in range(5):
                task = Task(user_id=user.id,
                            text=f"Task {i+1} finished",
                            done=True,
                            priority=priorities[i % len(priorities)],
                            created_time=now - timedelta(days=1),
                            last_updated=now,
                            due_time=now + timedelta(hours=24))
                db.session.add(task)
            # Delayed tasks: not done and due in past
            for i in range(5):
                task = Task(user_id=user.id,
                            text=f"Task {i+1} delayed",
                            done=False,
                            priority=priorities[i % len(priorities)],
                            created_time=now - timedelta(days=2),
                            last_updated=now - timedelta(hours=2),
                            due_time=now - timedelta(hours=1))
                db.session.add(task)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
