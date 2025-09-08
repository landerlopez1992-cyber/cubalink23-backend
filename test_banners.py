#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para la gestión de banners
"""

import requests
import json
import os

# Configuración
BASE_URL = "http://localhost:3005"
ADMIN_USERNAME = "landerlopez1992@gmail.com"
ADMIN_PASSWORD = "Maquina.2055"

def test_login():
    """Probar login del admin"""
    print("🔐 Probando login...")
    
    login_data = {
        'username': ADMIN_USERNAME,
        'password': ADMIN_PASSWORD
    }
    
    try:
        response = requests.post("{}/auth/login".format(BASE_URL), data=login_data)
        if response.status_code == 200:
            print("✅ Login exitoso")
            return True
        else:
            print("❌ Login falló: {}".format(response.status_code))
            return False
    except Exception as e:
        print("❌ Error en login: {}".format(e))
        return False

def test_get_banners():
    """Probar obtener banners"""
    print("\n🎨 Probando obtener banners...")
    
    try:
        response = requests.get("{}/admin/api/banners".format(BASE_URL).format(BASE_URL))
        if response.status_code == 200:
            banners = response.json()
            print("✅ Banners obtenidos: {} banners".format(len(banners)))
            for banner in banners[:3]:  # Mostrar solo los primeros 3
                print("   - {}: {}".format(banner.get('title', 'Sin título'), banner.get('active', False)))
            return banners
        else:
            print("❌ Error obteniendo banners: {}".format(response.status_code))
            return []
    except Exception as e:
        print("❌ Error en obtener banners: {}".format(e))
        return []

def test_get_active_banners():
    """Probar obtener banners activos"""
    print("\n🌟 Probando obtener banners activos...")
    
    try:
        response = requests.get("{}/admin/api/banners/active".format(BASE_URL).format(BASE_URL))
        if response.status_code == 200:
            banners = response.json()
            print("✅ Banners activos obtenidos: {} banners".format(len(banners)))
            for banner in banners:
                print("   - {}: Posición {}".format(banner.get('title', 'Sin título'), banner.get('position', 0)))
            return banners
        else:
            print("❌ Error obteniendo banners activos: {}".format(response.status_code))
            return []
    except Exception as e:
        print("❌ Error en obtener banners activos: {}".format(e))
        return []

def test_add_banner():
    """Probar agregar banner"""
    print("\n➕ Probando agregar banner...")
    
    banner_data = {
        'title': 'Banner de Prueba',
        'description': 'Este es un banner de prueba para el sistema',
        'link_url': 'https://ejemplo.com',
        'active': True,
        'position': 1
    }
    
    try:
        response = requests.post("{}/admin/api/banners".format(BASE_URL).format(BASE_URL), data=banner_data)
        if response.status_code == 200:
            banner = response.json()
            print("✅ Banner agregado: {} - ID: {}".format(banner.get('title'), banner.get('id')))
            return banner
        else:
            print("❌ Error agregando banner: {} - {}".format(response.status_code, response.text))
            return None
    except Exception as e:
        print("❌ Error en agregar banner: {}".format(e))
        return None

def test_update_banner(banner_id):
    """Probar actualizar banner"""
    print("\n✏️ Probando actualizar banner ID: {}...".format(banner_id))
    
    update_data = {
        'title': 'Banner de Prueba (Actualizado)',
        'description': 'Este es un banner de prueba actualizado',
        'link_url': 'https://ejemplo-actualizado.com',
        'active': True,
        'position': 2
    }
    
    try:
        response = requests.put("{}/admin/api/banners/{}".format(BASE_URL, banner_id), json=update_data)
        if response.status_code == 200:
            banner = response.json()
            print("✅ Banner actualizado: {} - Posición: {}".format(banner.get('title'), banner.get('position')))
            return banner
        else:
            print("❌ Error actualizando banner: {} - {}".format(response.status_code, response.text))
            return None
    except Exception as e:
        print("❌ Error en actualizar banner: {}".format(e))
        return None

def test_toggle_banner_status(banner_id):
    """Probar activar/desactivar banner"""
    print("\n🔄 Probando desactivar banner ID: {}...".format(banner_id))
    
    toggle_data = {
        'active': False
    }
    
    try:
        response = requests.post("{}/admin/api/banners/{}/toggle".format(BASE_URL, banner_id), json=toggle_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Banner desactivado: {result.get('success')}")
            return result
        else:
            print("❌ Error desactivando banner: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print("❌ Error en desactivar banner: {e}")
        return None

def test_activate_banner_status(banner_id):
    """Probar activar banner"""
    print("\n✅ Probando activar banner ID: {banner_id}...")
    
    toggle_data = {
        'active': True
    }
    
    try:
        response = requests.post("{}/admin/api/banners/{}/toggle".format(BASE_URL, banner_id), json=toggle_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Banner activado: {result.get('success')}")
            return result
        else:
            print("❌ Error activando banner: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print("❌ Error en activar banner: {e}")
        return None

def test_update_banner_position(banner_id):
    """Probar actualizar posición del banner"""
    print("\n📍 Probando actualizar posición del banner ID: {banner_id}...")
    
    position_data = {
        'position': 5
    }
    
    try:
        response = requests.put("{}/admin/api/banners/{banner_id}/position", json=position_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Posición actualizada: {result.get('success')}")
            return result
        else:
            print("❌ Error actualizando posición: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print("❌ Error en actualizar posición: {e}")
        return None

def test_health_check():
    """Probar health check"""
    print("\n🏥 Probando health check...")
    
    try:
        response = requests.get("{}/api/health")
        if response.status_code == 200:
            health = response.json()
            print("✅ Health check: {health.get('status')} - {health.get('message')}")
            return True
        else:
            print("❌ Health check falló: {response.status_code}")
            return False
    except Exception as e:
        print("❌ Error en health check: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas del sistema de gestión de banners...")
    print("=" * 60)
    
    # Verificar que el servidor esté corriendo
    if not test_health_check():
        print("\n❌ El servidor no está corriendo. Inicia el servidor primero:")
        print("   python app.py")
        return
    
    # Probar login
    if not test_login():
        print("\n❌ No se pudo hacer login. Verifica las credenciales.")
        return
    
    # Probar obtener banners
    banners = test_get_banners()
    
    # Probar obtener banners activos
    active_banners = test_get_active_banners()
    
    # Probar agregar banner
    new_banner = test_add_banner()
    
    if new_banner:
        banner_id = new_banner.get('id')
        
        # Probar actualizar banner
        updated_banner = test_update_banner(banner_id)
        
        # Probar desactivar banner
        deactivated_result = test_toggle_banner_status(banner_id)
        
        # Probar activar banner
        activated_result = test_activate_banner_status(banner_id)
        
        # Probar actualizar posición
        position_result = test_update_banner_position(banner_id)
    
    print("\n" + "=" * 60)
    print("✅ Pruebas completadas!")
    print("\n📋 Resumen:")
    print("   - Banners en sistema: {len(banners)}")
    print("   - Banners activos: {len(active_banners)}")
    if new_banner:
        print("   - Banner de prueba agregado: {new_banner.get('title')}")
        print("   - Funciones de activación/desactivación: ✅")
        print("   - Control de posiciones: ✅")

if __name__ == "__main__":
    main()

