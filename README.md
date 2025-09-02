# 🚀 CubaLink23 Backend - API Duffel

Backend Flask para la app CubaLink23 que integra con la API real de Duffel para búsqueda de vuelos.

## ⚙️ Configuración

### Variables de Entorno Requeridas:

```bash
DUFFEL_API_KEY=tu_api_key_aqui
PORT=3005
```

### Para desarrollo local:
1. Crear archivo `.env` con las variables arriba
2. `pip3 install -r requirements.txt`
3. `python3 app.py`

### Para Render.com:
1. Configurar `DUFFEL_API_KEY` en variables de entorno de Render
2. El `PORT` se configura automáticamente

## 🎯 Funcionalidades

- ✅ **Búsqueda de aeropuertos** - `/api/airports/search`
- ✅ **Búsqueda de vuelos** - `/api/flights/search`
- ✅ **Vuelos comerciales** (Duffel API)
- ✅ **Vuelos charter** (API local)
- ✅ **Logos de aerolíneas** (conversión SVG→PNG)
- ✅ **CORS configurado** para Flutter

## 🔗 Endpoints

### Buscar Aeropuertos
```
GET /api/airports/search?query=MIA
```

### Buscar Vuelos
```
POST /api/flights/search
{
  "origin": "MIA",
  "destination": "HAV", 
  "departure_date": "2025-01-15",
  "passengers": 1,
  "airlineType": "comerciales"
}
```