const API_BASE = 'http://localhost:5000/api';

// Utilities
async function fetchAPI(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
            },
            ...options,
        });
        if (!response.ok) throw new Error('API Request Failed');
        if (options.method === 'DELETE') return null;
        return await response.json();
    } catch (e) {
        console.error(e);
        alert('Operation failed');
    }
}

// Customers
async function loadCustomers() {
    const customers = await fetchAPI('/customers');
    const tableBody = document.getElementById('customerTableBody');
    if (!tableBody) return;
    
    tableBody.innerHTML = customers.map(c => `
        <tr>
            <td>${c.name}</td>
            <td>${c.email}</td>
            <td>${c.phone || '-'}</td>
            <td>
                <button class="btn btn-danger btn-sm" onclick="deleteCustomer(${c.id})">Delete</button>
            </td>
        </tr>
    `).join('');
}

async function createCustomer(event) {
    event.preventDefault();
    const data = {
        name: document.getElementById('cName').value,
        email: document.getElementById('cEmail').value,
        phone: document.getElementById('cPhone').value
    };
    await fetchAPI('/customers', {
        method: 'POST',
        body: JSON.stringify(data)
    });
    closeModal('customerModal');
    loadCustomers();
}

async function deleteCustomer(id) {
    if(!confirm('Are you sure?')) return;
    await fetchAPI(`/customers/${id}`, { method: 'DELETE' });
    loadCustomers();
}

// Vehicles
async function loadVehicles() {
    const vehicles = await fetchAPI('/vehicles');
    const tableBody = document.getElementById('vehicleTableBody');
    if (!tableBody) return;

    tableBody.innerHTML = vehicles.map(v => `
        <tr>
            <td>${v.license_plate}</td>
            <td>${v.model}</td>
            <td>${v.customer_id}</td>
            <td>
                <button class="btn btn-danger btn-sm" onclick="deleteVehicle(${v.id})">Delete</button>
            </td>
        </tr>
    `).join('');
}

async function createVehicle(event) {
    event.preventDefault();
    const data = {
        license_plate: document.getElementById('vLicense').value,
        model: document.getElementById('vModel').value,
        customer_id: document.getElementById('vOwner').value
    };
    await fetchAPI('/vehicles', {
        method: 'POST',
        body: JSON.stringify(data)
    });
    closeModal('vehicleModal');
    loadVehicles();
}

async function deleteVehicle(id) {
    if(!confirm('Are you sure?')) return;
    await fetchAPI(`/vehicles/${id}`, { method: 'DELETE' });
    loadVehicles();
}

// Services
async function loadServices() {
    const services = await fetchAPI('/services');
    const tableBody = document.getElementById('serviceTableBody');
    if (!tableBody) return;

    tableBody.innerHTML = services.map(s => `
        <tr>
            <td>${s.description}</td>
            <td>$${s.cost}</td>
            <td>${s.vehicle_id}</td>
            <td>${new Date(s.date).toLocaleDateString()}</td>
            <td>
                <button class="btn btn-danger btn-sm" onclick="deleteService(${s.id})">Delete</button>
            </td>
        </tr>
    `).join('');
}

async function createService(event) {
    event.preventDefault();
    const data = {
        description: document.getElementById('sDesc').value,
        cost: document.getElementById('sCost').value,
        vehicle_id: document.getElementById('sVehicle').value
    };
    await fetchAPI('/services', {
        method: 'POST',
        body: JSON.stringify(data)
    });
    closeModal('serviceModal');
    loadServices();
}

async function deleteService(id) {
    if(!confirm('Are you sure?')) return;
    await fetchAPI(`/services/${id}`, { method: 'DELETE' });
    loadServices();
}

// Modal Logic
function openModal(id) {
    document.getElementById(id).classList.add('active');
}

function closeModal(id) {
    document.getElementById(id).classList.remove('active');
}
