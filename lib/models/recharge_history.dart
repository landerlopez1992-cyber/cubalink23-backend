enum RechargeStatus {
  pending,
  completed,
  failed,
  cancelled,
}

enum PaymentMethod {
  paypal,
  creditCard,
  bankTransfer,
  wallet,
}

class RechargeHistory {
  final String id;
  final String phoneNumber;
  final String operator;
  final double amount;
  final DateTime timestamp;
  final String status;

  RechargeHistory({
    required this.id,
    required this.phoneNumber,
    required this.operator,
    required this.amount,
    required this.timestamp,
    required this.status,
  });

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'phoneNumber': phoneNumber,
      'operator': operator,
      'amount': amount,
      'timestamp': timestamp.toIso8601String(),
      'status': status,
    };
  }

  factory RechargeHistory.fromJson(Map<String, dynamic> json) {
    return RechargeHistory(
      id: json['id'],
      phoneNumber: json['phoneNumber'],
      operator: json['operator'],
      amount: (json['amount'] ?? 0).toDouble(),
      timestamp: json['timestamp'] is String ? DateTime.parse(json['timestamp']) : DateTime.now(),
      status: json['status'] ?? 'completed',
    );
  }

  /// Método estático para obtener historial de muestra
  static List<RechargeHistory> getSampleHistory() {
    return [
      RechargeHistory(
        id: 'rh_001',
        phoneNumber: '+52 55 1234 5678',
        operator: 'Telcel',
        amount: 100,
        timestamp: DateTime.now().subtract(Duration(hours: 2)),
        status: 'Completada',
      ),
      RechargeHistory(
        id: 'rh_002',
        phoneNumber: '+53 5 234 5678',
        operator: 'CubaCel',
        amount: 500,
        timestamp: DateTime.now().subtract(Duration(minutes: 30)),
        status: 'Pendiente',
      ),
      RechargeHistory(
        id: 'rh_003',
        phoneNumber: '+1 305 123 4567',
        operator: 'AT&T',
        amount: 25,
        timestamp: DateTime.now().subtract(Duration(days: 1)),
        status: 'Completada',
      ),
    ];
  }
}

class RechargeTransaction {
  final String id;
  final String recipientPhone;
  final String recipientName;
  final String countryCode;
  final String operatorId;
  final double amount;
  final double cost;
  final RechargeStatus status;
  final PaymentMethod paymentMethod;
  final DateTime createdAt;
  final DateTime? completedAt;
  final String? transactionReference;

  RechargeTransaction({
    required this.id,
    required this.recipientPhone,
    required this.recipientName,
    required this.countryCode,
    required this.operatorId,
    required this.amount,
    required this.cost,
    required this.status,
    required this.paymentMethod,
    required this.createdAt,
    this.completedAt,
    this.transactionReference,
  });

  RechargeTransaction copyWith({
    String? id,
    String? recipientPhone,
    String? recipientName,
    String? countryCode,
    String? operatorId,
    double? amount,
    double? cost,
    RechargeStatus? status,
    PaymentMethod? paymentMethod,
    DateTime? createdAt,
    DateTime? completedAt,
    String? transactionReference,
  }) {
    return RechargeTransaction(
      id: id ?? this.id,
      recipientPhone: recipientPhone ?? this.recipientPhone,
      recipientName: recipientName ?? this.recipientName,
      countryCode: countryCode ?? this.countryCode,
      operatorId: operatorId ?? this.operatorId,
      amount: amount ?? this.amount,
      cost: cost ?? this.cost,
      status: status ?? this.status,
      paymentMethod: paymentMethod ?? this.paymentMethod,
      createdAt: createdAt ?? this.createdAt,
      completedAt: completedAt ?? this.completedAt,
      transactionReference: transactionReference ?? this.transactionReference,
    );
  }

  String get statusText {
    switch (status) {
      case RechargeStatus.pending:
        return 'Pendiente';
      case RechargeStatus.completed:
        return 'Completada';
      case RechargeStatus.failed:
        return 'Fallida';
      case RechargeStatus.cancelled:
        return 'Cancelada';
    }
  }

  String get paymentMethodText {
    switch (paymentMethod) {
      case PaymentMethod.paypal:
        return 'PayPal';
      case PaymentMethod.creditCard:
        return 'Tarjeta de Crédito';
      case PaymentMethod.bankTransfer:
        return 'Transferencia Bancaria';
      case PaymentMethod.wallet:
        return 'Wallet';
    }
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'recipientPhone': recipientPhone,
      'recipientName': recipientName,
      'countryCode': countryCode,
      'operatorId': operatorId,
      'amount': amount,
      'cost': cost,
      'status': status.name,
      'paymentMethod': paymentMethod.name,
      'createdAt': createdAt.toIso8601String(),
      'completedAt': completedAt?.toIso8601String(),
      'transactionReference': transactionReference,
    };
  }
  
  /// Alias for toJson() for compatibility
  Map<String, dynamic> toMap() => toJson();

  factory RechargeTransaction.fromJson(Map<String, dynamic> json) {
    return RechargeTransaction(
      id: json['id'],
      recipientPhone: json['recipientPhone'],
      recipientName: json['recipientName'],
      countryCode: json['countryCode'],
      operatorId: json['operatorId'],
      amount: json['amount'].toDouble(),
      cost: json['cost'].toDouble(),
      status: RechargeStatus.values.firstWhere(
        (e) => e.name == json['status'],
        orElse: () => RechargeStatus.pending,
      ),
      paymentMethod: PaymentMethod.values.firstWhere(
        (e) => e.name == json['paymentMethod'],
        orElse: () => PaymentMethod.paypal,
      ),
      createdAt: DateTime.parse(json['createdAt']),
      completedAt: json['completedAt'] != null
          ? DateTime.parse(json['completedAt'])
          : null,
      transactionReference: json['transactionReference'],
    );
  }

  static List<RechargeTransaction> getSampleTransactions() {
    return [
      RechargeTransaction(
        id: 'tx_001',
        recipientPhone: '+52 55 1234 5678',
        recipientName: 'María González',
        countryCode: 'MX',
        operatorId: 'telcel_mx',
        amount: 100,
        cost: 104.99,
        status: RechargeStatus.completed,
        paymentMethod: PaymentMethod.paypal,
        createdAt: DateTime.now().subtract(Duration(hours: 2)),
        completedAt: DateTime.now().subtract(Duration(hours: 2, minutes: 5)),
        transactionReference: 'TXN123456789',
      ),
      RechargeTransaction(
        id: 'tx_002',
        recipientPhone: '+53 5 234 5678',
        recipientName: 'Carlos Herrera',
        countryCode: 'CU',
        operatorId: 'cubacel_cu',
        amount: 500,
        cost: 21.99,
        status: RechargeStatus.pending,
        paymentMethod: PaymentMethod.creditCard,
        createdAt: DateTime.now().subtract(Duration(minutes: 30)),
        transactionReference: 'TXN987654321',
      ),
      RechargeTransaction(
        id: 'tx_003',
        recipientPhone: '+1 305 123 4567',
        recipientName: 'Ana Pérez',
        countryCode: 'US',
        operatorId: 'att_us',
        amount: 25,
        cost: 26.99,
        status: RechargeStatus.completed,
        paymentMethod: PaymentMethod.creditCard,
        createdAt: DateTime.now().subtract(Duration(days: 1)),
        completedAt: DateTime.now().subtract(Duration(days: 1, minutes: 3)),
        transactionReference: 'TXN456789123',
      ),
    ];
  }
}