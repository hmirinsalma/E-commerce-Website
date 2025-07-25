// animations.js - Add this file to your static/js directory

document.addEventListener('DOMContentLoaded', function() {
    // Initialize animations
    initScrollReveal();
    initHoverAnimations();
    initAddToCartAnimation();
    initBrandSlider();
    initProductImageZoom();
    initCountdownAnimation();
    initNotificationAnimation();
});

// Scroll Reveal Animation
function initScrollReveal() {
    const revealElements = document.querySelectorAll('.reveal');
    
    function checkReveal() {
        for (let i = 0; i < revealElements.length; i++) {
            const windowHeight = window.innerHeight;
            const elementTop = revealElements[i].getBoundingClientRect().top;
            const elementVisible = 150;
            
            if (elementTop < windowHeight - elementVisible) {
                revealElements[i].classList.add('active');
            }
        }
    }
    
    window.addEventListener('scroll', checkReveal);
    // Check on initial load
    checkReveal();
}

// Hover Animations for Product Cards
function initHoverAnimations() {
    const productCards = document.querySelectorAll('.product-card');
    
    productCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            const image = this.querySelector('.card-img-top');
            if (image && !image.classList.contains('grayscale')) {
                image.classList.add('scale-in');
                setTimeout(() => {
                    image.classList.remove('scale-in');
                }, 500);
            }
        });
    });
}

// Add to Cart Animation
function initAddToCartAnimation() {
    // Store original ajouterAuPanier function if it exists
    const originalAjouterAuPanier = window.ajouterAuPanier;
    
    // Override with animated version
    window.ajouterAuPanier = function(produitId) {
        // Find the button that was clicked
        const buttons = document.querySelectorAll(`button[onclick="ajouterAuPanier('${produitId}')"]`);
        
        if (buttons.length > 0) {
            const button = buttons[0];
            button.classList.add('add-to-cart-animation');
            
            setTimeout(() => {
                button.classList.remove('add-to-cart-animation');
            }, 500);
        }
        
        // Call the original function
        if (originalAjouterAuPanier) {
            originalAjouterAuPanier(produitId);
        }
    };
}

// Animated Brand Slider
function initBrandSlider() {
    const brandsSlider = document.querySelector('.brands-slider');
    if (!brandsSlider) return;
    
    // Make the animation smoother
    brandsSlider.style.animationTimingFunction = 'linear';
    
    // Pause animation on hover
    brandsSlider.addEventListener('mouseenter', function() {
        this.style.animationPlayState = 'paused';
    });
    
    brandsSlider.addEventListener('mouseleave', function() {
        this.style.animationPlayState = 'running';
    });
    
    // Add hover effect to individual brand items
    const brandItems = document.querySelectorAll('.brand-item');
    brandItems.forEach(item => {
        item.classList.add('hover-lift');
    });
}

// Product Image Zoom on Hover
function initProductImageZoom() {
    const productImages = document.querySelectorAll('.product-card .card-img-top:not(.grayscale)');
    
    productImages.forEach(image => {
        image.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1)';
            this.style.transition = 'transform 0.5s ease';
        });
        
        image.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
}

// Animated Countdown Timer
function initCountdownAnimation() {
    const countdown = document.getElementById('countdown');
    if (!countdown) return;
    
    // Add pulse animation to countdown
    countdown.classList.add('attention');
}

// Notification Animation Enhancement
function initNotificationAnimation() {
    // Store original showNotification function if it exists
    const originalShowNotification = window.showNotification;
    
    // Override with enhanced animated version
    window.showNotification = function(message) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = 'notification';
        notification.textContent = message;
        
        // Add extra animation classes
        notification.classList.add('slide-in-right');
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        setTimeout(() => {
            notification.classList.remove('show');
            notification.classList.add('slide-in-right');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    };
}

// Animated Add to Cart Button
function animateAddToCart(button) {
    // Create a small circle element
    const circle = document.createElement('div');
    circle.style.position = 'absolute';
    circle.style.width = '20px';
    circle.style.height = '20px';
    circle.style.borderRadius = '50%';
    circle.style.backgroundColor = '#d23f72';
    circle.style.zIndex = '1000';
    
    // Get button position
    const buttonRect = button.getBoundingClientRect();
    circle.style.top = buttonRect.top + 'px';
    circle.style.left = buttonRect.left + 'px';
    
    // Append to body
    document.body.appendChild(circle);
    
    // Get cart icon position
    const cartIcon = document.querySelector('.cart-toggle-btn');
    const cartRect = cartIcon.getBoundingClientRect();
    
    // Animate circle to cart
    circle.style.transition = 'all 0.8s ease-in-out';
    circle.style.top = cartRect.top + 'px';
    circle.style.left = cartRect.left + 'px';
    circle.style.opacity = '0';
    circle.style.transform = 'scale(0.5)';
    
    // Remove circle after animation
    setTimeout(() => {
        document.body.removeChild(circle);
    }, 800);
    
    // Animate cart icon
    cartIcon.classList.add('bounce');
    setTimeout(() => {
        cartIcon.classList.remove('bounce');
    }, 1000);
}
// Add this to your animations.js file or create a new file called cart-animations.js

document.addEventListener('DOMContentLoaded', function() {
    // Override the ajouterAuPanier function to add visual feedback
    const originalAjouterAuPanier = window.ajouterAuPanier;
    
    window.ajouterAuPanier = function(produitId) {
        // Find the button that was clicked
        const buttons = document.querySelectorAll(`button[onclick="ajouterAuPanier('${produitId}')"]`);
        
        if (buttons.length > 0) {
            const button = buttons[0];
            
            // Create flying element animation
            const productCard = button.closest('.product-card');
            if (productCard) {
                const productImage = productCard.querySelector('.card-img-top');
                if (productImage) {
                    createFlyingElement(productImage, button);
                }
            }
            
            // Add pulse animation to button
            button.classList.add('add-to-cart-animation');
            setTimeout(() => {
                button.classList.remove('add-to-cart-animation');
            }, 500);
        }
        
        // Call the original function
        if (originalAjouterAuPanier) {
            return originalAjouterAuPanier(produitId);
        }
    };
    
    // Function to create flying element animation
    function createFlyingElement(sourceImage, button) {
        // Create a clone of the image
        const flyingImage = document.createElement('img');
        flyingImage.src = sourceImage.src;
        flyingImage.style.position = 'fixed';
        flyingImage.style.zIndex = '9999';
        flyingImage.style.width = '50px';
        flyingImage.style.height = '50px';
        flyingImage.style.objectFit = 'cover';
        flyingImage.style.borderRadius = '50%';
        flyingImage.style.boxShadow = '0 5px 15px rgba(0,0,0,0.1)';
        
        // Get positions
        const buttonRect = button.getBoundingClientRect();
        flyingImage.style.top = buttonRect.top + 'px';
        flyingImage.style.left = buttonRect.left + 'px';
        
        // Add to body
        document.body.appendChild(flyingImage);
        
        // Get cart button position
        const cartButton = document.querySelector('.cart-toggle-btn');
        if (!cartButton) {
            document.body.removeChild(flyingImage);
            return;
        }
        
        const cartRect = cartButton.getBoundingClientRect();
        
        // Animate the flying image
        setTimeout(() => {
            flyingImage.style.transition = 'all 0.8s cubic-bezier(0.18, 0.89, 0.32, 1.28)';
            flyingImage.style.top = cartRect.top + 'px';
            flyingImage.style.left = cartRect.left + 'px';
            flyingImage.style.width = '20px';
            flyingImage.style.height = '20px';
            flyingImage.style.opacity = '0';
            
            // Animate cart button
            cartButton.classList.add('bounce');
            
            // Update cart count with animation
            setTimeout(() => {
                const cartCount = document.getElementById('cart-count');
                if (cartCount) {
                    cartCount.classList.add('pulse');
                    setTimeout(() => {
                        cartCount.classList.remove('pulse');
                    }, 1000);
                }
                
                // Remove flying image
                document.body.removeChild(flyingImage);
                
                // Remove bounce from cart
                setTimeout(() => {
                    cartButton.classList.remove('bounce');
                }, 1000);
            }, 800);
        }, 10);
    }
});
// Add this to your animations.js file

// Create spinner element
function createSpinner() {
    const spinnerOverlay = document.createElement('div');
    spinnerOverlay.className = 'spinner-overlay';
    
    const spinner = document.createElement('div');
    spinner.className = 'spinner';
    
    spinnerOverlay.appendChild(spinner);
    document.body.appendChild(spinnerOverlay);
    
    return spinnerOverlay;
}

// Show spinner
function showSpinner() {
    let spinnerOverlay = document.querySelector('.spinner-overlay');
    
    if (!spinnerOverlay) {
        spinnerOverlay = createSpinner();
    }
    
    setTimeout(() => {
        spinnerOverlay.classList.add('show');
    }, 10);
    
    return spinnerOverlay;
}

// Hide spinner
function hideSpinner() {
    const spinnerOverlay = document.querySelector('.spinner-overlay');
    
    if (spinnerOverlay) {
        spinnerOverlay.classList.remove('show');
        
        setTimeout(() => {
            if (spinnerOverlay.parentNode) {
                spinnerOverlay.parentNode.removeChild(spinnerOverlay);
            }
        }, 300);
    }
}

// Override fetch requests to show spinner
const originalFetch = window.fetch;
window.fetch = function() {
    const spinner = showSpinner();
    
    return originalFetch.apply(this, arguments)
        .then(response => {
            hideSpinner();
            return response;
        })
        .catch(error => {
            hideSpinner();
            throw error;
        });
};