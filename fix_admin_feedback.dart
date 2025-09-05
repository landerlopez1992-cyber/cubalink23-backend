
// Script para arreglar feedback del panel admin
// Modificar lib/screens/admin/store_settings_screen.dart

// En el método _showProductDialog, después de crear/actualizar producto:

try {
  // ... código existente para crear/actualizar producto ...
  
  if (success) {
    Navigator.pop(context); // Cerrar dialog de carga
    Navigator.pop(context); // Cerrar dialog de producto
    
    await _loadData(); // Recargar datos
    
    // ARREGLO: Mostrar mensaje de éxito más visible
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Row(
          children: [
            Icon(Icons.check_circle, color: Colors.white),
            SizedBox(width: 8),
            Expanded(
              child: Text(
                isEditing ? '✅ Producto actualizado exitosamente' : '✅ Producto creado exitosamente',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
            ),
          ],
        ),
        backgroundColor: Colors.green,
        duration: Duration(seconds: 4),
        behavior: SnackBarBehavior.floating,
        margin: EdgeInsets.all(16),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
      ),
    );
    
    // ARREGLO: Mostrar también un dialog de confirmación
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Row(
          children: [
            Icon(Icons.check_circle, color: Colors.green),
            SizedBox(width: 8),
            Text('Éxito'),
          ],
        ),
        content: Text(
          isEditing ? 'El producto ha sido actualizado correctamente.' : 'El producto ha sido creado correctamente.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('Continuar'),
          ),
        ],
      ),
    );
    
  } else {
    throw Exception(errorMessage ?? 'Error desconocido guardando el producto');
  }
  
} catch (e) {
  // ... código existente para manejo de errores ...
  
  // ARREGLO: Mostrar error más visible
  ScaffoldMessenger.of(context).showSnackBar(
    SnackBar(
      content: Row(
        children: [
          Icon(Icons.error, color: Colors.white),
          SizedBox(width: 8),
          Expanded(
            child: Text(
              'Error: \$userFriendlyError',
              style: TextStyle(fontSize: 16),
            ),
          ),
        ],
      ),
      backgroundColor: Colors.red,
      duration: Duration(seconds: 6),
      behavior: SnackBarBehavior.floating,
      margin: EdgeInsets.all(16),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(8),
      ),
      action: SnackBarAction(
        label: 'Ver Solución',
        textColor: Colors.white,
        onPressed: () => _showSupabaseSetupDialog(context),
      ),
    ),
  );
}
