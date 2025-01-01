from flask import Flask , render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    srno = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String(200) ,  nullable = False )
    desc = db.Column(db.String(500)   ,nullable = False)
    date_created = db.Column(db.DateTime , default= datetime.now)

    # Defines what object will return i.e sr. no and description when printed
    def __repr__(self) -> str:
        return f"{self.srno} - {self.desc}"


@app.route('/' , methods=['POST' , 'GET'])
def home():
    if( request.method == "POST"):
        title = request.form['title']
        desc = request.form['desc']
        add_todo = Todo( title= title , desc = desc)
        db.session.add(add_todo)
        db.session.commit()


    all_todo = Todo.query.all()

    return render_template('index.html',all_todo = all_todo)

@app.route('/update/<int:todo_id>', methods=["POST", "GET"] )
def update(todo_id):
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']

        update_todo = Todo.query.filter_by(srno=todo_id).first()
        update_todo.title = title
        update_todo.desc = desc

        db.session.add(update_todo)
        db.session.commit()
        
        return redirect("/")
    update_todo = Todo.query.filter_by(srno=todo_id).first()
    return render_template("update.html",todo=update_todo)


@app.route( '/delete/<int:todo_id>' , methods = ['POST', 'GET'] )
def delete(todo_id):
    del_todo = Todo.query.filter_by(srno=todo_id).first()
    db.session.delete(del_todo)
    db.session.commit()
    return redirect("/")

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == '__main__':
    #Create database
    with app.app_context():
        db.create_all()
    app.run(debug=True)
        