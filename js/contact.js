// Contact form handling with EmailJS
document.addEventListener('DOMContentLoaded', function() {
    emailjs.init({
        publicKey: 'zeTxx5s2bnFI56ONe',
        disableSentry: true
    });

    const contactForm = document.getElementById('contactForm');
    // ... rest of the code
});
    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();
            const message = document.getElementById('message').value.trim();
            
            if (!name || !email || !message) {
                alert('Please fill out all fields.');
                return;
            }
            
            // Show loading state
            const submitButton = contactForm.querySelector('button[type="submit"]');
            const originalButtonText = submitButton.textContent;
            submitButton.textContent = 'Sending...';
            submitButton.disabled = true;

            
            // Set form field names
            document.getElementById('name').name = 'Name';
            document.getElementById('email').name = 'Email';
            document.getElementById('message').name = 'Message';

            console.log(window.emailjs);

            emailjs.sendForm('Service_ID_EmailJS', 'Email_template', contactForm) 
                .then(function(response) {
                    console.log('SUCCESS!', response.status, response.text);
                    
                    // Show success message
                    alert('Your message has been sent successfully!');
                    
                    // Reset form
                    contactForm.reset();
                })
                .catch(function(error) {
                    console.error('FAILED...', error, JSON.stringify(error, null, 2));
                    alert('Failed to send message. Please try again later.');
                })
                .finally(function() {
                    // Restore button state
                    submitButton.textContent = originalButtonText;
                    submitButton.disabled = false;
                });
               
        });
    } else {
        console.error('Contact form not found');
    }