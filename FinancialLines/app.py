
from flask import Flask,render_template, request, redirect,Blueprint,abort
from flask_caching import Cache
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


financiallines = Blueprint(
    'financiallines', 
    __name__,
    template_folder='../templates/financiallines',  # Path to the templates
    static_folder='../static/financiallines',  # Path to the static files

)

@financiallines.before_request
def before_request_func():
    # You can check the request path or other request properties here
    print("Hello")



cache = Cache(config={'CACHE_TYPE': 'filesystem'})
# Database URI
DATABASE_URI = 'sqlite:///FinancialLines.db'

# Set up the engine
engine = create_engine(DATABASE_URI)

# Base class for your models
Base = declarative_base()

# Define your Entry model
class Entry(Base):
    __tablename__ = 'Financiallines_todo'

    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)
    description = Column(String(120), nullable=False)
    status = Column(Boolean, default=False)

# Create tables in the database
Base.metadata.create_all(engine)

# Set up the session
Session = sessionmaker(bind=engine)
session = Session()


@financiallines.route('/')
def index():
    # entries = [
    #     {
    #         'id' : 1,
    #         'title': 'test title 1',
    #         'description' : 'test desc 1',
    #         'status' : True
    #     },
    #     {
    #         'id': 2,
    #         'title': 'test title 2',
    #         'description': 'test desc 2',
    #         'status': False
    #     }
    # ]
    entries = session.query(Entry).all()
    return render_template('index.html', entries=entries)

@financiallines.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        form = request.form
        title = form.get('title')
        description = form.get('description')
        if not title or description:
            entry = Entry(title = title, description = description)
            session.add(entry)
            session.commit()
            return redirect('/financiallines')

    return "of the jedi"

@financiallines.route('/update/<int:id>')
def updateRoute(id):
    if not id or id != 0:
        entry = session.query(Entry).get(id) 
        if entry:
            return render_template('update.html', entry=entry)

    return "of the jedi"

@financiallines.route('/update/<int:id>', methods=['POST'])
def update(id):
    if not id or id != 0:
        entry = session.query(Entry).get(id)
        if entry:
            form = request.form
            title = form.get('title')
            description = form.get('description')
            entry.title = title
            entry.description = description
            session.commit()
        return redirect('/financiallines')

    return "of the jedi"



@financiallines.route('/delete/<int:id>')
def delete(id):
    if not id or id != 0:
        entry = session.query(Entry).get(id)
        if entry:
            session.delete(entry)
            session.commit()
        return redirect('/financiallines')

    return "of the jedi"

@financiallines.route('/turn/<int:id>')
def turn(id):
    if not id or id != 0:
        entry = session.query(Entry).get(id)
        if entry:
            entry.status = not entry.status
            session.commit()
        return redirect('/financiallines')

    return "of the jedi"

