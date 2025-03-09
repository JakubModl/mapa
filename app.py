
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
import os
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    places = Place.query.all()
    return render_template('index.html', places=places)

@app.route('/zapisnicek')
def zapisnicek():
    notes = Note.query.order_by(Note.timestamp.desc()).all()
    return render_template('zapisnicek.html', notes=notes)

@app.route('/add_place', methods=['POST'])
def add_place():
    try:
        name = request.form.get('name')
        lat = float(request.form.get('lat'))
        lng = float(request.form.get('lng'))
        date = request.form.get('date')

        if not name or not lat or not lng or not date:
            return "Missing data", 400

        timestamp = datetime.strptime(date, '%Y-%m-%dT%H:%M')
        new_place = Place(name=name, lat=lat, lng=lng, timestamp=timestamp)
        db.session.add(new_place)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error: {e}")
        return "Invalid data", 400

@app.route('/delete_place/<int:id>', methods=['POST'])
def delete_place(id):
    place = Place.query.get(id)
    if place:
        db.session.delete(place)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/update_place/<int:id>', methods=['POST'])
def update_place(id):
    try:
        place = Place.query.get(id)
        if place:
            place.name = request.form['name']
            place.timestamp = datetime.strptime(request.form['date'], '%Y-%m-%dT%H:%M')
            db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error: {e}")
        return "Invalid data", 400

@app.route('/add_note', methods=['POST'])
def add_note():
    content = request.form.get('content')
    if content:
        new_note = Note(content=content)
        db.session.add(new_note)
        db.session.commit()
    return redirect(url_for('zapisnicek'))

@app.route('/delete_note/<int:id>', methods=['POST'])
def delete_note(id):
    note = Note.query.get(id)
    if note:
        db.session.delete(note)
        db.session.commit()
    return redirect(url_for('zapisnicek'))

@app.route('/get_places', methods=['GET'])
def get_places():
    places = Place.query.all()
    places_list = [{'id': place.id, 'name': place.name, 'lat': place.lat, 'lng': place.lng, 'timestamp': place.timestamp.strftime('%Y-%m-%d %H:%M:%S')} for place in places]
    return jsonify(places_list)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

