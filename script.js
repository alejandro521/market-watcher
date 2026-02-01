let userId = null;

// --- Signup ---
async function signup() {
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    const res = await fetch('/auth/signup', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({email, password})
    });
    const data = await res.json();
    document.getElementById('signup-message').innerText = data.message || data.detail;
}

// --- Login ---
async function login() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const res = await fetch('/auth/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({email, password})
    });
    const data = await res.json();
    if (data.user_id) {
        userId = data.user_id;
        document.getElementById('login-message').innerText = "Login successful!";
        document.getElementById('signup-section').style.display = 'none';
        document.getElementById('login-section').style.display = 'none';
        document.getElementById('alerts-section').style.display = 'block';
        loadAlerts();
    } else {
        document.getElementById('login-message').innerText = data.detail || "Login failed";
    }
}

// --- Load Alerts ---
async function loadAlerts() {
    const res = await fetch(`/alerts/list/${userId}`);
    const data = await res.json();
    const list = document.getElementById('alerts-list');
    list.innerHTML = '';
    data.alerts.forEach(alert => {
        const li = document.createElement('li');
        li.innerText = `${alert.symbol} - ${alert.direction} ${alert.target_price}`;
        list.appendChild(li);
    });
}

// --- Add Alert ---
async function addAlert() {
    const symbol = document.getElementById('alert-symbol').value;
    const target_price = parseFloat(document.getElementById('alert-price').value);
    const direction = document.getElementById('alert-direction').value;
    const res

