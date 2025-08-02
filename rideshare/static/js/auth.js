// Authentication utilities

// Get user type from localStorage
function getUserType() {
    return localStorage.getItem('user_type');
}

// Get user email from localStorage
function getUserEmail() {
    return localStorage.getItem('user_email');
}

// Redirect to appropriate dashboard based on user type
function redirectToDashboard() {
    const userType = getUserType();
    if (userType === 'DRIVER') {
        window.location.href = '/driver-dashboard/';
    } else {
        window.location.href = '/dashboard/';
    }
}

// Check if user is authenticated
function isAuthenticated() {
    // First check localStorage
    let token = localStorage.getItem('access_token');
    
    // If not in localStorage, check cookies
    if (!token) {
        token = getCookie('access_token');
    }
    
    if (!token) return false;
    
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        return payload.exp > Date.now() / 1000;
    } catch (error) {
        console.error('Error checking token:', error);
        return false;
    }
}

// Get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Make authenticated API request
async function makeAuthenticatedRequest(url, options = {}) {
    const token = localStorage.getItem('access_token');
    
    if (!token) {
        throw new Error('No authentication token found');
    }
    
    const defaultOptions = {
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    };
    
    const mergedOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...options.headers
        }
    };
    
    try {
        const response = await fetch(url, mergedOptions);
        
        if (response.status === 401) {
            // Token might be expired, try to refresh
            const refreshed = await refreshToken();
            if (refreshed) {
                // Retry the request with new token
                mergedOptions.headers['Authorization'] = `Bearer ${localStorage.getItem('access_token')}`;
                return await fetch(url, mergedOptions);
            } else {
                // Refresh failed, redirect to login
                logout();
                return response;
            }
        }
        
        return response;
    } catch (error) {
        console.error('API request error:', error);
        throw error;
    }
}

// Refresh authentication token
async function refreshToken() {
    const refreshTokenValue = localStorage.getItem('refresh_token');
    
    if (!refreshTokenValue) {
        return false;
    }
    
    try {
        const response = await fetch('/api/token/refresh/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                refresh: refreshTokenValue
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('access_token', data.access);
            if (data.refresh) {
                localStorage.setItem('refresh_token', data.refresh);
            }
            return true;
        } else {
            return false;
        }
    } catch (error) {
        console.error('Token refresh error:', error);
        return false;
    }
}

// Logout user
async function logout() {
    const refreshTokenValue = localStorage.getItem('refresh_token');
    
    try {
        if (refreshTokenValue) {
            await fetch('/auth/logout/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    refresh: refreshTokenValue
                })
            });
        }
    } catch (error) {
        console.error('Logout error:', error);
    } finally {
        // Clear local storage
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user_email');
        localStorage.removeItem('user_type');
        localStorage.removeItem('user_id');
        
        // Redirect to home page
        window.location.href = '/';
    }
}

// Get user profile
async function getUserProfile() {
    try {
        const response = await makeAuthenticatedRequest('/profile/');
        if (response.ok) {
            const userData = await response.json();
            // Store user type for UI decisions
            localStorage.setItem('user_type', userData.user_type);
            localStorage.setItem('user_id', userData.id);
            return userData;
        }
        return null;
    } catch (error) {
        console.error('Error fetching user profile:', error);
        return null;
    }
}

// Update navigation based on authentication status
function updateNavigation() {
    const isAuth = isAuthenticated();
    const loginNav = document.getElementById('nav-login');
    const registerNav = document.getElementById('nav-register');
    const userMenuNav = document.getElementById('nav-user-menu');
    const usernameSpan = document.getElementById('nav-username');
    const driverMenuItem = document.getElementById('driver-menu-item');
    
    if (isAuth) {
        // Hide guest links
        if (loginNav) loginNav.style.display = 'none';
        if (registerNav) registerNav.style.display = 'none';
        
        // Show user menu
        if (userMenuNav) {
            userMenuNav.classList.remove('d-none');
            
            // Set username
            const userEmail = localStorage.getItem('user_email');
            if (usernameSpan && userEmail) {
                usernameSpan.textContent = userEmail.split('@')[0];
            }
            
            // Show driver menu item for drivers
            const userType = localStorage.getItem('user_type');
            if (driverMenuItem && userType === 'DRIVER') {
                driverMenuItem.classList.remove('d-none');
            }
        }
    } else {
        // Show guest links
        if (loginNav) loginNav.style.display = 'block';
        if (registerNav) registerNav.style.display = 'block';
        
        // Hide user menu
        if (userMenuNav) userMenuNav.classList.add('d-none');
    }
}

// Initialize authentication state on page load
document.addEventListener('DOMContentLoaded', function() {
    updateNavigation();
    
    // If user is authenticated, fetch and store profile data
    if (isAuthenticated()) {
        getUserProfile();
    }
});

// Auto-refresh token before expiration
setInterval(async function() {
    if (isAuthenticated()) {
        const token = localStorage.getItem('access_token');
        if (token) {
            try {
                const payload = JSON.parse(atob(token.split('.')[1]));
                const timeUntilExpiry = payload.exp - (Date.now() / 1000);
                
                // Refresh token if it expires in less than 5 minutes
                if (timeUntilExpiry < 300) {
                    await refreshToken();
                }
            } catch (error) {
                console.error('Error checking token expiration:', error);
            }
        }
    }
}, 60000); // Check every minute
