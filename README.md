<div dir="ltr">

# 🛡️ WitGuard – Python Code Analysis & Versioning System

Welcome to **ViewGuard**, a powerful CLI-based version control and code analysis system written in Python. This project combines a simplified Git-like CLI client with a FastAPI backend server to ensure high code quality during every push – simulating an internal CI tool focused on clean, maintainable code.

---

## 📦 Project Overview

The project is divided into two main components:

### 1️⃣ **Client – `wit`: A Mini Version Control System**
A command-line tool that mimics Git behavior and supports essential operations such as:
- `wit init` – Initialize a `.wit` folder for tracking
- `wit add <file>` – Stage files for the next commit
- `wit commit -m "message"` – Create a snapshot with a message
- `wit log` – Display commit history
- `wit status` – Show current changes
- `wit checkout <commit_id>` – Restore previous commit


## 🛠️ Technologies

- **Python**
- **Click library** for building a CLI
- **Object-Oriented Programming (OOP)** principles

---

### 2️⃣ **Backend – Code Analysis Server (`FastAPI`)**

A Python backend that analyzes pushed code in real-time through the `wit push` command and returns:
- Code quality alerts 🧠
- Visual reports 📊

> Built with:
- `FastAPI` – for the RESTful API
- `ast` – for Python code parsing
- `matplotlib` – for data visualization

---

## 🎯 Main Features

### ✅ Code Quality Checks (via AST)
The backend automatically scans uploaded `.py` files and checks for:
- 🚫 **Function too long** – More than 20 lines
- 🚫 **File too long** – More than 200 lines
- 🚫 **Unused variables**
- 🚫 **Missing docstrings**

### 📊 Graph Reports (PNG)
After each analysis, the backend generates:
- Histogram – Distribution of function lengths
- Pie Chart – Iss
- Bar Chart – Issues per file
- 🔁 Bonus: Line chart showing issue history over time

<br><br>
## 🌐 API Endpoints

| Endpoint     | Method | Description                          |
|--------------|--------|--------------------------------------|
| `/analyze`   | POST   | Accepts `.py` files and returns graphs |
| `/alerts`    | POST   | Accepts `.py` files and returns issue warnings |




<br><br>
## 🚀 How to Run the Project

### 1. Install Requirements

Make sure you have Python 3.8+ installed.  
Then, install the required dependencies for both the backend and client:

```bash
pip install -r requirements.txt
```

---

### 2. Run the Backend Server

Navigate to the `backend` directory and run the FastAPI server using Uvicorn:

```bash
cd backend
uvicorn main:app --reload
```

This will start the server on `http://127.0.0.1:8000` by default.

---

### 3. Run the Client (WIT System)

Navigate to the `client` folder and run the WIT CLI tool:

```bash
cd client
python wit.py <command> [options]
```

#### Example Workflow:

```bash
python wit init
python wit add example.py
python wit commit -m "Initial commit"
python wit push
```

The `push` command will automatically send files to the backend for analysis and receive back:

- Visual graphs (saved as PNGs)
- Issue alerts (e.g., unused variables, missing docstrings, long functions)

<br><br>
## 📁 Project Folder Structure

```text
ViewGuard/
├── backend/                  # FastAPI backend server
│   ├── main.py               # Entry point of the server
│   ├── analysis_utils.py           # Code analysis logic
│   └── ...
├── client/                   # WIT CLI tool
│   ├── wit.py
|   ├── abstractWit.py
|   ├── basicFunctions.py
|   ├── commandLine.py
|   ├── Exceptions.py
|   ├── repositoryData.json
|   ├── wit.bat 
│   └── ...
├── README.md
└── requirements.txt
```

---

## 🌟 Bonus Feature (Optional)

The server will also warn about variables that contain non-English (e.g., Hebrew) characters in their names. This helps ensure consistent, clean code across teams.

