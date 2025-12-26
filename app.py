from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import shutil

app = Flask(__name__)

# Katalog tymczasowy na serwerze
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form.get('url')
    
    if not video_url:
        return "Brak linku!", 400

    # Czyszczenie folderu downloads przed nowym pobraniem (żeby nie zapchać serwera)
    # W produkcji lepiej używać crona lub zadań w tle, ale to zadziała na start.
    for filename in os.listdir(DOWNLOAD_FOLDER):
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f'Nie udało się usunąć {file_path}. Powód: {e}')

    # Konfiguracja yt-dlp
    ydl_opts = {
        'format': 'best', # Próba pobrania najlepszej jakości (często wymaga ffmpeg na serwerze)
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'noplaylist': True,
        # Opcje by udawać przeglądarkę (pomaga na blokady):
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info_dict)
            
        return send_file(filename, as_attachment=True)

    except Exception as e:
        return f"Błąd serwera lub nieobsługiwany link: {str(e)}", 500

if __name__ == '__main__':
    # WAŻNE DLA HOSTINGU:
    # 1. host='0.0.0.0' sprawia, że strona jest dostępna z zewnątrz.
    # 2. Pobieramy PORT z systemu (wymagane przez Heroku, Render itp.)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)