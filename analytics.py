import sqlite3
from datetime import datetime, date
import os

DATABASE_PATH = 'analytics.db'

def init_database():
    """Initialize the analytics database"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Table for tracking visits
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            ip_hash TEXT,
            user_agent TEXT,
            date DATE
        )
    ''')
    
    # Table for tracking generations
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS generations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            success BOOLEAN,
            include_text BOOLEAN,
            error_message TEXT,
            processing_time REAL,
            date DATE
        )
    ''')
    
    # Table for daily statistics (for quick queries)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_stats (
            date DATE PRIMARY KEY,
            unique_visitors INTEGER DEFAULT 0,
            total_visits INTEGER DEFAULT 0,
            generations_success INTEGER DEFAULT 0,
            generations_failed INTEGER DEFAULT 0,
            total_generations INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()

def track_visit(ip_address=None, user_agent=None):
    """Track a page visit"""
    import hashlib
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Hash IP for privacy
    ip_hash = hashlib.sha256(ip_address.encode()).hexdigest() if ip_address else 'unknown'
    today = date.today()
    
    # Record visit
    cursor.execute('''
        INSERT INTO visits (ip_hash, user_agent, date)
        VALUES (?, ?, ?)
    ''', (ip_hash, user_agent, today))
    
    # Update daily stats
    cursor.execute('''
        INSERT INTO daily_stats (date, total_visits, unique_visitors)
        VALUES (?, 1, 1)
        ON CONFLICT(date) DO UPDATE SET
            total_visits = total_visits + 1
    ''', (today,))
    
    # Check if this is a unique visitor today
    cursor.execute('''
        SELECT COUNT(DISTINCT ip_hash) 
        FROM visits 
        WHERE date = ?
    ''', (today,))
    unique_count = cursor.fetchone()[0]
    
    cursor.execute('''
        UPDATE daily_stats 
        SET unique_visitors = ?
        WHERE date = ?
    ''', (unique_count, today))
    
    conn.commit()
    conn.close()

def track_generation(success, include_text=False, error_message=None, processing_time=None):
    """Track an image generation attempt"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    today = date.today()
    
    # Record generation
    cursor.execute('''
        INSERT INTO generations (success, include_text, error_message, processing_time, date)
        VALUES (?, ?, ?, ?, ?)
    ''', (success, include_text, error_message, processing_time, today))
    
    # Update daily stats
    if success:
        cursor.execute('''
            INSERT INTO daily_stats (date, generations_success, total_generations)
            VALUES (?, 1, 1)
            ON CONFLICT(date) DO UPDATE SET
                generations_success = generations_success + 1,
                total_generations = total_generations + 1
        ''', (today,))
    else:
        cursor.execute('''
            INSERT INTO daily_stats (date, generations_failed, total_generations)
            VALUES (?, 1, 1)
            ON CONFLICT(date) DO UPDATE SET
                generations_failed = generations_failed + 1,
                total_generations = total_generations + 1
        ''', (today,))
    
    conn.commit()
    conn.close()

def get_analytics_summary():
    """Get summary analytics"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Total stats
    cursor.execute('SELECT COUNT(*) FROM visits')
    total_visits = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT ip_hash) FROM visits')
    total_unique_visitors = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM generations WHERE success = 1')
    successful_generations = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM generations WHERE success = 0')
    failed_generations = cursor.fetchone()[0]
    
    # Today's stats
    today = date.today()
    cursor.execute('SELECT * FROM daily_stats WHERE date = ?', (today,))
    today_stats = cursor.fetchone()
    
    if today_stats:
        today_data = {
            'unique_visitors': today_stats[1],
            'total_visits': today_stats[2],
            'successful_generations': today_stats[3],
            'failed_generations': today_stats[4],
            'total_generations': today_stats[5]
        }
    else:
        today_data = {
            'unique_visitors': 0,
            'total_visits': 0,
            'successful_generations': 0,
            'failed_generations': 0,
            'total_generations': 0
        }
    
    # Last 7 days
    cursor.execute('''
        SELECT date, unique_visitors, total_visits, generations_success, generations_failed
        FROM daily_stats
        ORDER BY date DESC
        LIMIT 7
    ''')
    last_7_days = cursor.fetchall()
    
    conn.close()
    
    return {
        'total': {
            'visits': total_visits,
            'unique_visitors': total_unique_visitors,
            'successful_generations': successful_generations,
            'failed_generations': failed_generations,
            'total_generations': successful_generations + failed_generations
        },
        'today': today_data,
        'last_7_days': [
            {
                'date': row[0],
                'unique_visitors': row[1],
                'total_visits': row[2],
                'successful_generations': row[3],
                'failed_generations': row[4]
            }
            for row in last_7_days
        ]
    }

# Initialize database on import
init_database()
