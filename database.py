"""
Módulo de base de datos simple para el backend
"""

import sqlite3
import json
from datetime import datetime

def get_db_connection():
    """Obtener conexión a la base de datos SQLite"""
    conn = sqlite3.connect('charter_flights.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Inicializar la base de datos con las tablas necesarias"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tabla de aerolíneas charter
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS charter_airlines (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            markup REAL DEFAULT 0,
            active BOOLEAN DEFAULT 1,
            routes TEXT,
            check_frequency INTEGER DEFAULT 30,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de reservas charter
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS charter_bookings (
            id TEXT PRIMARY KEY,
            flight_data TEXT NOT NULL,
            passenger_info TEXT NOT NULL,
            payment_info TEXT NOT NULL,
            status TEXT DEFAULT 'PENDIENTE',
            total_amount REAL NOT NULL,
            markup_amount REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            confirmed_at TIMESTAMP,
            ticket_number TEXT
        )
    ''')
    
    # Tabla de logs de scraping
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scraping_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            airline_id TEXT NOT NULL,
            search_data TEXT NOT NULL,
            results_count INTEGER DEFAULT 0,
            success BOOLEAN DEFAULT 1,
            error_message TEXT,
            execution_time REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def save_charter_airline(airline_data):
    """Guardar o actualizar aerolínea charter"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR REPLACE INTO charter_airlines 
        (id, name, url, markup, active, routes, check_frequency, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        airline_data['id'],
        airline_data['name'],
        airline_data['url'],
        airline_data['markup'],
        airline_data['active'],
        json.dumps(airline_data.get('routes', [])),
        airline_data.get('check_frequency', 30),
        datetime.now()
    ))
    
    conn.commit()
    conn.close()

def get_charter_airlines():
    """Obtener todas las aerolíneas charter"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM charter_airlines')
    airlines = cursor.fetchall()
    
    conn.close()
    
    result = []
    for airline in airlines:
        result.append({
            'id': airline['id'],
            'name': airline['name'],
            'url': airline['url'],
            'markup': airline['markup'],
            'active': bool(airline['active']),
            'routes': json.loads(airline['routes']) if airline['routes'] else [],
            'check_frequency': airline['check_frequency']
        })
    
    return result

def save_charter_booking(booking_data):
    """Guardar reserva charter"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO charter_bookings 
        (id, flight_data, passenger_info, payment_info, total_amount, markup_amount)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        booking_data['id'],
        json.dumps(booking_data['flight_data']),
        json.dumps(booking_data['passenger_info']),
        json.dumps(booking_data['payment_info']),
        booking_data['total_amount'],
        booking_data.get('markup_amount', 0)
    ))
    
    conn.commit()
    conn.close()

def get_charter_booking(booking_id):
    """Obtener reserva charter por ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM charter_bookings WHERE id = ?', (booking_id,))
    booking = cursor.fetchone()
    
    conn.close()
    
    if booking:
        return {
            'id': booking['id'],
            'flight_data': json.loads(booking['flight_data']),
            'passenger_info': json.loads(booking['passenger_info']),
            'payment_info': json.loads(booking['payment_info']),
            'status': booking['status'],
            'total_amount': booking['total_amount'],
            'markup_amount': booking['markup_amount'],
            'created_at': booking['created_at'],
            'updated_at': booking['updated_at'],
            'confirmed_at': booking['confirmed_at'],
            'ticket_number': booking['ticket_number']
        }
    
    return None

def update_charter_booking_status(booking_id, status, ticket_number=None):
    """Actualizar estado de reserva charter"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if status == 'CONFIRMADO':
        cursor.execute('''
            UPDATE charter_bookings 
            SET status = ?, confirmed_at = ?, ticket_number = ?, updated_at = ?
            WHERE id = ?
        ''', (status, datetime.now(), ticket_number, datetime.now(), booking_id))
    else:
        cursor.execute('''
            UPDATE charter_bookings 
            SET status = ?, updated_at = ?
            WHERE id = ?
        ''', (status, datetime.now(), booking_id))
    
    conn.commit()
    conn.close()

def get_user_charter_bookings(user_id=None, limit=50):
    """Obtener reservas charter de un usuario (simulado)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM charter_bookings 
        ORDER BY created_at DESC 
        LIMIT ?
    ''', (limit,))
    
    bookings = cursor.fetchall()
    conn.close()
    
    result = []
    for booking in bookings:
        result.append({
            'id': booking['id'],
            'flight_data': json.loads(booking['flight_data']),
            'passenger_info': json.loads(booking['passenger_info']),
            'status': booking['status'],
            'total_amount': booking['total_amount'],
            'created_at': booking['created_at'],
            'confirmed_at': booking['confirmed_at'],
            'ticket_number': booking['ticket_number']
        })
    
    return result

def log_scraping_result(airline_id, search_data, results_count, success=True, error_message=None, execution_time=None):
    """Registrar resultado de scraping"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO scraping_logs 
        (airline_id, search_data, results_count, success, error_message, execution_time)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        airline_id,
        json.dumps(search_data),
        results_count,
        success,
        error_message,
        execution_time
    ))
    
    conn.commit()
    conn.close()

# Inicializar base de datos al importar el módulo
init_database()
