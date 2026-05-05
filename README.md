# 🎵 Audio2MP3 Pro: Seamless Audio Conversion Tool

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-WebGUI-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Audio2MP3 Pro** is a lightweight, offline desktop application designed to solve a common media compatibility issue: converting various audio formats into standard MP3 files. Built with a powerful Python backend and a stunning, animated **Claymorphism** frontend, this tool guarantees privacy, speed, and a delightful user experience.

---

## 📖 Abstract & Overview

Students and professionals frequently encounter audio format issues when downloading lectures, utilizing sound clips, or sharing voice notes. While online converters exist, they require internet access, enforce strict file size limits, and risk user privacy. 

**Audio2MP3 Pro** brings the power of format conversion directly to your desktop. It works entirely offline, ensuring that private audio files are never uploaded to a third-party server, effectively saving time and removing technical frustration from daily workflows.

---

## ✨ Features

- **Universal Format Support:** Convert `.wav`, `.flac`, `.aac`, `.ogg`, `.m4a`, and `.wma` seamlessly to `.mp3`.
- **100% Offline & Private:** Audio is processed entirely on your local machine.
- **Audio Trimming:** Specify exact Start and End times to extract specific snippets of audio.
- **Live Preview Player:** Listen to your audio files directly inside the queue before converting.
- **Batch Processing:** Drag and drop multiple files to convert them all at once. Automatically packages bulk conversions into a clean `.zip` file.
- **Custom Quality:** Select your preferred bitrate (128kbps, 192kbps Standard, or 320kbps Lossless).
- **Modern Claymorphism UI:** Features an animated, tactile interface with Dark/Light mode support and native system window integration.

---

# 📸 Screenshots


## Dashboard (Dark Mode)
<img width="1918" height="1016" alt="Dark" src="https://github.com/user-attachments/assets/71572fab-939a-4aa2-88e0-d12bce85ca18" />

##  Dashboard (Light Mode)

<img width="1918" height="1022" alt="Light" src="https://github.com/user-attachments/assets/c663b7c9-5dac-48e0-bb2c-ea4ceb71d14f" />

## ⚙️ System Design & Architecture

### How the Application Works Step-by-Step:
1. **Initialization:** The Python script uses `flaskwebgui` to launch a local server and seamlessly bind it to a native desktop Chrome window.
2. **File Selection:** Users interact with the drag-and-drop HTML5 UI to queue audio files.
3. **Processing Trigger:** The frontend sends the files and user preferences (bitrate, trim times) to the Flask backend asynchronously.
4. **Audio Transcoding:** The application utilizes the `pydub` library, which relies on the `FFmpeg` engine, to read the original audio data and mathematically encode it into MP3 format.
5. **Saving the File:** The generated MP3 file is instantly downloaded back to the user's system. If multiple files are processed, they are dynamically compressed into a `.zip` archive.

---

## 💻 System Requirements

**Hardware Requirements:**
* **Processor:** Intel Core i3 / AMD Ryzen 3 (or equivalent)
* **Memory:** Minimum 4GB RAM (8GB recommended for batch processing)
* **Storage:** At least 200MB of free disk space

**Software Requirements:**
* **Operating System:** Windows 10 / Windows 11 (Compatible with macOS/Linux via source)
* **FFmpeg:** Must be installed and added to the system PATH.

---

## 🚀 Installation & Setup

### Option 1: Run as a Standalone App (.exe)
If you have the compiled executable, simply double-click `AudioConverterPro.exe` to launch the application. No installation is required!

### Option 2: Run from Source (For Developers)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YourUsername/Audio-to-MP3-Pro.git
   cd Audio-to-MP3-Pro

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check out the issues page if you'd like to help improve the project.

1. Fork the Project
2. Create your Feature Branch: git checkout -b feature/AmazingFeature
3. Commit your Changes: git commit -m 'Add some AmazingFeature'
4. Push to the Branch: git push origin feature/AmazingFeature
5. Open a Pull Request

### Developed with ❤️ by Sahil
