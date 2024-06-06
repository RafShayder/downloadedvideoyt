from pytube import YouTube
from moviepy.editor import *
import speech_recognition as sr
def download_video(url, path='.'):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        stream.download(output_path=path)
        print(f'Descargado: {yt.title}')
    except Exception as e:
        print(f'Error: {e}')
        
def convert_to_mp3(input_file, output_file):
    try:
        audio_clip = AudioFileClip(input_file)
        audio_clip.write_audiofile(output_file,codec='mp3')
        print(f'Convertido a: {output_file}')
    except Exception as e:
        print(f'Error en la conversión: {e}')

def download_audio(url, path='.'):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        audio_file=stream.download(output_path=path)
        base, _ = os.path.splitext(audio_file)
        mp3_file = f"{base}.mp3"
        convert_to_mp3(audio_file,mp3_file)
        os.remove(audio_file)
        print(f'Descargado: {yt.title}')
    except Exception as e:
        print(f'Error: {e}')
        
def download_video_with_audio(url, output_path='.'):
    try:
        yt = YouTube(url)
        # Filtrar los streams para obtener el que contiene video y audio juntos
        stream = yt.streams.filter(progressive=True, file_extension='mp4',resolution='720p').first()
        if stream:
            m=stream.download(output_path=output_path)
            print(m)
            print(f'Video descargado: {yt.title}')
        else:
            print('No se encontró un stream de video con audio.')
    except Exception as e:
        print(f'Error: {e}')
        
    
def audio_to_text(audio_file, segment_duration=30):
    # Convertir MP3 a WAV
    sound = AudioFileClip(audio_file)
    audio_file_wav = audio_file.replace(".mp3", ".wav")
    sound.write_audiofile(audio_file_wav)

    # Dividir el audio en segmentos y reconocer cada segmento
    recognizer = sr.Recognizer()
    audio = AudioFileClip(audio_file_wav)
    audio_duration = audio.duration
    texts = []

    for start in range(0, int(audio_duration), segment_duration):
        end = min(start + segment_duration, int(audio_duration))
        segment = audio.subclip(start, end)
        segment_file = f"segment_{start}_{end}.wav"
        segment.write_audiofile(segment_file)

        with sr.AudioFile(segment_file) as source:
            audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data,language='en-EN') # language='es-ES'
            texts.append(text)
        except sr.UnknownValueError:
            print("No se pudo entender el audio")
        except sr.RequestError as e:
            print(f"Error al conectarse al servicio de reconocimiento de voz: {e}")

        # Eliminar el archivo de segmento temporal
        os.remove(segment_file)

    # Unir los textos reconocidos
    full_text = ' '.join(texts)
    return full_text

    
    
# Ejemplo de uso
video_url = 'https://youtu.be/Qc7_zRjH808?list=RDQc7_zRjH808'
#download_video(video_url)
#download_audio(video_url)
#download_video_with_audio(video_url)

