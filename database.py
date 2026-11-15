
import sqlite3
import json
from datetime import datetime

DB_NAME = "brandlens.db"


# ==========================================
# 1. DATABASE INITIALIZATION
# ==========================================

def initialize_database():

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # Review history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_content TEXT NOT NULL,
            issues TEXT,
            corrected_content TEXT,
            review_date TEXT
        )
    """)

    # Multiple brand profiles table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS brands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand_name TEXT NOT NULL UNIQUE,
            brand_tone TEXT,
            approved_words TEXT,
            prohibited_words TEXT,
            brand_rules TEXT,
            created_at TEXT
        )
    """)

    connection.commit()
    connection.close()


# ==========================================
# 2. SAVE REVIEW
# ==========================================

def save_review(original_content, issues, corrected_content):

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    review_date = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO reviews (
            original_content,
            issues,
            corrected_content,
            review_date
        )
        VALUES (?, ?, ?, ?)
    """, (
        original_content,
        json.dumps(issues),
        corrected_content,
        review_date
    ))

    connection.commit()
    connection.close()


# ==========================================
# 3. GET ALL REVIEWS
# ==========================================

def get_all_reviews():

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM reviews
        ORDER BY id DESC
    """)

    reviews = cursor.fetchall()

    connection.close()

    return reviews


# ==========================================
# 4. GET REVIEW COUNT
# ==========================================

def get_review_count():

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM reviews"
    )

    count = cursor.fetchone()[0]

    connection.close()

    return count


# ==========================================
# 5. SAVE BRAND PROFILE
# ==========================================

def save_brand(
    brand_name,
    brand_tone,
    approved_words,
    prohibited_words,
    brand_rules
):

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    created_at = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    try:

        cursor.execute("""
            INSERT INTO brands (
                brand_name,
                brand_tone,
                approved_words,
                prohibited_words,
                brand_rules,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            brand_name,
            brand_tone,
            json.dumps(approved_words),
            json.dumps(prohibited_words),
            brand_rules,
            created_at
        ))

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()


# ==========================================
# 6. GET ALL BRANDS
# ==========================================

def get_all_brands():

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM brands
        ORDER BY id DESC
    """)

    brands = cursor.fetchall()

    connection.close()

    return brands


# ==========================================
# 7. GET ONE BRAND
# ==========================================

def get_brand_by_name(brand_name):

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM brands
        WHERE brand_name = ?
    """, (brand_name,))

    brand = cursor.fetchone()

    connection.close()

    return brand


# ==========================================
# INITIALIZE DATABASE
# ==========================================

initialize_database()
