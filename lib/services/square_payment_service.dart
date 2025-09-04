// SQUARE COMPLETAMENTE DESACTIVADO
// Este servicio ahora funciona en modo simulación

class SquarePaymentService {
  // Square desconectado - sin credenciales reales

  /// Initialize Square Payment Service (DESACTIVADO)
  static Future<void> initialize() async {
    // Square completamente desactivado
    print('🚫 Square DESCONECTADO - funcionando en modo simulación');
  }

  /// Procesar pago SIMULADO (Square desconectado)
  static Future<SquarePaymentResult> processPayment({
    required double amount,
    required String description,
    required String cardLast4,
    required String cardType,
    required String cardHolderName,
  }) async {
    // SIMULACIÓN: Square completamente desactivado
    print('🎭 PAGO SIMULADO (Square desconectado)');
    print('💳 Monto: \$${amount.toStringAsFixed(2)}');
    print('💳 Tarjeta: $cardType ****$cardLast4');
    print('💳 Titular: $cardHolderName');
    
    // Simular procesamiento
    await Future.delayed(const Duration(seconds: 2));
    
    // Generar resultado simulado
    final String fakeTransactionId = 'SIMULADO_${DateTime.now().millisecondsSinceEpoch}';
    
    print('✅ PAGO SIMULADO EXITOSO');
    print('🆔 ID Simulado: $fakeTransactionId');
    
    return SquarePaymentResult(
      success: true,
      transactionId: fakeTransactionId,
      message: 'Pago procesado exitosamente (SIMULADO)',
      amount: amount,
    );
  }
  

}

/// Resultado del pago Square
class SquarePaymentResult {
  final bool success;
  final String? transactionId;
  final String message;
  final double amount;

  SquarePaymentResult({
    required this.success,
    required this.transactionId,
    required this.message,
    required this.amount,
  });

  @override
  String toString() {
    return 'SquarePaymentResult(success: $success, transactionId: $transactionId, message: $message, amount: $amount)';
  }
}