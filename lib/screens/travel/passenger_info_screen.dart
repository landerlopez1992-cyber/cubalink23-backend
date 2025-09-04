import 'package:flutter/material.dart';
import 'package:cubalink23/services/duffel_api_service.dart';
import 'package:cubalink23/models/flight_offer.dart';
import 'payment_confirmation_screen.dart';

class PassengerInfoScreen extends StatefulWidget {
  final FlightOffer selectedOffer;
  final int totalPassengers;
  final Map<String, dynamic> searchDetails;

  const PassengerInfoScreen({
    Key? key,
    required this.selectedOffer,
    required this.totalPassengers,
    required this.searchDetails,
  }) : super(key: key);

  @override
  _PassengerInfoScreenState createState() => _PassengerInfoScreenState();
}

class _PassengerInfoScreenState extends State<PassengerInfoScreen> {
  final _formKey = GlobalKey<FormState>();
  List<Map<String, TextEditingController>> _passengerControllers = [];
  bool _isCreatingOrder = false;

  @override
  void initState() {
    super.initState();
    _initializeControllers();
  }

  void _initializeControllers() {
    for (int i = 0; i < widget.totalPassengers; i++) {
      _passengerControllers.add({
        'title': TextEditingController(text: 'mr'),
        'firstName': TextEditingController(),
        'lastName': TextEditingController(),
        'email': TextEditingController(),
        'phone': TextEditingController(),
        'birthDate': TextEditingController(),
        'gender': TextEditingController(text: 'm'),
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[50],
      appBar: AppBar(
        title: Text('Información de Pasajeros'),
        backgroundColor: Theme.of(context).colorScheme.primary,
        foregroundColor: Colors.white,
        elevation: 0,
      ),
      body: Column(
        children: [
          // Resumen del vuelo seleccionado
          Container(
            width: double.infinity,
            padding: EdgeInsets.all(20),
            margin: EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(16),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity( 0.08),
                  blurRadius: 10,
                  offset: Offset(0, 2),
                ),
              ],
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Icon(Icons.flight_takeoff, 
                      color: Theme.of(context).colorScheme.primary, size: 20),
                    SizedBox(width: 8),
                    Text(
                      'Vuelo Seleccionado',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: Colors.grey[800],
                      ),
                    ),
                  ],
                ),
                SizedBox(height: 16),
                
                // Información principal del vuelo
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            widget.selectedOffer.airline,
                            style: TextStyle(
                              fontWeight: FontWeight.w600,
                              fontSize: 16,
                              color: Colors.grey[800],
                            ),
                          ),
                          SizedBox(height: 4),
                          Text(
                            '${widget.selectedOffer.formattedDepartureTime} - ${widget.selectedOffer.formattedArrivalTime}',
                            style: TextStyle(color: Colors.grey[600], fontSize: 14),
                          ),
                          Text(
                            widget.selectedOffer.stopsText,
                            style: TextStyle(color: Colors.grey[500], fontSize: 12),
                          ),
                        ],
                      ),
                    ),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.end,
                      children: [
                        Container(
                          padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                          decoration: BoxDecoration(
                            color: Theme.of(context).colorScheme.primary,
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: Text(
                            widget.selectedOffer.formattedPrice,
                            style: TextStyle(
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                              fontSize: 16,
                            ),
                          ),
                        ),
                        SizedBox(height: 4),
                        Text(
                          'por persona',
                          style: TextStyle(
                            color: Colors.grey[500],
                            fontSize: 11,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
                
                SizedBox(height: 16),
                
                // Información adicional del vuelo
                Container(
                  padding: EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.grey[50],
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Row(
                    children: [
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Duración',
                              style: TextStyle(color: Colors.grey[600], fontSize: 12),
                            ),
                            Text(
                              widget.selectedOffer.formattedDuration,
                              style: TextStyle(fontWeight: FontWeight.w600),
                            ),
                          ],
                        ),
                      ),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Pasajeros',
                              style: TextStyle(color: Colors.grey[600], fontSize: 12),
                            ),
                            Text(
                              '${widget.totalPassengers}',
                              style: TextStyle(fontWeight: FontWeight.w600),
                            ),
                          ],
                        ),
                      ),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Clase',
                              style: TextStyle(color: Colors.grey[600], fontSize: 12),
                            ),
                            Text(
                              widget.searchDetails['cabinClass'] ?? 'Económica',
                              style: TextStyle(fontWeight: FontWeight.w600),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          
          Expanded(
            child: Form(
              key: _formKey,
              child: ListView.builder(
                padding: EdgeInsets.symmetric(horizontal: 16),
                itemCount: widget.totalPassengers,
                itemBuilder: (context, index) {
                  return _buildPassengerForm(index);
                },
              ),
            ),
          ),
          
          // Botón de continuar
          Container(
            width: double.infinity,
            padding: EdgeInsets.all(20),
            child: ElevatedButton(
              onPressed: _isCreatingOrder ? null : _createBooking,
              style: ElevatedButton.styleFrom(
                backgroundColor: Theme.of(context).colorScheme.primary,
                foregroundColor: Colors.white,
                padding: EdgeInsets.symmetric(vertical: 16),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              child: _isCreatingOrder
                  ? Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(
                            color: Colors.white,
                            strokeWidth: 2,
                          ),
                        ),
                        SizedBox(width: 12),
                        Text(
                          'Creando Reserva...',
                          style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
                        ),
                      ],
                    )
                  : Text(
                      'Crear Reserva',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildPassengerForm(int index) {
    final controllers = _passengerControllers[index];
    
    return Container(
      margin: EdgeInsets.only(bottom: 20),
      padding: EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity( 0.08),
            blurRadius: 10,
            offset: Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: Theme.of(context).colorScheme.primary.withOpacity( 0.1),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Icon(
                  Icons.person,
                  color: Theme.of(context).colorScheme.primary,
                  size: 20,
                ),
              ),
              SizedBox(width: 12),
              Text(
                'Pasajero ${index + 1}',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Colors.grey[800],
                ),
              ),
            ],
          ),
          SizedBox(height: 20),
          
          // Fila de Título y Género
          Row(
            children: [
              Expanded(
                child: DropdownButtonFormField<String>(
                  value: controllers['title']?.text ?? 'mr',
                  decoration: InputDecoration(
                    labelText: 'Título',
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                    filled: true,
                    fillColor: Colors.grey[50],
                  ),
                  items: [
                    DropdownMenuItem(value: 'mr', child: Text('Sr.')),
                    DropdownMenuItem(value: 'mrs', child: Text('Sra.')),
                    DropdownMenuItem(value: 'ms', child: Text('Srta.')),
                  ],
                  onChanged: (value) {
                    controllers['title']?.text = value ?? 'mr';
                    // Auto-set gender based on title
                    if (value == 'mr') {
                      controllers['gender']?.text = 'm';
                    } else {
                      controllers['gender']?.text = 'f';
                    }
                  },
                ),
              ),
              SizedBox(width: 12),
              Expanded(
                child: DropdownButtonFormField<String>(
                  value: controllers['gender']?.text ?? 'm',
                  decoration: InputDecoration(
                    labelText: 'Género',
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                    filled: true,
                    fillColor: Colors.grey[50],
                  ),
                  items: [
                    DropdownMenuItem(value: 'm', child: Text('Masculino')),
                    DropdownMenuItem(value: 'f', child: Text('Femenino')),
                  ],
                  onChanged: (value) {
                    controllers['gender']?.text = value ?? 'm';
                  },
                ),
              ),
            ],
          ),
          SizedBox(height: 16),
          
          // Nombre y Apellido
          Row(
            children: [
              Expanded(
                child: TextFormField(
                  controller: controllers['firstName'],
                  decoration: InputDecoration(
                    labelText: 'Nombre',
                    hintText: 'Ingrese su nombre',
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                    filled: true,
                    fillColor: Colors.grey[50],
                    prefixIcon: Icon(Icons.person_outline),
                  ),
                  validator: (value) {
                    if (value == null || value.trim().isEmpty) {
                      return 'Requerido';
                    }
                    return null;
                  },
                ),
              ),
              SizedBox(width: 12),
              Expanded(
                child: TextFormField(
                  controller: controllers['lastName'],
                  decoration: InputDecoration(
                    labelText: 'Apellido',
                    hintText: 'Ingrese su apellido',
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                    filled: true,
                    fillColor: Colors.grey[50],
                    prefixIcon: Icon(Icons.person_outline),
                  ),
                  validator: (value) {
                    if (value == null || value.trim().isEmpty) {
                      return 'Requerido';
                    }
                    return null;
                  },
                ),
              ),
            ],
          ),
          SizedBox(height: 16),
          
          // Email
          TextFormField(
            controller: controllers['email'],
            keyboardType: TextInputType.emailAddress,
            decoration: InputDecoration(
              labelText: 'Email',
              hintText: 'ejemplo@correo.com',
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              filled: true,
              fillColor: Colors.grey[50],
              prefixIcon: Icon(Icons.email_outlined),
            ),
            validator: (value) {
              if (value == null || value.trim().isEmpty) {
                return 'El email es requerido';
              }
              if (!RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$').hasMatch(value)) {
                return 'Email inválido';
              }
              return null;
            },
          ),
          SizedBox(height: 16),
          
          // Teléfono
          TextFormField(
            controller: controllers['phone'],
            keyboardType: TextInputType.phone,
            decoration: InputDecoration(
              labelText: 'Teléfono',
              hintText: '+1234567890',
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              filled: true,
              fillColor: Colors.grey[50],
              prefixIcon: Icon(Icons.phone_outlined),
            ),
            validator: (value) {
              if (value == null || value.trim().isEmpty) {
                return 'El teléfono es requerido';
              }
              if (!value.startsWith('+')) {
                return 'Debe incluir código de país (+)';
              }
              return null;
            },
          ),
          SizedBox(height: 16),
          
          // Fecha de nacimiento
          GestureDetector(
            onTap: () => _selectBirthDate(context, index),
            child: AbsorbPointer(
              child: TextFormField(
                controller: controllers['birthDate'],
                decoration: InputDecoration(
                  labelText: 'Fecha de Nacimiento',
                  hintText: 'YYYY-MM-DD',
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                  filled: true,
                  fillColor: Colors.grey[50],
                  prefixIcon: Icon(Icons.calendar_today),
                ),
                validator: (value) {
                  if (value == null || value.trim().isEmpty) {
                    return 'La fecha de nacimiento es requerida';
                  }
                  return null;
                },
              ),
            ),
          ),
        ],
      ),
    );
  }

  Future<void> _selectBirthDate(BuildContext context, int passengerIndex) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: DateTime(1990, 1, 1),
      firstDate: DateTime(1900),
      lastDate: DateTime.now(),
      builder: (context, child) {
        return Theme(
          data: Theme.of(context).copyWith(
            colorScheme: Theme.of(context).colorScheme.copyWith(
              primary: Theme.of(context).colorScheme.primary,
            ),
          ),
          child: child!,
        );
      },
    );
    
    if (picked != null) {
      setState(() {
        _passengerControllers[passengerIndex]['birthDate']?.text = 
            '${picked.year}-${picked.month.toString().padLeft(2, '0')}-${picked.day.toString().padLeft(2, '0')}';
      });
    }
  }

  Future<void> _createBooking() async {
    if (!_formKey.currentState!.validate()) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Por favor complete todos los campos requeridos'),
          backgroundColor: Colors.orange[600],
          behavior: SnackBarBehavior.floating,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        ),
      );
      return;
    }

    setState(() {
      _isCreatingOrder = true;
    });

    try {
      print('🎯 CREANDO RESERVA CON DUFFEL API');
      
      // Preparar datos del primer pasajero (Duffel requiere solo 1 por llamada)
      final controllers = _passengerControllers[0];
      final passengerData = {
        'title': controllers['title']?.text ?? 'mr',
        'given_name': controllers['firstName']?.text?.trim() ?? '',
        'family_name': controllers['lastName']?.text?.trim() ?? '',
        'email': controllers['email']?.text?.trim() ?? '',
        'phone_number': controllers['phone']?.text?.trim() ?? '',
        'born_on': controllers['birthDate']?.text ?? '',
        'gender': controllers['gender']?.text ?? 'm',
      };

      print('👤 Datos del pasajero: ${passengerData['given_name']} ${passengerData['family_name']}');
      print('✈️ Vuelo seleccionado: ${widget.selectedOffer.id}');
      print('💰 Precio total: ${widget.selectedOffer.formattedPrice}');

      // Llamar a la API de Duffel para crear la reserva
      final bookingResult = await DuffelApiService.createBooking(
        offerId: widget.selectedOffer.id,
        passengers: [passengerData],
      );

      if (bookingResult != null) {
        print('🎉 ¡Reserva creada exitosamente!');
        print('📋 Order ID: ${bookingResult['data']['id']}');
        
        // Navegar a pantalla de confirmación de pago
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(
            builder: (context) => PaymentConfirmationScreen(
              selectedOffer: widget.selectedOffer,
              bookingData: bookingResult,
              passengerInfo: passengerData,
            ),
          ),
        );
      } else {
        _showError('Error al crear la reserva. Por favor intente nuevamente.');
      }
      
    } catch (e) {
      print('❌ Error creando reserva: $e');
      _showError('Error al crear la reserva: ${e.toString()}');
    } finally {
      if (mounted) {
        setState(() {
          _isCreatingOrder = false;
        });
      }
    }
  }

  void _showError(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: Colors.red[600],
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        duration: Duration(seconds: 5),
      ),
    );
  }

  @override
  void dispose() {
    for (final controllers in _passengerControllers) {
      controllers.values.forEach((controller) => controller.dispose());
    }
    super.dispose();
  }
}