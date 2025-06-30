from flask import Flask, jsonify,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context().push()
class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    time=db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self): 
        return f"{self.sno}-{self.title}"
@app.route('/', methods=['GET','POST'])
def first():
    if request.method=='POST':
       title=request.form['title']
       desc=request.form['desc']
       todos=Todo(title=title, desc=desc)
       db.session.add(todos)
       db.session.commit()
    alltodos=Todo.query.all()
    print(alltodos)
    return render_template("index.html",alltodos=alltodos)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()#where clause
    if todo is not None:

      db.session.delete(todo)
      db.session.commit()
    else:
        print(f"no todo is found with sno={sno}")
    return redirect('/')

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
     title=request.form['title']
     desc=request.form['desc']   
     todo=Todo.query.filter_by(sno=sno).first()
     todo.title=title
     todo.desc=desc
     db.session.add(todo)
     db.session.commit()

     return redirect('/')
    todo=Todo.query.filter_by(sno=sno).first()
     
    return render_template('update.html',todo=todo)



if __name__ == '__main__':
    app.run(debug=True)
