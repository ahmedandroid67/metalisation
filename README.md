# Arabic Portrait Generator with Gemini AI 🎨

A professional web application that generates stunning metallic portrait artworks with Arabic calligraphy using Google's Gemini AI.

## ✨ Features

- **Upload Photo**: Drag-and-drop or click to upload your portrait photo
- **Arabic Calligraphy**: Enter an Arabic name that will be rendered in elegant 3D metallic calligraphy
- **AI-Powered Generation**: Uses Gemini AI to create professional-quality artwork
- **Metallic Aesthetic**: Chrome/silver finish with dramatic lighting on dark teal-to-black gradient
- **RTL Support**: Full right-to-left layout for Arabic interface
- **Responsive Design**: Works beautifully on desktop, tablet, and mobile devices
- **Download Results**: Save your generated portraits directly

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Gemini API key (already configured in `.env`)

### Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Flask server:**
   ```bash
   python app.py
   ```
   
   The server will start on `http://localhost:5000`

3. **Open the web application:**
   - Simply open `index.html` in your web browser
   - Or use a local server for better performance:
     ```bash
     python -m http.server 8000
     ```
   - Then visit `http://localhost:8000`

## 💡 How to Use

1. **Upload Your Photo**: Click or drag-and-drop a portrait photo (PNG, JPG, JPEG)
2. **Enter Arabic Name**: Type the name in Arabic that you want displayed
3. **Generate**: Click the "إنشاء الصورة الاحترافية" button
4. **Download**: Save your generated metallic portrait

## 🎨 Generated Portrait Style

The AI creates portraits with:
- **Metallic silver/chrome illustration** with dramatic lighting
- **Dark teal-to-black gradient background** for professional look
- **3D Arabic calligraphy** with polished chrome finish
- **Cinematic lighting** emphasizing facial features
- **High-resolution output** with smooth metallic textures

## 🔧 Technical Stack

### Backend
- **Flask**: Python web framework
- **Google Generative AI**: Gemini API for image generation
- **Pillow**: Image processing
- **Flask-CORS**: Cross-origin resource sharing

### Frontend
- **HTML5**: Semantic structure
- **CSS3**: Modern styling with glassmorphism effects
- **JavaScript**: Interactive functionality
- **Google Fonts**: Cairo & Amiri for Arabic typography

## 📁 Project Structure

```
Metalise/
├── app.py                 # Flask backend server
├── index.html            # Main web page
├── style.css             # Styling with metallic aesthetic
├── script.js             # Frontend functionality
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (API key)
├── .env.example         # Environment template
├── .gitignore           # Git ignore rules
├── README.md            # This file
└── uploads/             # Temporary upload folder (auto-created)
```

## 🔐 Environment Variables

The `.env` file contains:
- `GEMINI_API_KEY`: Your Gemini API key
- `FLASK_SECRET_KEY`: Flask session secret

## 🌐 API Endpoints

- `GET /api/health`: Health check endpoint
- `POST /api/generate`: Generate portrait with Arabic calligraphy
  - Form data: `image` (file), `arabicName` (string)
  - Returns: Base64-encoded generated image

## 🎯 Browser Support

- Chrome/Edge (recommended)
- Firefox
- Safari
- Opera

## 📝 Notes

- Maximum image upload size: 16MB
- Supported formats: PNG, JPG, JPEG
- Internet connection required for Gemini API
- Processing time: 5-15 seconds per image

## 🐛 Troubleshooting

### Server won't start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that port 5000 is not in use

### API errors
- Verify your Gemini API key in `.env`
- Check your internet connection
- Ensure you have API quota remaining

### Image generation fails
- Verify your API key has Imagen access
- Check file size (must be under 16MB)
- Try a different portrait photo

## 📄 License

This project is for personal use. Ensure compliance with Google's Gemini AI terms of service.

## 🙏 Credits

- Powered by Google Gemini AI
- Arabic fonts: Cairo & Amiri from Google Fonts
- Created with ❤️ for Arabic portrait generation

---

**Enjoy creating stunning metallic portraits! ✨🎨**
