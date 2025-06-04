from flask import Flask, render_template, request, redirect, url_for
from google.cloud import firestore

app = Flask(__name__)
db = firestore.Client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_video():
    custom_title = request.form['custom_title']
    youtube_url = request.form['youtube_url']
    
    # Валидация URL
    if not ('youtube.com' in youtube_url or 'youtu.be' in youtube_url):
        return "Incorrect YouTube URL!", 400
    
    # Добавление в Firestore
    doc_ref = db.collection('videos').document()
    doc_ref.set({
        'custom_title': custom_title,
        'youtube_url': youtube_url
    })
    
    return redirect(url_for('show_videos'))

@app.route('/videos')
def show_videos():
    videos = []
    docs = db.collection('videos').stream()
    for doc in docs:
        video = doc.to_dict()
        video['id'] = doc.id
        videos.append(video)
    return render_template('videos.html', videos=videos)