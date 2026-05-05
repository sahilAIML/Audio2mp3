import sys
import os
import zipfile
import threading
import uuid
from io import BytesIO
from flask import Flask, render_template, request, send_file, jsonify
from pydub import AudioSegment
from werkzeug.utils import secure_filename
from flaskwebgui import FlaskUI

# --- PyInstaller Path Fix ---
def get_base_path():
    """Gets the absolute path to the bundled files when running as an .exe"""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

base_dir = get_base_path()

# Initialize Flask with the correct paths for templates and static files (like your logo)
app = Flask(__name__, 
            template_folder=os.path.join(base_dir, 'templates'),
            static_folder=os.path.join(base_dir, 'static'))

UPLOAD_FOLDER = 'temp_audio'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global dictionary to track progress of background tasks
TASKS = {}

def parse_time_to_ms(time_str):
    """Converts MM:SS or SS string to milliseconds."""
    if not time_str or time_str.strip() == "": return None
    try:
        parts = time_str.split(':')
        if len(parts) == 2:
            return (int(parts[0]) * 60 + float(parts[1])) * 1000
        return float(parts[0]) * 1000
    except:
        return None

def process_conversion(task_id, files_data, bitrate):
    """Runs in background thread to process files and update progress."""
    try:
        converted_files = []
        total_files = len(files_data)

        for index, data in enumerate(files_data):
            # Update Progress
            TASKS[task_id]['status'] = f"Converting {index + 1} of {total_files}: {data['filename']}"
            TASKS[task_id]['progress'] = int((index / total_files) * 100)

            input_path = data['path']
            name_only = os.path.splitext(data['filename'])[0]
            output_path = os.path.join(UPLOAD_FOLDER, f"{name_only}.mp3")

            # Load audio
            audio = AudioSegment.from_file(input_path)

            # Apply Trimming if requested
            start_ms = parse_time_to_ms(data['start'])
            end_ms = parse_time_to_ms(data['end'])
            
            if start_ms is not None and end_ms is not None:
                audio = audio[start_ms:end_ms]
            elif start_ms is not None:
                audio = audio[start_ms:]
            elif end_ms is not None:
                audio = audio[:end_ms]

            # Export
            audio.export(output_path, format="mp3", bitrate=bitrate)
            converted_files.append(output_path)

        # Zip files if multiple
        if len(converted_files) > 1:
            TASKS[task_id]['status'] = "Zipping files..."
            zip_path = os.path.join(UPLOAD_FOLDER, f"converted_batch_{task_id}.zip")
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for file_path in converted_files:
                    zf.write(file_path, os.path.basename(file_path))
            TASKS[task_id]['result_file'] = zip_path
        else:
            TASKS[task_id]['result_file'] = converted_files[0]

        # Finalize
        TASKS[task_id]['progress'] = 100
        TASKS[task_id]['status'] = "Complete!"
        TASKS[task_id]['ready'] = True

    except Exception as e:
        TASKS[task_id]['error'] = str(e)
        TASKS[task_id]['status'] = "Failed."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    files = request.files.getlist('files')
    start_times = request.form.getlist('start_times')
    end_times = request.form.getlist('end_times')
    bitrate = request.form.get('bitrate', '192k')

    if not files or files[0].filename == '':
        return jsonify({'error': 'No files provided'}), 400

    task_id = str(uuid.uuid4())
    TASKS[task_id] = {'progress': 0, 'status': 'Starting...', 'ready': False, 'error': None}

    # Save uploaded files temporarily
    files_data = []
    for i, file in enumerate(files):
        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, f"{task_id}_{filename}")
        file.save(input_path)
        
        files_data.append({
            'filename': filename,
            'path': input_path,
            'start': start_times[i] if i < len(start_times) else "",
            'end': end_times[i] if i < len(end_times) else ""
        })

    # Start background thread
    thread = threading.Thread(target=process_conversion, args=(task_id, files_data, bitrate))
    thread.daemon = True
    thread.start()

    return jsonify({'task_id': task_id})

@app.route('/status/<task_id>')
def status(task_id):
    return jsonify(TASKS.get(task_id, {'error': 'Task not found'}))

@app.route('/download/<task_id>')
def download(task_id):
    task = TASKS.get(task_id)
    if not task or not task.get('ready'):
        return "File not ready", 400
    
    file_path = task['result_file']
    filename = os.path.basename(file_path)
    
    # Send file
    response = send_file(file_path, as_attachment=True, download_name=filename)
    return response

if __name__ == '__main__':
    # FlaskUI turns the web app into a standalone desktop window!
    FlaskUI(app=app, server="flask", width=850, height=750).run()