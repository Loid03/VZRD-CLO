// ============================================
// VZRD - Main JavaScript File
// ============================================

// Global variables
let cart = JSON.parse(localStorage.getItem('vzrd_cart')) || [];
let isCartOpen = false;

// ============================================
// INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    updateCartCount();
    updateCartDisplay();
    setupEventListeners();
    setupSmoothScrolling();
    setupFormValidation();
    setupNewsletterForm();
    setupBackToTop();
    setupScrollAnimations();
    setupTypingEffect();
    setupCouponSystem();
    
    // Initialize AOS if available
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-in-out',
            once: true,
            offset: 50
        });
    }
    
    console.log('VZRD app initialized successfully');
}

// ============================================
// EVENT LISTENERS
// ============================================

function setupEventListeners() {
    // Navbar scroll effect
    window.addEventListener('scroll', handleNavbarScroll);
    
    // Cart close on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && isCartOpen) {
            toggleCart();
        }
    });
    
    // Responsive menu handling
    const navbarToggler = document.querySelector('.navbar-toggler');
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            const navbarCollapse = document.querySelector('.navbar-collapse');
            setTimeout(() => {
                if (navbarCollapse.classList.contains('show')) {
                    document.body.style.overflow = 'hidden';
                } else {
                    document.body.style.overflow = '';
                }
            }, 100);
        });
    }
    
    // Click outside to close mobile menu
    document.addEventListener('click', function(e) {
        const navbar = document.querySelector('.navbar');
        const navbarCollapse = document.querySelector('.navbar-collapse');
        
        if (navbarCollapse && navbarCollapse.classList.contains('show') && 
            !navbar.contains(e.target)) {
            const navbarToggler = document.querySelector('.navbar-toggler');
            if (navbarToggler) {
                navbarToggler.click();
            }
        }
    });
    
    // Setup mobile enhancements
    setupMobileNavigation();
    setupTouchEnhancements();
}

function handleNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(25, 27, 35, 0.98)';
        navbar.style.backdropFilter = 'blur(20px)';
    } else {
        navbar.style.background = 'rgba(25, 27, 35, 0.95)';
        navbar.style.backdropFilter = 'blur(20px)';
    }
}

function setupSmoothScrolling() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#' || href.length <= 1) return;
            
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                const headerOffset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ============================================
// CART FUNCTIONALITY
// ============================================

function toggleCart() {
    const cartSidebar = document.getElementById('cartSidebar');
    const cartOverlay = document.getElementById('cartOverlay');
    
    isCartOpen = !isCartOpen;
    
    if (isCartOpen) {
        cartSidebar.classList.add('open');
        cartOverlay.classList.add('open');
        document.body.style.overflow = 'hidden';
    } else {
        cartSidebar.classList.remove('open');
        cartOverlay.classList.remove('open');
        document.body.style.overflow = '';
    }
}

function addToCart(productId, productName, productPrice, productImage, size = 'M') {
    const existingItem = cart.find(item => 
        item.id === productId && item.size === size
    );
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: productId,
            name: productName,
            price: productPrice,
            image: productImage,
            size: size,
            quantity: 1
        });
    }
    
    localStorage.setItem('vzrd_cart', JSON.stringify(cart));
    updateCartCount();
    updateCartDisplay();
    
    // Show success message
    showNotification(`${productName} adicionado ao carrinho!`, 'success');
    
    // Animate cart icon
    animateCartIcon();
}

function removeFromCart(productId, size) {
    cart = cart.filter(item => !(item.id === productId && item.size === size));
    localStorage.setItem('vzrd_cart', JSON.stringify(cart));
    updateCartCount();
    updateCartDisplay();
}

function updateCartQuantity(productId, size, newQuantity) {
    const item = cart.find(item => item.id === productId && item.size === size);
    if (item) {
        if (newQuantity <= 0) {
            removeFromCart(productId, size);
        } else {
            item.quantity = newQuantity;
            localStorage.setItem('vzrd_cart', JSON.stringify(cart));
            updateCartCount();
            updateCartDisplay();
        }
    }
}

function updateCartCount() {
    const cartCount = document.getElementById('cartCount');
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    
    if (cartCount) {
        cartCount.textContent = totalItems;
        if (totalItems > 0) {
            cartCount.style.display = 'flex';
        } else {
            cartCount.style.display = 'none';
        }
    }
}

function updateCartDisplay() {
    const cartItems = document.getElementById('cartItems');
    const cartTotal = document.getElementById('cartTotal');
    
    if (!cartItems || !cartTotal) return;
    
    if (cart.length === 0) {
        cartItems.innerHTML = `
            <div class="empty-cart">
                <i class="fas fa-shopping-cart"></i>
                <p>Seu carrinho está vazio</p>
            </div>
        `;
        cartTotal.textContent = '0,00';
        return;
    }
    
    let total = 0;
    cartItems.innerHTML = cart.map(item => {
        const itemTotal = item.price * item.quantity;
        total += itemTotal;
        
        return `
            <div class="cart-item">
                <div class="cart-item-image">
                    <img src="${item.image}" alt="${item.name}">
                </div>
                <div class="cart-item-details">
                    <div class="cart-item-name">${item.name}</div>
                    <div class="cart-item-price">R$ ${item.price.toFixed(2)} (${item.size})</div>
                    <div class="cart-item-controls">
                        <button class="quantity-btn" onclick="updateCartQuantity(${item.id}, '${item.size}', ${item.quantity - 1})">
                            <i class="fas fa-minus"></i>
                        </button>
                        <input type="number" class="quantity-input" value="${item.quantity}" min="1" 
                               onchange="updateCartQuantity(${item.id}, '${item.size}', parseInt(this.value))">
                        <button class="quantity-btn" onclick="updateCartQuantity(${item.id}, '${item.size}', ${item.quantity + 1})">
                            <i class="fas fa-plus"></i>
                        </button>
                        <button class="remove-item" onclick="removeFromCart(${item.id}, '${item.size}')">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }).join('');
    
    cartTotal.textContent = total.toFixed(2);
}

function animateCartIcon() {
    const cartIcon = document.querySelector('.cart-icon');
    if (cartIcon) {
        cartIcon.style.transform = 'scale(1.2)';
        setTimeout(() => {
            cartIcon.style.transform = 'scale(1)';
        }, 200);
    }
}

function clearCart() {
    cart = [];
    localStorage.setItem('vzrd_cart', JSON.stringify(cart));
    updateCartCount();
    updateCartDisplay();
}

// ============================================
// WHATSAPP INTEGRATION
// ============================================

function buyNow(productId, productName, productPrice, size = 'M') {
    const message = `Olá! Tenho interesse em comprar:\n\n` +
                   `🛍️ Produto: ${productName}\n` +
                   `💰 Preço: R$ ${productPrice.toFixed(2)}\n` +
                   `📏 Tamanho: ${size}\n\n` +
                   `Gostaria de mais informações sobre pagamento e entrega.`;
    
    const whatsappUrl = `https://wa.me/5511916292538?text=${encodeURIComponent(message)}`;
    window.open(whatsappUrl, '_blank');
}

function checkout() {
    if (cart.length === 0) {
        showNotification('Seu carrinho está vazio!', 'warning');
        return;
    }
    
    // Close cart and redirect to checkout page
    toggleCart();
    window.location.href = '/checkout';
}

// ============================================
// NOTIFICATIONS
// ============================================

function showNotification(message, type = 'info', duration = 3000) {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.toast-notification');
    existingNotifications.forEach(notification => notification.remove());
    
    const notification = document.createElement('div');
    notification.className = `toast-notification alert alert-${type === 'success' ? 'success' : type === 'warning' ? 'warning' : 'info'} alert-dismissible fade show`;
    notification.style.cssText = `
        position: fixed;
        top: 90px;
        right: 20px;
        z-index: 1070;
        max-width: 300px;
        opacity: 0;
        transform: translateX(100%);
        transition: all 0.3s ease;
        border-radius: 0.5rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    `;
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.opacity = '1';
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Auto remove
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 300);
    }, duration);
}

// ============================================
// FORM HANDLING
// ============================================

function setupFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', validateField);
            input.addEventListener('input', function() {
                if (this.classList.contains('is-invalid') && this.checkValidity()) {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                }
            });
        });
    });
}

function validateField(event) {
    const field = event.target;
    if (field.checkValidity()) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
    } else {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
    }
}

function setupNewsletterForm() {
    const newsletterForms = document.querySelectorAll('.newsletter-form');
    
    newsletterForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const emailInput = form.querySelector('input[type="email"]');
            const email = emailInput.value.trim();
            
            if (email && isValidEmail(email)) {
                // In a real app, this would send to backend
                showNotification('Obrigado por se inscrever! Em breve você receberá nossas novidades.', 'success');
                emailInput.value = '';
            } else {
                showNotification('Por favor, insira um e-mail válido.', 'warning');
            }
        });
    });
}

function subscribeNewsletter(event) {
    event.preventDefault();
    
    const form = event.target;
    const emailInput = form.querySelector('input[type="email"]');
    const email = emailInput.value.trim();
    
    if (email && isValidEmail(email)) {
        showNotification('Obrigado por se inscrever! Em breve você receberá nossas novidades.', 'success');
        emailInput.value = '';
    } else {
        showNotification('Por favor, insira um e-mail válido.', 'warning');
    }
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

function formatPrice(price) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(price);
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// ============================================
// PERFORMANCE OPTIMIZATIONS
// ============================================

// Lazy loading for images
function setupLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
}

// Preload critical resources
function preloadCriticalResources() {
    const criticalImages = [
        '/static/assets/logo.svg'
    ];
    
    criticalImages.forEach(src => {
        const link = document.createElement('link');
        link.rel = 'preload';
        link.as = 'image';
        link.href = src;
        document.head.appendChild(link);
    });
}

// ============================================
// ERROR HANDLING
// ============================================

window.addEventListener('error', function(event) {
    console.error('JavaScript error:', event.error);
    // In production, you might want to send errors to a logging service
});

window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled promise rejection:', event.reason);
    // In production, you might want to send errors to a logging service
});

// ============================================
// ACCESSIBILITY IMPROVEMENTS
// ============================================

// Focus management for modal
function trapFocus(element) {
    const focusableElements = element.querySelectorAll(
        'a[href], button, textarea, input[type="text"], input[type="radio"], input[type="checkbox"], select'
    );
    
    const firstFocusableElement = focusableElements[0];
    const lastFocusableElement = focusableElements[focusableElements.length - 1];
    
    element.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            if (e.shiftKey) {
                if (document.activeElement === firstFocusableElement) {
                    lastFocusableElement.focus();
                    e.preventDefault();
                }
            } else {
                if (document.activeElement === lastFocusableElement) {
                    firstFocusableElement.focus();
                    e.preventDefault();
                }
            }
        }
    });
}

// ============================================
// ANALYTICS & TRACKING
// ============================================

function trackEvent(category, action, label = null, value = null) {
    // Google Analytics 4 tracking
    if (typeof gtag !== 'undefined') {
        gtag('event', action, {
            event_category: category,
            event_label: label,
            value: value
        });
    }
    
    // Console log for development
    console.log('Event tracked:', { category, action, label, value });
}

// Track cart interactions
function trackCartEvent(action, productName, productPrice) {
    trackEvent('ecommerce', action, productName, productPrice);
}

// Track form submissions
function trackFormSubmission(formName) {
    trackEvent('engagement', 'form_submit', formName);
}

// ============================================
// DEVELOPMENT HELPERS
// ============================================

// Only in development
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    // Debug mode
    window.VZRD_DEBUG = {
        cart: () => cart,
        clearCart: clearCart,
        showNotification: showNotification,
        trackEvent: trackEvent
    };
    
    console.log('VZRD Debug mode enabled. Access window.VZRD_DEBUG for helper functions.');
}

// ============================================
// EXPORT FOR MODULE SYSTEMS
// ============================================

// ============================================
// MOBILE ENHANCEMENTS
// ============================================

function setupMobileNavigation() {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        // Close menu when clicking nav links
        const navLinks = navbarCollapse.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth < 992) {
                    setTimeout(() => {
                        const backdrop = document.querySelector('.navbar-backdrop');
                        if (backdrop) backdrop.remove();
                        navbarCollapse.classList.remove('show');
                        navbarToggler.setAttribute('aria-expanded', 'false');
                        document.body.style.overflow = '';
                    }, 100);
                }
            });
        });
    }
}

function setupTouchEnhancements() {
    // Add touch feedback for buttons
    const buttons = document.querySelectorAll('.btn, .product-card');
    
    buttons.forEach(button => {
        button.addEventListener('touchstart', function() {
            this.style.transform = 'scale(0.98)';
            this.style.transition = 'transform 0.1s ease';
        }, { passive: true });
        
        button.addEventListener('touchend', function() {
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        }, { passive: true });
        
        button.addEventListener('touchcancel', function() {
            this.style.transform = '';
        }, { passive: true });
    });
    
    // Improve tap targets for mobile
    if (window.innerWidth <= 768) {
        const smallButtons = document.querySelectorAll('.btn-sm, .quantity-btn');
        smallButtons.forEach(btn => {
            btn.style.minHeight = '44px';
            btn.style.minWidth = '44px';
        });
    }
    
    // Smooth scroll behavior for mobile
    if ('scrollBehavior' in document.documentElement.style) {
        document.documentElement.style.scrollBehavior = 'smooth';
    }
}

// Product Navigation Functions
function goToProductDetail(productId) {
    window.location.href = `/produto/${productId}`;
}

// ============================================
// BACK TO TOP BUTTON
// ============================================

function setupBackToTop() {
    // Create back to top button
    const backToTopBtn = document.createElement('button');
    backToTopBtn.className = 'back-to-top';
    backToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTopBtn.setAttribute('aria-label', 'Voltar ao topo');
    document.body.appendChild(backToTopBtn);
    
    // Show/hide on scroll
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.classList.add('show');
        } else {
            backToTopBtn.classList.remove('show');
        }
    });
    
    // Smooth scroll to top
    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// ============================================
// SCROLL ANIMATIONS
// ============================================

function setupScrollAnimations() {
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    
    if (animateElements.length === 0) return;
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    animateElements.forEach(element => {
        observer.observe(element);
    });
}

// ============================================
// TYPING EFFECT
// ============================================

function setupTypingEffect() {
    const typingElements = document.querySelectorAll('.typing-text');
    
    typingElements.forEach(element => {
        const text = element.textContent;
        element.textContent = '';
        element.style.borderRight = '2px solid var(--purple-primary)';
        
        let i = 0;
        function typeWriter() {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            } else {
                // Blinking cursor
                setInterval(function() {
                    element.style.borderRight = element.style.borderRight === 'none' ? 
                        '2px solid var(--purple-primary)' : 'none';
                }, 500);
            }
        }
        
        // Start typing when element comes into view
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    setTimeout(typeWriter, 500);
                    observer.unobserve(entry.target);
                }
            });
        });
        
        observer.observe(element);
    });
}

// ============================================
// COUPON SYSTEM
// ============================================

let appliedCoupon = null;
const coupons = {
    'VZRD10': { discount: 0.10, description: '10% de desconto' },
    'WELCOME15': { discount: 0.15, description: '15% de desconto para novos clientes' },
    'STREETWEAR20': { discount: 0.20, description: '20% de desconto especial' }
};

function setupCouponSystem() {
    const couponBtn = document.getElementById('applyCouponBtn');
    const couponInput = document.getElementById('couponCode');
    
    if (couponBtn && couponInput) {
        couponBtn.addEventListener('click', applyCoupon);
        couponInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                applyCoupon();
            }
        });
    }
}

function applyCoupon() {
    const couponInput = document.getElementById('couponCode');
    const couponCode = couponInput.value.trim().toUpperCase();
    const messageDiv = document.getElementById('couponMessage');
    
    if (!couponCode) {
        showCouponMessage('Digite um código de cupom', 'error');
        return;
    }
    
    if (coupons[couponCode]) {
        appliedCoupon = coupons[couponCode];
        showCouponMessage(`Cupom aplicado! ${appliedCoupon.description}`, 'success');
        updateCartTotal();
        couponInput.disabled = true;
        document.getElementById('applyCouponBtn').textContent = 'Aplicado';
        document.getElementById('applyCouponBtn').disabled = true;
    } else {
        showCouponMessage('Cupom inválido ou expirado', 'error');
    }
}

function showCouponMessage(message, type) {
    const messageDiv = document.getElementById('couponMessage');
    if (messageDiv) {
        messageDiv.textContent = message;
        messageDiv.className = `coupon-${type}`;
        messageDiv.style.display = 'block';
        
        if (type === 'error') {
            setTimeout(() => {
                messageDiv.style.display = 'none';
            }, 3000);
        }
    }
}

function removeCoupon() {
    appliedCoupon = null;
    document.getElementById('couponCode').disabled = false;
    document.getElementById('couponCode').value = '';
    document.getElementById('applyCouponBtn').textContent = 'Aplicar';
    document.getElementById('applyCouponBtn').disabled = false;
    document.getElementById('couponMessage').style.display = 'none';
    updateCartTotal();
}

function updateCartTotal() {
    const subtotalElement = document.getElementById('cartSubtotal');
    const discountElement = document.getElementById('cartDiscount');
    const totalElement = document.getElementById('cartTotal');
    
    if (!subtotalElement || !totalElement) return;
    
    let subtotal = 0;
    cart.forEach(item => {
        subtotal += item.price * item.quantity;
    });
    
    let discount = 0;
    if (appliedCoupon) {
        discount = subtotal * appliedCoupon.discount;
    }
    
    const total = subtotal - discount;
    
    subtotalElement.textContent = formatPrice(subtotal);
    if (discountElement) {
        discountElement.textContent = discount > 0 ? '-' + formatPrice(discount) : formatPrice(0);
        discountElement.parentElement.style.display = discount > 0 ? 'flex' : 'none';
    }
    totalElement.textContent = formatPrice(total);
}

// For ES6 modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        addToCart,
        removeFromCart,
        updateCartQuantity,
        toggleCart,
        buyNow,
        checkout,
        showNotification
    };
}
