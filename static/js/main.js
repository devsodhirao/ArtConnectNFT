// Main JavaScript file for the Artist Pop-up Event application

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })

    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Implement a simple dark mode toggle
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
        });

        // Check for saved dark mode preference
        if (localStorage.getItem('darkMode') === 'true') {
            document.body.classList.add('dark-mode');
        }
    }

    // Add fade-in effect for content
    const fadeElements = document.querySelectorAll('.fade-in');
    fadeElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transition = 'opacity 0.5s ease-in-out';
        setTimeout(() => {
            element.style.opacity = '1';
        }, 100);
    });
});

// Function to simulate blockchain interaction (to be replaced with real blockchain integration)
function simulateBlockchainInteraction(action, data) {
    console.log(`Simulating blockchain ${action}:`, data);
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve({ success: true, message: `${action} simulated successfully` });
        }, 1000);
    });
}

// Example usage of simulateBlockchainInteraction
// simulateBlockchainInteraction('mint', { artworkId: 1, owner: 'user123' })
//     .then(result => console.log(result))
//     .catch(error => console.error(error));
