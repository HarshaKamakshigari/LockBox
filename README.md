
# 🔐LockBox AES File Encryption Web App

A simple and secure AES file encryption and decryption web app built using **FastAPI** for the backend and **HTML** for the frontend. It allows users to encrypt and decrypt files using AES encryption directly in their browser.

---

## ✨ Features

- AES file encryption with secure key generation
- Decryption with user-provided AES keys
- HTML frontend for easy interaction
- FastAPI-powered backend
- Dockerized for containerized deployment
- Basic CI pipeline with GitHub Actions

---

## 🛠 Tech Stack

- **Backend:** FastAPI (Python)
- **Frontend:** HTML5 
- **Encryption:** AES (via PyCryptodome)
- **Containerization:** Docker
- **CI/CD:** GitHub Actions

---



---

## 🚀 Getting Started

### 🔧 Local Setup (without Docker)

1. **Clone the repository**

```bash
git clone https://github.com/HarshaKamakshigari/LockBox
cd aes-file-encryption-app
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Run the app**

```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000` in your browser.

---

### 🐳 Running with Docker

1. **Build the Docker image**

```bash
docker build -t aes-encryption-app .
```

2. **Run the container**

```bash
docker run -d -p 8000:8000 aes-encryption-app
```

Visit `http://localhost:8000` in your browser.

---

## 🧪 CI/CD - GitHub Actions

Basic GitHub Actions pipeline is set up to:

- ✅ Lint the code and ensure formatting
- ✅ Run a dummy test check (no unit tests included yet)

> The workflow is defined in `.github/workflows/ci.yml`

You can extend this to add real unit tests and deployment steps later!

---

## 📦 Dependencies

```
fastapi
uvicorn
python-multipart
pycryptodome
```

---

## 🧠 How It Works

### 🔐 Encryption Flow:

1. User uploads a file.
2. A random AES key is picked.
3. The file is encrypted using AES.
4. The encrypted file is downloaded and the key is displayed (user must save it!).

### 🔓 Decryption Flow:

1. User uploads the encrypted file and enters their AES key.
2. File is decrypted on the server and returned for download.

> ⚠️ Keep your AES key safe. Without it, decryption will fail.

---


## 📜 License

MIT License

---

Made with by [Harsha Kamakshigari]([https://github.com/HarshaKamakshigari])
