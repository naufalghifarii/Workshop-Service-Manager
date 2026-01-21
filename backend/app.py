from flask import Flask, request, jsonify, g
from flask_cors import CORS
from config import Config
from models import db, Customer, Vehicle, Service
from prometheus_client import generate_latest, Counter, Histogram, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)

# Prometheus Metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP Request Duration', ['method', 'endpoint'])
DB_LATENCY = Histogram('db_query_duration_seconds', 'Database Query Duration', ['operation'])

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    if request.path != '/metrics':
        latency = time.time() - g.start_time
        REQUEST_LATENCY.labels(method=request.method, endpoint=request.path).observe(latency)
        REQUEST_COUNT.labels(method=request.method, endpoint=request.path, status=response.status_code).inc()
    return response

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

# CRUD Routes for Customers
@app.route('/api/customers', methods=['GET', 'POST'])
@app.route('/api/customers', methods=['GET', 'POST'])
def handle_customers():
    if request.method == 'POST':
        data = request.json
        new_customer = Customer(name=data['name'], email=data['email'], phone=data.get('phone'))
        with DB_LATENCY.labels(operation='insert_customer').time():
            db.session.add(new_customer)
            db.session.commit()
        return jsonify(new_customer.to_dict()), 201
    else:
        with DB_LATENCY.labels(operation='select_customers').time():
            customers = Customer.query.all()
        return jsonify([c.to_dict() for c in customers])

@app.route('/api/customers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_customer_id(id):
    customer = Customer.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify(customer.to_dict())
    elif request.method == 'PUT':
        data = request.json
        customer.name = data.get('name', customer.name)
        customer.email = data.get('email', customer.email)
        customer.phone = data.get('phone', customer.phone)
        db.session.commit()
        return jsonify(customer.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(customer)
        db.session.commit()
        return '', 204

# CRUD Routes for Vehicles
@app.route('/api/vehicles', methods=['GET', 'POST'])
@app.route('/api/vehicles', methods=['GET', 'POST'])
def handle_vehicles():
    if request.method == 'POST':
        data = request.json
        new_vehicle = Vehicle(
            license_plate=data['license_plate'],
            model=data['model'], 
            customer_id=data['customer_id']
        )
        with DB_LATENCY.labels(operation='insert_vehicle').time():
            db.session.add(new_vehicle)
            db.session.commit()
        return jsonify(new_vehicle.to_dict()), 201
    else:
        with DB_LATENCY.labels(operation='select_vehicles').time():
            vehicles = Vehicle.query.all()
        return jsonify([v.to_dict() for v in vehicles])

@app.route('/api/vehicles/<int:id>', methods=['DELETE'])
def delete_vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)
    db.session.delete(vehicle)
    db.session.commit()
    return '', 204

# CRUD Routes for Services
@app.route('/api/services', methods=['GET', 'POST'])
@app.route('/api/services', methods=['GET', 'POST'])
def handle_services():
    if request.method == 'POST':
        data = request.json
        new_service = Service(
            description=data['description'],
            cost=data['cost'],
            vehicle_id=data['vehicle_id']
        )
        with DB_LATENCY.labels(operation='insert_service').time():
            db.session.add(new_service)
            db.session.commit()
        return jsonify(new_service.to_dict()), 201
    else:
        with DB_LATENCY.labels(operation='select_services').time():
            services = Service.query.all()
        return jsonify([s.to_dict() for s in services])

@app.route('/api/services/<int:id>', methods=['DELETE'])
def delete_service(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    return '', 204

# DB Init
with app.app_context():
    # Only create tables if they don't exist
    try:
        db.create_all()
    except Exception as e:
        print(f"Error creating database tables: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
