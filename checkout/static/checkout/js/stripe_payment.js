// stripe_payment.js
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Stripe with the public key passed from the template
    const stripe = Stripe(stripePublicKey);

    // Create an instance of Elements
    const elements = stripe.elements();

    // Create an instance of the card Element
    const card = elements.create('card');

    // Add an instance of the card Element into the `card-element` div
    card.mount('#card-element');

    // Handle real-time validation errors from the card Element.
    card.on('change', function(event) {
        const displayError = document.getElementById('card-errors');
        if (event.error) {
            displayError.textContent = event.error.message;
        } else {
            displayError.textContent = '';
        }
    });
});

