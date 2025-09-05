class CartItem {
  final String id;
  final String name;
  final double price;
  final String imageUrl;
  final int quantity;
  final String type; // 'amazon', 'recharge', etc.
  final String? description;
  final dynamic weight; // Puede ser double (peso real) o String (peso con texto/desconocido)
  final double? weightLb; // Peso en libras (más preciso)
  final String? category;
  final String? vendorId; // ID del vendedor (amazon, walmart, admin, etc.)
  final Map<String, dynamic>? additionalData;

  const CartItem({
    required this.id,
    required this.name,
    required this.price,
    required this.imageUrl,
    required this.quantity,
    required this.type,
    this.description,
    this.weight,
    this.weightLb,
    this.category,
    this.vendorId,
    this.additionalData,
  });

  CartItem copyWith({
    String? id,
    String? name,
    double? price,
    String? imageUrl,
    int? quantity,
    String? type,
    String? description,
    dynamic weight,
    double? weightLb,
    String? category,
    String? vendorId,
    Map<String, dynamic>? additionalData,
  }) {
    return CartItem(
      id: id ?? this.id,
      name: name ?? this.name,
      price: price ?? this.price,
      imageUrl: imageUrl ?? this.imageUrl,
      quantity: quantity ?? this.quantity,
      type: type ?? this.type,
      description: description ?? this.description,
      weight: weight ?? this.weight,
      weightLb: weightLb ?? this.weightLb,
      category: category ?? this.category,
      vendorId: vendorId ?? this.vendorId,
      additionalData: additionalData ?? this.additionalData,
    );
  }

  double get totalPrice => price * quantity;

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'price': price,
      'imageUrl': imageUrl,
      'quantity': quantity,
      'type': type,
      'description': description,
      'weight': weight,
      'weightLb': weightLb,
      'category': category,
      'vendorId': vendorId,
      'additionalData': additionalData,
      'timestamp': DateTime.now().millisecondsSinceEpoch,
    };
  }

  Map<String, dynamic> toMap() => toJson();

  factory CartItem.fromJson(Map<String, dynamic> json) {
    return CartItem(
      id: json['id'] ?? '',
      name: json['name'] ?? '',
      price: (json['price'] ?? 0).toDouble(),
      imageUrl: json['imageUrl'] ?? '',
      quantity: json['quantity'] ?? 1,
      type: json['type'] ?? 'unknown',
      description: json['description'],
      weight: json['weight'], // Mantener como dynamic
      weightLb: json['weightLb']?.toDouble(),
      category: json['category'],
      vendorId: json['vendorId'],
      additionalData: json['additionalData'],
    );
  }
}