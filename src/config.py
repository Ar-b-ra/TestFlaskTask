import os

DATABASE_DIR = "databases"

if not os.path.exists(DATABASE_DIR):
    os.makedirs(DATABASE_DIR)
