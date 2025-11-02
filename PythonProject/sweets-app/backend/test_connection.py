"""
Test MongoDB connection without starting the full server.
This helps debug connection issues.
"""
import os
import sys
from urllib.parse import quote_plus

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_connection():
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        from app.config import settings
        
        print("🔍 Testing MongoDB connection...")
        print(f"📝 Connection String: {settings.MONGO_URL.replace(settings.MONGO_URL.split('@')[0].split('://')[1] if '@' in settings.MONGO_URL else '', '***USERNAME***:***PASSWORD***').replace('***USERNAME***:***PASSWORD***', '***USERNAME***:***PASSWORD***')}")
        print(f"📦 Database Name: {settings.MONGO_DB_NAME}")
        print()
        
        async def test():
            try:
                client = AsyncIOMotorClient(settings.MONGO_URL)
                # Test connection
                await client.admin.command('ping')
                print("✅ Connection successful!")
                print(f"✅ Connected to database: {settings.MONGO_DB_NAME}")
                return True
            except Exception as e:
                error_msg = str(e)
                print(f"❌ Connection failed!")
                print(f"❌ Error: {error_msg}")
                
                # Provide helpful suggestions
                if "authentication failed" in error_msg.lower() or "bad auth" in error_msg.lower():
                    print()
                    print("💡 Authentication Error Suggestions:")
                    print("   1. Check your username and password are correct")
                    print("   2. If password has special characters, make sure they're URL-encoded:")
                    print("      - @ becomes %40")
                    print("      - # becomes %23")
                    print("      - $ becomes %24")
                    print("      - % becomes %25")
                    print("   3. Verify the database user exists in MongoDB Atlas")
                    print("   4. Check Database Access settings in Atlas")
                
                if "timeout" in error_msg.lower() or "could not connect" in error_msg.lower():
                    print()
                    print("💡 Connection Error Suggestions:")
                    print("   1. Check your IP address is whitelisted in Network Access")
                    print("   2. Verify your internet connection")
                    print("   3. Check if MongoDB Atlas is accessible")
                
                return False
        
        import asyncio
        result = asyncio.run(test())
        return result
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're in the backend directory and dependencies are installed:")
        print("   pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_connection()

