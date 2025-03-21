from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from .models import db, User, Ticket
from functools import wraps
from sqlalchemy import or_

bp = Blueprint('main', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.register'))

@bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    user_id = session['user_id']
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '').strip()
    status_filter = request.args.get('status', '').strip()
    if session.get('role') == 'admin':
        query = Ticket.query
    else:
        query = Ticket.query.filter_by(user_id=user_id)
    if search:
        query = query.filter((Ticket.title.ilike(f"%{search}%")) | (Ticket.description.ilike(f"%{search}%")))
    if status_filter:
        query = query.filter_by(status=status_filter)
    tickets = query.order_by(Ticket.id.desc()).paginate(page=page, per_page=9, error_out=False)
    return render_template('dashboard.html', tickets=tickets, search=search, status_filter=status_filter)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['role'] = user.role
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = 'user'
        status = 'active'
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
        else:
            user = User(username=username, role=role, status=status)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('main.login'))
    return render_template('register.html')

@bp.route('/tickets/new', methods=['GET', 'POST'])
def new_ticket():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    # New user existence check
    user = User.query.get(session['user_id'])
    if not user:
        flash("User not found. Please log in again.", "danger")
        return redirect(url_for('main.login'))
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        ticket = Ticket(title=title, description=description, status=status, user_id=user.id)
        db.session.add(ticket)
        db.session.commit()
        flash('Ticket created successfully!', 'success')
        return redirect(url_for('main.dashboard', _external=True))
    return render_template('ticket_form.html', ticket=None)

@bp.route('/tickets/<int:id>/edit', methods=['GET', 'POST'])
def edit_ticket(id):
    ticket = Ticket.query.get_or_404(id)
    if ticket.user_id != session['user_id']:
        flash('You do not have permission to edit this ticket.', 'danger')
        return redirect(url_for('main.dashboard'))
    if request.method == 'POST':
        ticket.title = request.form['title']
        ticket.description = request.form['description']
        ticket.status = request.form['status']
        db.session.commit()
        flash('Ticket updated successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('ticket_form.html', ticket=ticket)

@bp.route('/tickets/<int:id>/delete', methods=['POST'])
def delete_ticket(id):
    ticket = Ticket.query.get_or_404(id)
    if ticket.user_id != session['user_id']:
        flash('You do not have permission to delete this ticket.', 'danger')
        return redirect(url_for('main.dashboard'))
    db.session.delete(ticket)
    db.session.commit()
    flash('Ticket deleted successfully!', 'success')
    return redirect(url_for('main.dashboard'))

@bp.route('/admin')
@admin_required
def admin():
    users = User.query.all()
    total_users = User.query.count()
    total_tickets = Ticket.query.count()
    active_users = User.query.filter_by(status='active').count()
    inactive_users = User.query.filter_by(status='inactive').count()
    latest_ticket = Ticket.query.order_by(Ticket.id.desc()).first()
    search = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    query = Ticket.query
    if search:
        query = query.filter(or_(Ticket.title.ilike(f"%{search}%"), Ticket.description.ilike(f"%{search}%"), Ticket.status.ilike(f"%{search}%")))
    tickets_pagination = query.order_by(Ticket.id.desc()).paginate(page=page, per_page=9, error_out=False)
    return render_template('admin.html', users=users, total_users=total_users, total_tickets=total_tickets, active_users=active_users, inactive_users=inactive_users, latest_ticket=latest_ticket, tickets=tickets_pagination, search=search)

@bp.route('/admin/user/<int:id>/tickets')
@admin_required
def user_tickets(id):
    user = User.query.get_or_404(id)
    tickets = Ticket.query.filter_by(user_id=user.id).all()
    return render_template('tickets.html', tickets=tickets)

@bp.route('/admin/user/<int:id>/modify_status', methods=['POST'])
@admin_required
def modify_user_status(id):
    user = User.query.get_or_404(id)
    user.status = request.form['status']
    db.session.commit()
    flash('User status updated successfully!', 'success')
    return redirect(url_for('main.admin'))
