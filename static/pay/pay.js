function createParticles() {
    const container = document.querySelector('.bg-particles');
    for (let i = 0; i < 50; i++) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    particle.style.left = Math.random() * 100 + '%';
    particle.style.top = Math.random() * 100 + '%';
    particle.style.animationDelay = Math.random() * 6 + 's';
    particle.style.animationDuration = (Math.random() * 3 + 3) + 's';
    container.appendChild(particle);
    }
}
createParticles();

function getQueryParam(name) {
    const url = new URL(window.location.href);
    return url.searchParams.get(name);
}
const propertyId = getQueryParam('propertyId');
const qty = parseInt(getQueryParam('qty')) || 1;
let currentStep = 1;
let selectedPaymentMethod = 'card';
let selectedCard = '1';
let property = null;
const mockProperty = {
    id: '1',
    title: 'Luxury Downtown Apartment',
    location: 'Manhattan, NY',
    tokenPrice: 1250,
    image: 'https://via.placeholder.com/300x200'
};

function loadProperty() {
    property = mockProperty;
    updateSummary();
}

function updateSummary() {
    const subtotal = qty * property.tokenPrice;
    const fees = Math.round(subtotal * 0.025);
    const total = subtotal + fees;
    document.getElementById('checkoutSummary').innerHTML = `
    <div class="summary-row">
        <span class="summary-label">${property.title}</span>
        <span class="summary-value">$${property.tokenPrice.toLocaleString()}</span>
    </div>
    <div class="summary-row">
        <span class="summary-label">Location</span>
        <span class="summary-value">${property.location}</span>
    </div>
    <div class="summary-row">
        <span class="summary-label">Tokens × ${qty}</span>
        <span class="summary-value">$${subtotal.toLocaleString()}</span>
    </div>
    <div class="summary-row">
        <span class="summary-label">Platform Fee (2.5%)</span>
        <span class="summary-value">$${fees.toLocaleString()}</span>
    </div>
    <div class="summary-row">
        <span class="summary-label">Total</span>
        <span class="summary-value total-value">$${total.toLocaleString()}</span>
    </div>
    `;
}

function updateProgress() {
    const progressFill = document.getElementById('progressFill');
    const percentage = (currentStep / 3) * 100;
    progressFill.style.width = percentage + '%';
}
document.querySelectorAll('.payment-tab').forEach(tab => {
    tab.addEventListener('click', function() {
    document.querySelectorAll('.payment-tab').forEach(t => t.classList.remove('active'));
    this.classList.add('active');
    selectedPaymentMethod = this.dataset.tab;
    document.querySelectorAll('.payment-content').forEach(content => {
        content.style.display = 'none';
    });
    document.getElementById(selectedPaymentMethod + 'Content').style.display = 'block';
    currentStep = 2;
    updateProgress();
    });
});
document.querySelectorAll('.saved-card').forEach(card => {
    card.addEventListener('click', function() {
    if (this.id === 'addNewCard' || this.id === 'addNewBank') return;
    document.querySelectorAll('.saved-card').forEach(c => c.classList.remove('selected'));
    this.classList.add('selected');
    selectedCard = this.dataset.card || this.dataset.bank || this.dataset.crypto;
    currentStep = 3;
    updateProgress();
    });
});
document.getElementById('addNewCard').addEventListener('click', function() {
    document.getElementById('checkoutForm').classList.add('active');
    currentStep = 2;
    updateProgress();
});
document.querySelectorAll('input').forEach(input => {
    input.addEventListener('focus', function() {
    this.parentElement.style.transform = 'translateY(-2px)';
    });
    input.addEventListener('blur', function() {
    this.parentElement.style.transform = 'translateY(0)';
    });
});
document.getElementById('card').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
    let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
    e.target.value = formattedValue;
});

// Expiry date formatting
document.getElementById('exp').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length >= 2) {
        value = value.substring(0, 2) + '/' + value.substring(2, 4);
    }
    e.target.value = value;
});