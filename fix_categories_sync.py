#!/usr/bin/env python3
"""
Script para sincronizar las categorías entre la app y el panel admin
"""

def fix_categories_in_html():
    print("🔧 Sincronizando categorías en el panel admin...")
    
    # Leer el archivo HTML
    with open('templates/admin/products.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Mapeo de categorías antiguas a nuevas
    category_mapping = {
        "'Electrónicos'": "'electronicos'",
        "'Ropa'": "'ropa'", 
        "'Comida'": "'alimentos'",
        "'Servicios'": "'servicios'",
        "'Motos'": "'motos'",
        "'Alimentos'": "'alimentos'",
        "'Amazon'": "'amazon'",
        "'Walmart'": "'walmart'",
        '"Electrónicos"': '"electronicos"',
        '"Ropa"': '"ropa"',
        '"Comida"': '"alimentos"',
        '"Servicios"': '"servicios"',
        '"Motos"': '"motos"',
        '"Alimentos"': '"alimentos"',
        '"Amazon"': '"amazon"',
        '"Walmart"': '"walmart"'
    }
    
    # Aplicar los cambios
    for old_cat, new_cat in category_mapping.items():
        content = content.replace(old_cat, new_cat)
        print(f"✅ {old_cat} → {new_cat}")
    
    # Escribir el archivo actualizado
    with open('templates/admin/products.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("🎉 Categorías sincronizadas exitosamente!")

if __name__ == "__main__":
    fix_categories_in_html()
