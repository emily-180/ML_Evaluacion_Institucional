const firebaseConfig = {
    apiKey: "AIzaSyDqT-5T64l6EJqeaF63oqNRElOPKVLwY2o",
    authDomain: "cpa-ml.firebaseapp.com",
    projectId: "120459085809",
};

firebase.initializeApp(firebaseConfig);

function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    firebase.auth().setPersistence(firebase.auth.Auth.Persistence.SESSION)
        .then(() => {
            return firebase.auth().signInWithEmailAndPassword(email, password);
        })
        .then((userCredential) => {
            console.log("Usuário logado:", userCredential.user.email);
            window.location.href = "home";
        })
        .catch((error) => {
            console.error("Erro no login:", error.message);
        });

}

function showAlert(message, type = 'danger', timeout = 6000) {
    const container = document.getElementById('alert-container');
    const id = 'alert-' + Date.now();
    const html = `
    <div id="${id}" class="alert alert-${type} alert-dismissible fade show" role="alert">
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>`;
    container.insertAdjacentHTML('beforeend', html);
    if (timeout > 0) {
        setTimeout(() => {
            const el = document.getElementById(id);
            if (el) {
                const bsAlert = bootstrap.Alert.getOrCreateInstance(el);
                bsAlert.close();
            }
        }, timeout);
    }
}

function login() {
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    if (!email || !password) {
        return showAlert('Por favor, ingrese el correo electrónico y la contraseña.', 'warning');
    }

    firebase.auth().setPersistence(firebase.auth.Auth.Persistence.SESSION)
        .then(() => firebase.auth().signInWithEmailAndPassword(email, password))
        .then(() => window.location.href = "home")
        .catch((error) => {
            const messages = {
                'auth/user-not-found': 'Usuario no encontrado. Verifique el correo electrónico.',
                'auth/wrong-password': 'Contraseña incorrecta. Inténtelo nuevamente.',
                'auth/invalid-email': 'Correo electrónico no válido. Verifique el formato.',
                'auth/too-many-requests': 'Demasiados intentos. Espere y vuelva a intentarlo más tarde.'
            };
            showAlert(messages[error.code] || 'Error en el inicio de sesión. Verifique el correo electrónico y la contraseña.', 'danger');
        });
}


document.getElementById('sendResetBtn').addEventListener('click', () => {
    const email = document.getElementById('resetEmail').value.trim();
    if (!email) {
        const feedback = document.getElementById('resetFeedback');
        feedback.textContent = 'Por favor, escriba un correo electrónico válido';
        feedback.style.color = '#a31818';
        return;
    }
    const btn = document.getElementById('sendResetBtn');
    btn.disabled = true;
    btn.textContent = 'Enviando...';

    firebase.auth().sendPasswordResetEmail(email)
        .then(() => {
            showAlert('Correo de recuperación enviado! Verifique su bandeja de entrada.', 'success', 8000);
            const resetModalEl = document.getElementById('resetModal');
            const modal = bootstrap.Modal.getInstance(resetModalEl);
            if (modal) modal.hide();
        })
        .catch((error) => {
            let msg = 'No fue posible enviar el correo electrónico. Verifique la dirección.';
            if (error.code === 'auth/user-not-found') {
                msg = 'No se encontró ningún usuario con ese correo electrónico.';
            } else if (error.code === 'auth/invalid-email') {
                msg = 'Correo electrónico no válido. Verifique el formato.';
            } else {
                msg = error.message;
            }
            showAlert(msg, 'danger');
        })
        .finally(() => {
            btn.disabled = false;
            btn.textContent = 'Enviar correo';
        });
});
