from flask import Flask, render_template, request, jsonify
import yt_dlp
import os
import subprocess
from flask import send_file



app = Flask(__name__)

FFMPEG_PATH = "C:\\ffmpeg\\ffmpeg.exe"
os.environ["PATH"] += os.pathsep + os.path.dirname(FFMPEG_PATH)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')  # Ye HTML frontend ko load karega

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    format_type = data.get('format')
    start_time = data.get('startTime')
    end_time = data.get('endTime')

    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'ffmpeg_location': FFMPEG_PATH 
    }

    if format_type == "mp3":
        ydl_opts["format"] = "bestaudio"
        ydl_opts["postprocessors"] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    else:
        ydl_opts["format"] = "bestvideo+bestaudio"
        ydl_opts["postprocessors"] = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        if format_type == "mp3":
            filename = filename.rsplit('.', 1)[0] + ".mp3"
        else:
            filename = filename.rsplit('.', 1)[0] + ".mp4"
    
        if start_time and end_time:
            trimmed_filename = filename.replace(".", "_trimmed.")  # New trimmed file name
            trim_cmd = [
                FFMPEG_PATH, "-i", filename, "-ss", start_time, "-to", end_time, 
                "-c", "copy", trimmed_filename
            ]
            subprocess.run(trim_cmd, check=True)  # Run FFMPEG trimming
            filename = trimmed_filename  # S


    return send_file(filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
