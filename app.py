import os

from datetime import datetime
from dateutil import tz
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'host': os.environ.get('DATABASE_URL')
}


db = MongoEngine()
db.init_app(app)

from_zone=tz.tzutc() # do timezone UTC
to_zone = tz.tzstr('BRST+3') #para o timezone do brasil


class Todo(db.Document):
    id = db.ObjectIdField(primary_key=True)
    title = db.StringField(max_length=(256), required=True)
    done = db.BooleanField()
    dated_at = db.DateTimeField()


    def to_json(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'done': self.done,
            'dated_at': self.dated_at
        }


@app.route('/')
def index():
    todo_list = Todo.objects().order_by('-dated_at').all()
    for todo in todo_list:
        todo.dated_at = todo.dated_at.replace(tzinfo=from_zone)
        todo.dated_at = todo.dated_at.astimezone(to_zone)
    return render_template('index.html', lista = todo_list)


@app.route('/create', methods=['POST'])
def create():
    item_title = request.form.get('title')
    new_item = Todo(id=ObjectId(), title=item_title, done=False, dated_at=datetime.utcnow())
    new_item.save()
    return redirect(url_for('index'))


@app.route('/delete/<string:item_id>')
def delete(item_id):
    item = Todo.objects(id = item_id).first()
    item.delete()
    return redirect(url_for('index'))


@app.route('/update/<string:item_id>', methods=['POST'])
def updat_tittle(item_id):
    new_title = request.form.get('new_title')
    item = Todo.objects(id = item_id).first()
    item.update(title=new_title)
    return redirect(url_for('index'))


@app.route('/change-status/<string:item_id>')
def change_status(item_id):
    item = Todo.objects(id=item_id).first()
    item.update(done=not item.done)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()