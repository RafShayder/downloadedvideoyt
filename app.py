from flask import Flask, request, render_template, send_file
import os
from pytube import YouTube
from moviepy.editor import *

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Crear la carpeta de subidas si no existe
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
def download_video(url, output_path):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        stream.download(output_path=output_path)
        print(f'Descargado: {yt.title}')
    except Exception as e:
        print(f'Error: {e}')
   
def download_video_aduio(url, output_path):
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
    if stream:
        file_path = stream.download(output_path=output_path)
        return file_path
    return None

def download_audio(url, output_path):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
    if stream:
        file_path = stream.download(output_path=output_path)
        audio_path = os.path.splitext(file_path)[0] + '.mp3'
        audio_clip = AudioFileClip(file_path)
        audio_clip.write_audiofile(audio_path)
        os.remove(file_path)  # Eliminar el archivo de video original
        return audio_path
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        download_type = request.form.get('download_type')
        if url:
            if download_type == 'video':
                file_path = download_video(url, app.config['UPLOAD_FOLDER'])
            elif download_type =='audio':
                file_path = download_audio(url, app.config['UPLOAD_FOLDER'])
            elif download_type == 'video-aduio':
                file_path = download_video_aduio(url, app.config['UPLOAD_FOLDER'])
            else:
                return
            if file_path:
                return send_file(file_path, as_attachment=True)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
