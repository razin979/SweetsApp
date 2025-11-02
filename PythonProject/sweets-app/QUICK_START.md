# 🚀 Quick Start Guide

## Step 1: Start the Backend Server

**Open a terminal/PowerShell window and run:**

```powershell
cd sweets-app\backend
python run.py
```

**You should see:**
```
🚀 Starting FastAPI server...
📡 Server will be available at http://127.0.0.1:8000
📚 API docs available at http://127.0.0.1:8000/docs
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**✅ Keep this terminal window open!**

---

## Step 2: Start the Frontend

**Open a NEW terminal/PowerShell window and run:**

```powershell
cd sweets-app\frontend
streamlit run app.py
```

**You should see:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

---

## Step 3: Use the Application

1. Open your browser to the Streamlit URL (usually `http://localhost:8501`)
2. You should see the Sweets App interface
3. Register a new user or login

---

## 🔧 Troubleshooting

### Backend won't start?

1. **Check if port 8000 is already in use:**
   ```powershell
   netstat -ano | findstr :8000
   ```
   If something is using it, either stop that process or change the port in `run.py`

2. **Check if you have all dependencies:**
   ```powershell
   cd sweets-app\backend
   pip install -r requirements.txt
   ```

3. **Check your `.env` file exists** in `sweets-app\backend\` with:
   ```
   MONGO_URL=your_mongodb_connection_string
   MONGO_DB_NAME=sweets_db
   SECRET_KEY=your-secret-key
   ```

### Frontend can't connect?

- Make sure the backend is running first (Step 1)
- Check the backend is on `http://127.0.0.1:8000`
- Verify the `BASE_URL` in `frontend/app.py` matches your backend URL

### Still having issues?

1. Test the backend API directly: Open `http://127.0.0.1:8000/docs` in your browser
2. If the docs page loads, the backend is working
3. If not, check the backend terminal for error messages

---

## 📝 Notes

- **Backend runs on:** `http://127.0.0.1:8000`
- **Frontend runs on:** `http://localhost:8501` (or another port if 8501 is busy)
- **API Documentation:** `http://127.0.0.1:8000/docs`

