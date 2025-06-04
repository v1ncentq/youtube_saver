from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    custom_title = db.Column(db.String(100), nullable=False)
    youtube_url = db.Column(db.String(200), nullable=False)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_video():
    custom_title = request.form['custom_title']
    youtube_url = request.form['youtube_url']
    
    # Простая валидация URL
    if 'youtube.com' not in youtube_url and 'youtu.be' not in youtube_url:
        return "Неверная YouTube ссылка!", 400
    
    new_video = Video(custom_title=custom_title, youtube_url=youtube_url)
    db.session.add(new_video)
    db.session.commit()
    
    return redirect(url_for('show_videos'))

@app.route('/videos')
def show_videos():
    videos = Video.query.all()
    return render_template('videos.html', videos=videos)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)