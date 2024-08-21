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


// Handle form submit

var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    card.update({ 'disabled': true});  // Disable the card input
    $('#submit-button').attr('disabled', true);  // Disable the submit button

    // Confirm the card payment using the client secret
    stripe.confirmCardPayment(client_secret, {
        payment_method: {
            card: card,  // Attach the card element
        }
    }).then(function(result) {
        if (result.error) {
            // Show error to your customer
            var errorDiv = document.getElementById('card-errors');
            var html = `
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            $(errorDiv).html(html);
            card.update({ 'disabled': false});
            $('#submit-button').attr('disabled', false);
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                // Payment has succeeded, submit the form
                form.submit();
            }
        }
    });
});
