# backend_final.py - Entry point para Render.com
import os
from app import app

# Importa la aplicación principal para que gunicorn pueda encontrarla
# Render.com usa: gunicorn backend_final:app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)