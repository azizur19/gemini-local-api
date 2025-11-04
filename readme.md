
# Gemini Local API

This repository demonstrates how to create a **free local API** to access **Google Gemini** using:
- Django
- Django REST Framework
- Selenium (Chrome Driver)

It allows you to use Gemini like a normal API without paying for cloud usage.

---

## ✅ Features
- Local GUI chat window with Gemini
- API endpoint to get Gemini responses from any external program
- Easy to setup and run locally

---

## 🚀 How to Run

Make sure you have Python installed.

### 1️⃣ Clone this repository
```sh
git clone https://github.com/azizur19/gemini-local-api.git
cd gemini-local-api
```

### 2️⃣ Create Virtual Environment (recommended)
```sh
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Download Chrome Driver
Download compatible Chrome Driver from  
https://googlechromelabs.github.io/chrome-for-testing/  

Place it here and update the path in code:
```
C:\Chrome_Driver\chromedriver.exe
```

Used format:
```python
webdriver.Chrome(service=Service(r"C:\Chrome_Driver\chromedriver.exe"), options=options)
```

### 5️⃣ Run Server
```sh
python localapi/manage.py runserver
```

---

## 🌍 Available Links

| Purpose | URL |
|--------|-----|
| Beautiful GUI with Gemini chatbot | http://127.0.0.1:8000/api/local |
| API usage example | http://127.0.0.1:8000/api/local?prompt=what is the date of next friday |

Example usage from Python:
```python
import requests
res = requests.get("http://127.0.0.1:8000/api/local?prompt=hello")
print(res.json()["result"]["response"]["response"])
```

---

## 💬 Chat Window Preview

![Chat Window Screenshot](https://github.com/user-attachments/assets/42473bf3-85b5-4992-b51c-177a14ca7698)

---

## ⚠️ Notes
- Keep Chrome updated to match your Chrome Driver
- Local API works only when your browser is visible or running with automation

---

## 📌 Author

Created by [**ar_titumir**](https://github.com/azizur19)  
If this tool helps your productivity, please give a ⭐ on GitHub. 
https://github.com/azizur19 

---

Enjoy using Gemini for free locally. Contribute and make it even better!
