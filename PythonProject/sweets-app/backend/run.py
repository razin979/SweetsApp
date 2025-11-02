"""
Run script for the FastAPI application.
This ensures the app can be run from the backend directory.
"""
import sys
import os

# Ensure we're in the right directory
backend_dir = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(backend_dir) == "backend":
    os.chdir(backend_dir)
    sys.path.insert(0, backend_dir)

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting FastAPI server...")
    print("📡 Server will be available at http://127.0.0.1:8000")
    print("📚 API docs available at http://127.0.0.1:8000/docs")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

