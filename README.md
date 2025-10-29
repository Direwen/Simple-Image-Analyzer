# 🖼️ Image Analyzer API

A **FastAPI** application that analyzes images, identifies the brightest and darkest points, calculates average brightness, and stores analysis results in a database.

## ✨ Features

* Upload and analyze JPEG/PNG images
* Calculate average brightness, brightest and darkest points
* Process images with visual highlights of brightest (🔴 red) and darkest (🔵 blue) points
* Store analysis results in a PostgreSQL database
* Download processed images

## 🧠 Tech Stack

* **FastAPI** — Web framework for building APIs
* **SQLAlchemy** — ORM for database operations
* **OpenCV (cv2)** — Image processing library
* **NumPy** — Numerical computing library
* **Python-dotenv** — Environment variable management
* **PostgreSQL** — Relational database (via psycopg2)
* **uv** — Modern, fast Python package manager

## ⚙️ Prerequisites

* Python 3.12 or higher
* PostgreSQL database

---

## 🧩 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Direwen/Simple-Image-Analyzer.git
cd Simple-Image-Analyzer
```

### 2. Set up the environment

```bash
uv sync
```

This installs all dependencies according to the `pyproject.toml` and `uv.lock` files.

> 💡 `uv` automatically creates and manages a virtual environment in `.venv`.

### 3. Create the `.env` file

In the project root, create a `.env` file with your database connection string:

```
DATABASE_URL=postgresql://username:password@localhost/database_name
```

Replace `username`, `password`, and `database_name` with your actual PostgreSQL credentials.

---

## 🚀 Running the Application

### Start the FastAPI development server

```bash
uv run fastapi dev main.py
```

or, equivalently:

```bash
uv run uvicorn main:app --reload
```

By default, the API runs at:
➡️ **[http://localhost:8000](http://localhost:8000)**

### View API Docs

* **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## ⚙️ Managing Dependencies

Add a new package:

```bash
uv add package-name
```

Remove a package:

```bash
uv remove package-name
```

Update all packages to the latest compatible versions:

```bash
uv lock --upgrade
uv sync
```

> All dependencies are stored in `pyproject.toml` and locked in `uv.lock`.

---

## 🧹 Code Formatting

Use Ruff for formatting and linting:

```bash
uv run ruff format .
uv run ruff check .
```