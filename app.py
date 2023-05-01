from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class entryes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(300), nullable=False)
    entry = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return '<entry %r>' % self.name
    

# так как скрипт предназначен для одного человека, 
# то записи не сортируются по их владельцу
@app.route('/entry', methods=['GET', 'POST'])
def my_entry():
    if request.method == 'POST':
        # удаление записи
        try:
            entry_id = request.form['deleted_entry']
            entry = entryes.query.filter_by(id=entry_id).first()
            db.session.delete(entry)
            db.session.commit()
        except:
            pass

        # список записей
        entryes_list = entryes.query.all()
        return render_template('bots.html', entryes_list=entryes_list)
    
    else:
        # список записей
        entryes_list = entryes.query.all()
        return render_template('bots.html', entryes_list=entryes_list)
    

# добавление записи
@app.route('/entry-add', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        # создание записи
        try:
            insert_entry = request.form['entry']
            name = insert_entry[:10]
            entry = entryes(name=name, entry=insert_entry)
            db.session.add(entry)
            db.session.commit()
        except:
            pass

        # список записей
        entryes_list = entryes.query.all()
        return render_template('bots.html', entryes_list=entryes_list)
    
    else:
        # список записей
        entryes_list = entryes.query.all()
        return render_template('bots.html', entryes_list=entryes_list)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
    app.run(debug=False, port=5050)
