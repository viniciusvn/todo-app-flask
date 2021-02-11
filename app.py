from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'


db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    done = db.Column (db.Boolean)
    dated_at = db.Column(db.DateTime)



@app.route('/')
def index():
    todo_list = Todo.query.all()
    return render_template('index.html', lista = todo_list)

@app.route('/create', methods=['POST'])
def create():
    item_title = request.form.get('title')
    new_item = Todo(title=item_title, done=False, dated_at=datetime.utcnow())
    db.session.add(new_item)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete/<int:item_id>')
def delete(item_id):
    item = Todo.query.filter_by(id = item_id).first()
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:item_id>', methods=['POST'])
def updat_tittle(item_id):
    new_title = request.form.get('new_title')
    item = Todo.query.filter_by(id = item_id).first()
    item.title = new_title
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/change-status/<int:item_id>')
def change_status(item_id):
    item = Todo.query.filter_by(id=item_id).first()
    item.done = not item.done
    db.session.commit()
    return redirect(url_for('index'))

    



if __name__ == '__main__':
    db.create_all()
    app.run()

