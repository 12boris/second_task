from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class entryes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entry = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return '<entry %r>' % self.entry
    
    
@app.route('/entry', methods=['GET', 'POST'])
def my_entry():
    if request.method == 'POST':

        # запись
        content_entry = request.form['entry']
        entry = entryes.query.first()
        entry.entry = content_entry
        db.session.commit()

        print(entry)

        return render_template('bots.html', entry=entry)
    
    else:
        # запись
        entry = entryes.query.first()
        return render_template('bots.html', entry=entry)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not entryes.query.first():
            first_entry = entryes(entry="")
            db.session.add(first_entry)
            db.session.commit()
        
    app.run(debug=False, port=5050)
