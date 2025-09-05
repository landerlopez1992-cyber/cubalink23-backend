#!/usr/bin/env python3
"""
🚀 CubaLink23 Backend - ENTRY POINT
Este archivo importa y ejecuta backend_final.py para compatibilidad con Render.com
"""

import os

# Importar y ejecutar backend_final
from backend_final import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)), debug=False, threaded=True)
# Deploy timestamp: Thu Sep  4 20:31:55 EDT 2025
