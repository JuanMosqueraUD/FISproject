// Funciones para el sistema de autenticación

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const errorMessage = document.getElementById('error-message');
    const successMessage = document.getElementById('success-message');


    // Manejar el formulario de login
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        try {
            showMessage('Iniciando sesión...', 'info');
            
            const response = await fetch('/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                }),
                credentials: 'include' // Para incluir cookies
            });

            if (response.ok) {
                const data = await response.json();
                showMessage('¡Login exitoso! Redirigiendo...', 'success');
                
                // Esperar un momento para que el usuario vea el mensaje y luego redirigir
                setTimeout(() => {
                    window.location.href = data.redirect_url;
                }, 1000);
            } else {
                const errorData = await response.json();
                showMessage(errorData.detail || 'Error al iniciar sesión', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showMessage('Error de conexión. Intente nuevamente.', 'error');
        }
    });
});

function showRegisterForm() {
    const modal = new bootstrap.Modal(document.getElementById('registerModal'));
    modal.show();
}

async function submitRegister() {
    const username = document.getElementById('reg-username').value;
    const email = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;
    const isAdmin = document.getElementById('is-admin').checked;

    if (!username || !email || !password) {
        showMessage('Por favor complete todos los campos', 'error');
        return;
    }

    try {
        showMessage('Registrando usuario...', 'info');
        
        const response = await fetch('/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password,
                is_admin: isAdmin
            })
        });

        if (response.ok) {
            const userData = await response.json();
            showMessage(`¡Usuario ${userData.username} registrado exitosamente!`, 'success');
            
            // Cerrar modal y limpiar formulario
            const modal = bootstrap.Modal.getInstance(document.getElementById('registerModal'));
            modal.hide();
            document.getElementById('registerForm').reset();
            
            // Autocompletar el username en el login
            document.getElementById('username').value = userData.username;
        } else {
            const errorData = await response.json();
            showMessage(errorData.detail || 'Error al registrar usuario', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showMessage('Error de conexión. Intente nuevamente.', 'error');
    }
}

function showMessage(message, type) {
    const errorDiv = document.getElementById('error-message');
    const successDiv = document.getElementById('success-message');
    
    // Ocultar ambos mensajes primero
    errorDiv.classList.add('d-none');
    successDiv.classList.add('d-none');
    
    if (type === 'error') {
        errorDiv.textContent = message;
        errorDiv.classList.remove('d-none');
    } else if (type === 'success') {
        successDiv.textContent = message;
        successDiv.classList.remove('d-none');
    } else if (type === 'info') {
        successDiv.textContent = message;
        successDiv.classList.remove('d-none');
    }
    
    // Auto-ocultar después de 5 segundos
    setTimeout(() => {
        errorDiv.classList.add('d-none');
        successDiv.classList.add('d-none');
    }, 5000);
}

// Función para verificar si el usuario está autenticado
async function checkAuth() {
    try {
        const response = await fetch('/auth/me', {
            credentials: 'include'
        });
        
        if (response.ok) {
            const userData = await response.json();
            return userData;
        }
    } catch (error) {
        console.error('Error verificando autenticación:', error);
    }
    return null;
}

// Función para logout
async function logout() {
    try {
        const response = await fetch('/auth/logout', {
            method: 'POST',
            credentials: 'include'
        });
        
        if (response.ok) {
            const data = await response.json();
            window.location.href = data.redirect_url;
        } else {
            // En caso de error, redirigir de todas formas
            window.location.href = '/';
        }
    } catch (error) {
        console.error('Error cerrando sesión:', error);
        // En caso de error, redirigir de todas formas
        window.location.href = '/';
    }
}
