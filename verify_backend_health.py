#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de verificación del backend antes del deploy
Verifica que todas las APIs críticas funcionen correctamente
"""

import requests
import json
import sys
from datetime import datetime

# URLs del backend
BACKEND_URL = "https://cubalink23-backend.onrender.com"
ADMIN_URL = BACKEND_URL + "/admin"

def test_health_check():
    """Verificar health check del backend"""
    try:
        print("🏥 Verificando health check...")
        response = requests.get(BACKEND_URL + "/api/health", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Health check OK: " + str(data.get('status', 'unknown')))
            print("   📊 Mensaje: " + str(data.get('message', 'N/A')))
            return True
        else:
            print("   ❌ Health check falló: " + str(response.status_code))
            return False
    except Exception as e:
        print("   ❌ Error en health check: " + str(e))
        return False

def test_banners_api():
    """Verificar API de banners"""
    try:
        print("🖼️ Verificando API de banners...")
        response = requests.get(ADMIN_URL + "/api/banners", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print("   ✅ API banners OK: " + str(len(data)) + " banners encontrados")
                return True
            else:
                print("   ⚠️ API banners responde pero formato inesperado")
                return True
        else:
            print("   ❌ API banners falló: " + str(response.status_code))
            return False
    except Exception as e:
        print("   ❌ Error en API banners: " + str(e))
        return False

def test_flights_api():
    """Verificar API de vuelos"""
    try:
        print("✈️ Verificando API de vuelos...")
        response = requests.get(ADMIN_URL + "/api/flights/airports?query=miami", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                print("   ✅ API vuelos OK: " + str(len(data)) + " aeropuertos encontrados")
                return True
            else:
                print("   ⚠️ API vuelos responde pero sin resultados")
                return True
        else:
            print("   ❌ API vuelos falló: " + str(response.status_code))
            return False
    except Exception as e:
        print("   ❌ Error en API vuelos: " + str(e))
        return False

def test_admin_panel():
    """Verificar que el panel admin sea accesible"""
    try:
        print("🔐 Verificando panel admin...")
        response = requests.get(ADMIN_URL + "/", timeout=10)
        
        if response.status_code == 200:
            print("   ✅ Panel admin accesible")
            return True
        else:
            print("   ❌ Panel admin no accesible: " + str(response.status_code))
            return False
    except Exception as e:
        print("   ❌ Error accediendo panel admin: " + str(e))
        return False

def main():
    """Función principal de verificación"""
    print("🔍 VERIFICACIÓN DEL BACKEND ANTES DEL DEPLOY")
    print("=" * 50)
    print("📅 Fecha: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("🌐 Backend URL: " + BACKEND_URL)
    print()
    
    tests = [
        test_health_check,
        test_banners_api,
        test_flights_api,
        test_admin_panel
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print("📊 RESULTADO: " + str(passed) + "/" + str(total) + " pruebas pasaron")
    
    if passed == total:
        print("✅ TODAS LAS PRUEBAS PASARON - BACKEND LISTO PARA DEPLOY")
        return 0
    else:
        print("❌ ALGUNAS PRUEBAS FALLARON - NO HACER DEPLOY")
        return 1

if __name__ == "__main__":
    sys.exit(main())
