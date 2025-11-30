# Zoff Scope Application - Local Development Guide

This guide explains how to run the Zoff Scope application locally. The project consists of a FastAPI backend and two Next.js frontend applications (Store and Customer).

## Prerequisites

- **Node.js**: v20 or higher
- **Python**: 3.9 or higher

## Project Structure

- `apps/store`: Store-facing application (Next.js)
- `apps/customer`: Customer-facing application (Next.js)
- `backend`: API Server (FastAPI)

---

## 1. Backend Setup

The backend uses FastAPI and defaults to a local SQLite database for development, so no external database setup is required initially.

1. Open a terminal and navigate to the `backend` directory:
   ```bash
   cd backend
   ```

2. Create a Python virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - **Windows (PowerShell)**:
     ```powershell
     .\venv\Scripts\Activate
     ```
   - **Mac/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`.
   API Documentation (Swagger UI) is available at `http://127.0.0.1:8000/docs`.

---

## 2. Frontend Setup

You can run the Store app and Customer app independently.

### Store App

1. Open a new terminal and navigate to the `apps/store` directory:
   ```bash
   cd apps/store
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:3000`.

### Customer App

1. Open a new terminal and navigate to the `apps/customer` directory:
   ```bash
   cd apps/customer
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:3001` (Next.js automatically uses the next available port if 3000 is busy).
