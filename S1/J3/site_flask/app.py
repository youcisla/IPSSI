from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import case

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from pysondb import db as pysondb_db

db_path = "database.json"
a = pysondb_db.getDb(db_path)
if a.getAll():
    a.deleteAll()
print(a)

class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priorite = db.Column(db.String(20), nullable=False)
    creation_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    update_time = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Ticket id={self.id} titre={self.titre} priorite={self.priorite}>"

@app.before_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        titre = request.form.get('titre')
        description = request.form.get('description')
        priorite = request.form.get('priorite')
        nouveau_ticket = Ticket(titre=titre, description=description, priorite=priorite)
        db.session.add(nouveau_ticket)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        # Build query filters
        query = Ticket.query
        filter_titre = request.args.get('titre')
        filter_priorite = request.args.get('priorite')
        creation_from = request.args.get('creation_from')
        creation_to = request.args.get('creation_to')
        update_from = request.args.get('update_from')
        update_to = request.args.get('update_to')

        if filter_titre:
            query = query.filter(Ticket.titre.contains(filter_titre))
        if filter_priorite:
            query = query.filter(Ticket.priorite==filter_priorite)
        if creation_from:
            try:
                dt = datetime.strptime(creation_from, '%Y-%m-%d')
                query = query.filter(Ticket.creation_time >= dt)
            except:
                pass
        if creation_to:
            try:
                dt = datetime.strptime(creation_to, '%Y-%m-%d')
                query = query.filter(Ticket.creation_time <= dt)
            except:
                pass
        if update_from:
            try:
                dt = datetime.strptime(update_from, '%Y-%m-%d')
                query = query.filter(Ticket.update_time >= dt)
            except:
                pass
        if update_to:
            try:
                dt = datetime.strptime(update_to, '%Y-%m-%d')
                query = query.filter(Ticket.update_time <= dt)
            except:
                pass

        # Custom ordering based on priority (critique highest, then haute, normale, basse)
        priority_order = case(
            (Ticket.priorite=='critique', 1),
            (Ticket.priorite=='haute', 2),
            (Ticket.priorite=='normale', 3),
            (Ticket.priorite=='basse', 4),
            else_=5
        )
        query = query.order_by(priority_order, Ticket.creation_time.desc())

        # Pagination (10 tickets per page)
        page = request.args.get('page', 1, type=int)
        pagination = query.paginate(page=page, per_page=10, error_out=False)
        tickets = pagination.items

        return render_template('gestion_tickets.html', tickets=tickets, pagination=pagination)
    
@app.route('/update/<int:ticket_id>', methods=['GET', 'POST'])
def update_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if request.method == 'POST':
        ticket.titre = request.form.get('titre')
        ticket.description = request.form.get('description')
        ticket.priorite = request.form.get('priorite')
        ticket.update_time = datetime.utcnow()
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('update.html', ticket=ticket)

@app.route('/delete/<int:ticket_id>', methods=['POST'])
def delete_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    return redirect(url_for('index'))

# New routes for navigation links
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/tickets_in_progress')
def tickets_in_progress():
    return render_template('tickets_in_progress.html')

@app.route('/my_tickets')
def my_tickets():
    return render_template('my_tickets.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

if __name__ == '__main__':
    app.run()