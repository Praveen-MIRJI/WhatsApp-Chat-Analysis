# 💬 WhatsApp Chat Analyzer

A comprehensive Streamlit application for analyzing WhatsApp chat data with beautiful visualizations and insights.

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.50+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🚀 Live Demo

[![Deploy on Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

## ✨ Features

- 📊 **Message Statistics**: Total messages, words, media, and links
- 📈 **Timeline Analysis**: Daily and monthly activity patterns
- 🗓️ **Activity Heatmaps**: Hour vs day activity visualization
- 👥 **User Analysis**: Most active users and engagement metrics
- ☁️ **Word Clouds**: Visual representation of most used words
- 📝 **Common Words**: Bar charts of frequent words
- 😀 **Emoji Analysis**: Emoji usage statistics and pie charts
- 🎨 **Professional UI**: Beautiful gradient design with responsive layout

## 🛠️ Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/whatsapp-chat-analysis.git
   cd whatsapp-chat-analysis
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   ```
   http://localhost:8501
   ```

## 📱 Usage

1. **Export WhatsApp Chat**
   - Open WhatsApp → Select Chat → Menu → More → Export Chat
   - Choose "Without Media" for faster processing

2. **Upload File**
   - Click "Choose a file" in the sidebar
   - Select your exported WhatsApp chat file (.txt)

3. **Select Analysis**
   - Choose "Overall" for group analysis
   - Select specific user for individual analysis
   - Click "🚀 Start Analysis"

4. **Explore Insights**
   - View comprehensive statistics and visualizations
   - Analyze patterns and trends in your chat data

## 🎨 Screenshots

### Dashboard
![Dashboard](https://via.placeholder.com/800x400/667eea/ffffff?text=Dashboard+View)

### Analytics
![Analytics](https://via.placeholder.com/800x400/764ba2/ffffff?text=Analytics+View)

## 🚀 Deployment

### Heroku
```bash
heroku create your-app-name
git push heroku main
```

### Streamlit Cloud
1. Push to GitHub
2. Connect at https://share.streamlit.io
3. Deploy with one click

### Railway
```bash
railway login
railway init
railway up
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 📊 Supported Formats

- ✅ 12-hour format (AM/PM): `21/04/2025, 11:25 am - User: Message`
- ✅ 24-hour format: `21/04/2025, 11:25 - User: Message`
- ✅ Multiple languages and emojis
- ✅ Group chats and individual chats

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Text Processing**: WordCloud, Emoji
- **Deployment**: Heroku, Streamlit Cloud, Railway

## 📁 Project Structure

```
whatsapp-chat-analysis/
├── app.py                 # Main Streamlit application
├── helper.py             # Analysis helper functions
├── preprocessor.py       # Data preprocessing
├── requirements.txt      # Dependencies
├── runtime.txt          # Python version
├── Procfile             # Heroku configuration
├── setup.sh            # Deployment setup
├── .streamlit/
│   └── config.toml     # Streamlit config
├── stop_hinglish.txt   # Stop words
└── README.md           # Documentation
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- Matplotlib and Seaborn for visualization
- All contributors and users

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/whatsapp-chat-analysis/issues) page
2. Create a new issue with detailed description
3. Contact: your-email@example.com

---

⭐ **Star this repository if you found it helpful!**
