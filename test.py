import os

db_path = "./stratego.db"
if os.path.exists(db_path):
    print("✅ הקובץ stratego.db קיים")
else:
    print("❌ הקובץ stratego.db לא נמצא")
