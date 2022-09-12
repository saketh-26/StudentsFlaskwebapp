from flask import Flask,render_template,request,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import os

#database file path
basedir = os.path.abspath(os.path.dirname(__file__)) #basedirectory -->current directory
#print(__name__)
app = Flask(__name__)
#adding configurations
#database URI to specify the database you want to establish the
#connection
app.config['SQLALCHEMY_DATABASE_URI']=\
                                        'sqlite:///'+os.path.join(basedir,'studentsdata.db')

#to enable or disable tracking modifications of objects
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#print(db)
#print(dir(db))
#creating a class for storing students table

class Students(db.Model):
    id = db.Column(db.Integer,primary_key =True)
    firstname = db.Column(db.String(100),nullable =False)
    lastname = db.Column(db.String(100),nullable =False)
    email= db.Column(db.String(100),unique=True,nullable =False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    bio = db.Column(db.Text)

    def __repr__(self):
        return f'<Students {self.firstname}'

@app.route('/')
def index():
    students = Students.query.all()
    return render_template('index.html',students=students)

@app.route('/<int:student_id>/')
def student(student_id):
    student = Students.query.get_or_404(student_id)
    return render_template('student.html',student=student)

@app.route('/create/',methods=['GET','POST'])
def create():
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        age = request.form['age']
        bio = request.form['bio']
        student = Students(firstname=firstname,lastname=lastname,
                          email=email,age=age,bio=bio)
        db.session.add(student)
        db.session.commit()

        return redirect(url_for('index'))
        
    return render_template('create.html')

@app.route('/<int:student_id>/edit/', methods=['GET', 'POST'])
def edit(student_id):
    student = Students.query.get_or_404(student_id)

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        age = int(request.form['age'])
        bio = request.form['bio']

        student.firstname = firstname
        student.lastname = lastname
        student.email = email
        student.age = age
        student.bio = bio

        db.session.add(student)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit.html', student=student)

@app.post('/<int:student_id>/delete/')
def delete(student_id):
    student = Students.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run()
    
    
    
    




        
