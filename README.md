# Cubalink23 Backend - Charter Airlines API

## 🚀 Despliegue en Render.com

### 📋 Requisitos Previos
- Cuenta en [Render.com](https://render.com)
- Cuenta en [GitHub](https://github.com)
- Token de Duffel API (opcional)

### 🔧 Pasos para Desplegar

#### 1. Subir a GitHub
```bash
git init
git add .
git commit -m "Initial commit - Charter Airlines Backend"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

#### 2. Crear Servicio en Render.com
1. Ir a [Render.com](https://render.com)
2. Click en "New +" → "Web Service"
3. Conectar con GitHub
4. Seleccionar el repositorio
5. Configurar:
   - **Name**: `cubalink23-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`

#### 3. Configurar Variables de Entorno
En Render.com → Environment Variables:
```
DUFFEL_API_TOKEN=tu_token_aqui
FLASK_ENV=production
SECRET_KEY=cubalink23-secret-key-2023
```

#### 4. Desplegar
Click en "Create Web Service"

### 🌐 URLs de la API

Una vez desplegado, tu API estará disponible en:
```
https://tu-app.onrender.com
```

#### Endpoints Principales:
- `GET /` - Estado del servidor
- `POST /api/charter/search` - Búsqueda de vuelos charter
- `GET /api/charter/airlines` - Lista de aerolíneas charter
- `POST /api/charter/booking` - Crear reserva charter

### 🔍 Pruebas

#### Probar Búsqueda de Charter:
```bash
curl -X POST https://tu-app.onrender.com/api/charter/search \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "Miami",
    "destination": "Havana", 
    "departure_date": "2025-09-06",
    "passengers": 2
  }'
```

### 📊 Aerolíneas Charter Soportadas

1. **Xael Charter** - https://www.xaelcharter.com
2. **Cubazul Air Charter** - https://cubazulaircharter.com
3. **Havana Air Charter** - https://havanaair.com

### 🛠️ Tecnologías

- **Backend**: Flask (Python)
- **Web Scraping**: Selenium + BeautifulSoup
- **Base de Datos**: SQLite
- **Despliegue**: Render.com
- **API**: RESTful

### 🔧 Desarrollo Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar localmente
python3 app.py

# El servidor estará en http://localhost:3005
```

### 📝 Notas Importantes

- El web scraping funciona con datos reales + fallback
- Las reservas se guardan en SQLite
- El sistema incluye markup configurable
- CORS está habilitado para Flutter
