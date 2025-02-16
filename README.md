# **QuizStation 🎓**  
A **Streamlit-based** application that generates quizzes from topics, documents, and CSV files using AI.  

## **🚀 Features**  
- 📚 **Topic-based Quiz Generation** – Enter a topic and generate quiz questions automatically.  
- 📄 **Document-based Quiz Generation** – Upload PDFs or text files, extract content, and generate quizzes.  
- 📊 **CSV-based Quiz Upload** – Upload pre-made Q&A CSVs and start quizzes instantly.  
- ✅ **User-friendly Interface** – Built using **Streamlit**, with an intuitive UI for seamless quiz creation.  

---

## **🛠️ Technologies Used**  
- **Streamlit** – Interactive web application framework  
- **PyMuPDF (fitz)** – PDF text extraction  
- **Pandas** – Data manipulation  
- **Python** – Core logic and quiz processing    

---

## **📂 Project Structure**  
```
QuizStation/
│── app.py              # Main Streamlit app
│── requirements.txt     # Dependencies
│── utils/
│   ├── topic_page.py    # Topic-based quiz logic
│   ├── document_page.py # Document-based quiz logic
│   ├── csv_page.py      # CSV-based quiz logic
│   ├── topic_to_quiz.py # Topic quiz generator function
│   ├── doc_to_quiz.py   # Document quiz generator function
│   ├── csv_to_quiz.py   # CSV loader function
└── static/              # (If required) Static files directory
```

---

## **💡 How to Use**  
1. **Clone the repository:**  
   ```bash
   git clone https://github.com/arpitpatelsitapur/QUIZSTATION.git
   cd QUIZSTATION
   ```
2. **Install dependencies:**  
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Streamlit app:**  
   ```bash
   streamlit run app.py
   ```
4. **Use the app:**  
   - Navigate to **"Generate Quiz by Topic"** to create a quiz from a topic.  
   - Upload a **PDF or TXT file** in **"Generate Quiz from Document"**.  
   - Upload a **CSV file** in **"Upload Q&A CSV"** to load pre-made quizzes.  

---

## **📌 CSV Format Example**  
Ensure your CSV follows this format:  
```csv
question, option1, option2, option3, option4, correct_answer
"What is AI?", "Artificial Intelligence", "Artificial Information", "Automatic Interface", "None", "Artificial Intelligence"
```

---

## **🐞 Troubleshooting**  
- **Static Directory Error:** Run `mkdir static` if you encounter missing directory issues.  
- **PyMuPDF Error:** Reinstall with `pip install pymupdf`.  
- **Other Issues:** Run `streamlit run app.py --server.headless true` and check logs.  

---
  
