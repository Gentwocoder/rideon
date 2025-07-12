// Main JavaScript functionality for Rideon

// Show alert messages
function showAlert(message, type = 'info', duration = 5000) {
    const alertContainer = document.getElementById('alert-container');
    if (!alertContainer) return;
    
    const alertId = 'alert-' + Date.now();
    const alertHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert" id="${alertId}">
            <i class="fas fa-${getAlertIcon(type)} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    alertContainer.insertAdjacentHTML('beforeend', alertHTML);
    
    // Auto-dismiss after duration
    if (duration > 0) {
        setTimeout(() => {
            const alertElement = document.getElementById(alertId);
            if (alertElement) {
                const bsAlert = new bootstrap.Alert(alertElement);
                bsAlert.close();
            }
        }, duration);
    }
}

// Get appropriate icon for alert type
function getAlertIcon(type) {
    const icons = {
        'success': 'check-circle',
        'danger': 'exclamation-triangle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle',
        'primary': 'info-circle',
        'secondary': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Format ride status for display
function formatRideStatus(status) {
    const statusMap = {
        'pending': { text: 'Pending', class: 'status-pending' },
        'accepted': { text: 'Accepted', class: 'status-accepted' },
        'in_progress': { text: 'In Progress', class: 'status-in-progress' },
        'completed': { text: 'Completed', class: 'status-completed' },
        'cancelled': { text: 'Cancelled', class: 'status-cancelled' }
    };
    
    const statusInfo = statusMap[status] || { text: status, class: '' };
    return `<span class="${statusInfo.class}">${statusInfo.text}</span>`;
}

// Format currency
function formatCurrency(amount) {
    if (!amount) return 'N/A';
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Format distance
function formatDistance(distance) {
    if (!distance) return 'N/A';
    return `${distance} km`;
}

// Format duration
function formatDuration(minutes) {
    if (!minutes) return 'N/A';
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    
    if (hours > 0) {
        return `${hours}h ${mins}m`;
    }
    return `${mins}m`;
}

// Show loading overlay
function showLoading() {
    const loadingHTML = `
        <div class="loading-overlay" id="loading-overlay">
            <div class="loading-spinner"></div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', loadingHTML);
}

// Hide loading overlay
function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.remove();
    }
}

// Debounce function for search inputs
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

// Validate form fields
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
        }
    });
    
    return isValid;
}

// Clear form validation classes
function clearFormValidation(form) {
    const inputs = form.querySelectorAll('.is-valid, .is-invalid');
    inputs.forEach(input => {
        input.classList.remove('is-valid', 'is-invalid');
    });
}

// Get user location
function getUserLocation() {
    return new Promise((resolve, reject) => {
        if (!navigator.geolocation) {
            reject(new Error('Geolocation is not supported'));
            return;
        }
        
        navigator.geolocation.getCurrentPosition(
            position => {
                resolve({
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                });
            },
            error => {
                reject(error);
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 300000
            }
        );
    });
}

// Calculate distance between two points (Haversine formula)
function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Earth's radius in kilometers
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon/2) * Math.sin(dLon/2);
    
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    const distance = R * c;
    
    return Math.round(distance * 100) / 100; // Round to 2 decimal places
}

// Format phone number
function formatPhoneNumber(phone) {
    const cleaned = phone.replace(/\D/g, '');
    if (cleaned.length === 10) {
        return `(${cleaned.slice(0, 3)}) ${cleaned.slice(3, 6)}-${cleaned.slice(6)}`;
    }
    return phone;
}

// Copy text to clipboard
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showAlert('Copied to clipboard!', 'success', 2000);
    } catch (error) {
        console.error('Failed to copy:', error);
        showAlert('Failed to copy to clipboard', 'danger', 3000);
    }
}

// Handle network errors
function handleNetworkError(error) {
    console.error('Network error:', error);
    
    if (!navigator.onLine) {
        showAlert('You appear to be offline. Please check your internet connection.', 'warning');
    } else {
        showAlert('Network error occurred. Please try again.', 'danger');
    }
}

// Initialize tooltips and popovers
function initializeBootstrapComponents() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// Handle page visibility changes
document.addEventListener('visibilitychange', function() {
    if (!document.hidden && isAuthenticated()) {
        // Page became visible, refresh data if needed
        const lastRefresh = localStorage.getItem('last_data_refresh');
        const now = Date.now();
        
        if (!lastRefresh || (now - parseInt(lastRefresh)) > 300000) { // 5 minutes
            // Trigger data refresh
            const event = new CustomEvent('refreshData');
            document.dispatchEvent(event);
            localStorage.setItem('last_data_refresh', now.toString());
        }
    }
});

// Initialize on DOM content loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeBootstrapComponents();
    
    // Add fade-in animation to main content
    const main = document.querySelector('main');
    if (main) {
        main.classList.add('fade-in');
    }
    
    // Handle form submissions with loading states
    const forms = document.querySelectorAll('form[data-async]');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                const originalText = submitBtn.textContent;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
                
                // Re-enable after 10 seconds as fallback
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.textContent = originalText;
                }, 10000);
            }
        });
    });
});

// Handle browser back/forward navigation
window.addEventListener('popstate', function(e) {
    if (e.state && e.state.page) {
        // Handle SPA navigation if implemented
        console.log('Navigation to:', e.state.page);
    }
});

// Service Worker registration (for future PWA features)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/static/js/sw.js')
            .then(function(registration) {
                console.log('ServiceWorker registration successful');
            })
            .catch(function(error) {
                console.log('ServiceWorker registration failed');
            });
    });
}
