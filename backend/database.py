from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv

# ======================================
# LOAD ENV VARIABLES
# ======================================

load_dotenv()

# MongoDB URL (fallback if .env not used)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")


# ======================================
# CONNECT TO MONGODB
# ======================================

try:
    client = MongoClient(MONGO_URI)

    # verify connection
    client.admin.command("ping")
    print("✅ MongoDB Connected Successfully")

except ConnectionFailure as e:
    print("❌ MongoDB Connection Failed:", e)
    raise SystemExit("Database connection error")


# ======================================
# DATABASE
# ======================================

db = client["glow_guardians"]


# ======================================
# COLLECTIONS
# ======================================

# User authentication
users_collection = db["users"]

# Future AI Analysis storage
skin_analysis_collection = db["skin_analysis"]
hair_analysis_collection = db["hair_analysis"]
face_analysis_collection = db["face_analysis"]


# ======================================
# HELPER FUNCTION (OPTIONAL)
# ======================================

def get_database():
    """Return database instance"""
    return db
