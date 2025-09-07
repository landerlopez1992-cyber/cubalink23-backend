#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de rollback para el backend
Permite volver al estado anterior si algo sale mal después del deploy
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Ejecutar comando y mostrar resultado"""
    print("🔄 " + description + "...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ " + description + " completado")
            return True
        else:
            print("   ❌ Error en " + description + ":")
            print("   " + result.stderr)
            return False
    except Exception as e:
        print("   ❌ Error ejecutando " + description + ": " + str(e))
        return False

def rollback_to_safe_check():
    """Hacer rollback al branch safe-check"""
    print("🚨 INICIANDO ROLLBACK DEL BACKEND")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("admin_routes.py"):
        print("❌ Error: No estás en el directorio backend-duffel")
        return False
    
    # Cambiar al branch safe-check
    if not run_command("git checkout safe-check", "Cambiando a branch safe-check"):
        return False
    
    # Hacer push del rollback
    if not run_command("git push origin safe-check", "Pusheando rollback a GitHub"):
        return False
    
    print("=" * 50)
    print("✅ ROLLBACK COMPLETADO")
    print("📝 El backend ha vuelto al estado seguro")
    print("🌐 Render.com debería detectar el cambio y hacer rollback automático")
    return True

def main():
    """Función principal"""
    if len(sys.argv) > 1 and sys.argv[1] == "--force":
        rollback_to_safe_check()
    else:
        print("⚠️  ADVERTENCIA: Este script hará rollback del backend")
        print("📝 Esto volverá al estado anterior al deploy")
        print()
        response = input("¿Estás seguro de que quieres hacer rollback? (escribe 'SI' para confirmar): ")
        
        if response == "SI":
            rollback_to_safe_check()
        else:
            print("❌ Rollback cancelado")

if __name__ == "__main__":
    main()
