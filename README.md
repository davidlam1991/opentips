# 📝 Open Tips Forum Side Project

A Django-based forum where users can share and discuss tips in Canada, and interact through comments and replies.

## 🚀 Features

- 📝 Users can create, comment, edit, and delete posts  
- 💬 Nested commenting system with replies  
- 📌 Merge same address post automatically
- 🔍 Search and filter functionality  
- 📢 Report inappropriate comments and posts

## 📦 Tech Stack

- **Backend:** Django, Django REST Framework  
- **Frontend:** HTML, CSS, JavaScript  
- **Database:** PostgreSQL
- **Deployment:** Docker, Render  

## 🛠 Installation & Setup
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/davidlam1991/opentips
cd opentips
```
### 2️⃣ Set Up Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ Configure Environment Variables in .env.local
```angular2html
SECRET_KEY=
DEBUG=True
DJANGO_LOGLEVEL=info
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

# Database Settings
DATABASE_ENGINE=postgresql
DATABASE_NAME=railway
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=
DATABASE_HOST=autorack.proxy.rlwy.net
DATABASE_PORT=33292

# Google API Settings
GOOGLE_API_KEY=
RECAPTCHA_KEY=
RECAPTCHA_SECRET_KEY=

# Emailing settings
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST="smtp.gmail.com"
EMAIL_HOST_USER=""
EMAIL_HOST_PASSWORD=""
EMAIL_PORT=587
```
### 4️⃣ Edit docker-compose.yml 
```angular2html
   env_file:
     - .env.local
```

### 5️⃣ Run Migrations and Collect Static Files
```bash
python manage.py migrate
python manage.py collectstatic
```

### 6️⃣ Run the Server
```bash
python manage.py runserver
```
