# 🎥 YouTube → Insightful Article & PDF Generator

Convert any YouTube video into a well-structured article and downloadable PDF using AI.

---

## 🚀 Project Description

This project extracts content from YouTube videos and transforms it into:

* 📄 Insightful, structured articles
* 🧠 AI-generated summaries
* 📑 Downloadable PDF documents

It helps users **save time** by converting long videos into easy-to-read knowledge.

---

## ✨ Key Features

* 🔗 Paste any YouTube video URL
* 📜 Extract video transcript automatically
* 🧠 Generate structured article using LLM
* 📄 Convert article into PDF
* ⚡ Simple UI using Streamlit

---

## 🧠 How It Works

1. 🎥 Input YouTube URL
2. 📥 Fetch transcript using YouTube loader
3. 🤖 Process content using LLM (LangChain / Gemini / Bedrock)
4. 📝 Generate article
5. 📄 Convert article to PDF

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **AI Framework:** LangChain
* **LLM:** Google Gemini / AWS Bedrock
* **Data Source:** YouTube Transcript API
* **PDF Generation:** ReportLab / FPDF

---

## 📂 Project Structure

```
Youtube-to-Article-pdf/
│
├── app.py                 # Main Streamlit application
├── utils/
│   ├── loader.py         # Load YouTube transcript
│   ├── summarizer.py      # Generate article using LLM
│   ├── pdf.py            # Convert article to PDF
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

```bash
git clone https://github.com/gdimpulchandrika-rgb/Youtube-to-Article-pdf.git
cd Youtube-to-Article-pdf

python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---


---

## Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_api_key
# OR
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
```

---

## Use Cases

*  Students → Convert lectures to notes
*  Professionals → Extract insights from talks
* Researchers → Summarize educational content
* Content creators → Repurpose video content

---

## Future Improvements

* Multi-language support
* Speech-to-text for videos without subtitles
* SEO optimized articles
* Cloud deployment (AWS / GCP)
* Chrome extension

---


