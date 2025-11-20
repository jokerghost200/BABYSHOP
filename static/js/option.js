document.addEventListener("DOMContentLoaded", () => {
    const cancelBtn = document.getElementById("cancelSettingsBtn");
    const form = document.getElementById("settingsForm");
    const inputs = Array.from(form.querySelectorAll("input, select"));
    const themeSwitch = document.getElementById("themeSwitch");
    const notifSwitch = document.getElementById("notifSwitch");

    // Sauvegarder l'état initial
    const initialValues = {};
    inputs.forEach(input => {
        if(input.type === "checkbox") initialValues[input.name] = input.checked;
        else initialValues[input.name] = input.value;
    });

    // Restaurer le thème sombre au chargement
    const savedTheme = localStorage.getItem("theme");
    if(savedTheme === "dark") {
        document.body.classList.add("dark");
        if(themeSwitch) themeSwitch.checked = true;
    }

    // Annuler les changements
    cancelBtn.addEventListener("click", () => {
        inputs.forEach(input => {
            if(input.type === "checkbox") input.checked = initialValues[input.name];
            else input.value = initialValues[input.name];
        });
        document.body.classList.toggle("dark", themeSwitch.checked);
        localStorage.setItem("theme", themeSwitch.checked ? "dark" : "light");

        const toast = document.createElement("div");
        toast.className = "notif-toast";
        toast.innerHTML = '<i class="fa-solid fa-rotate-left me-2"></i> Modifications annulées';
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 2000);
    });

    // Changer le thème sombre
    if(themeSwitch){
        themeSwitch.addEventListener("change", () => {
            const isDark = themeSwitch.checked;
            document.body.classList.toggle("dark", isDark);
            localStorage.setItem("theme", isDark ? "dark" : "light");

            const toast = document.createElement("div");
            toast.className = "theme-toast";
            toast.innerHTML = isDark
                ? '<i class="fa-solid fa-moon me-2"></i> Thème sombre activé'
                : '<i class="fa-solid fa-sun me-2"></i> Thème clair activé';
            document.body.appendChild(toast);
            setTimeout(() => toast.remove(), 2500);
        });
    }

    // Notifications
    if(notifSwitch){
        notifSwitch.addEventListener("change", () => {
            const toast = document.createElement("div");
            toast.className = "notif-toast";
            toast.innerHTML = notifSwitch.checked
                ? '<i class="fa-solid fa-bell me-2"></i> Notifications activées'
                : '<i class="fa-solid fa-bell-slash me-2"></i> Notifications désactivées';
            document.body.appendChild(toast);
            setTimeout(() => toast.remove(), 2500);
        });
    }

    // Animation des champs modifiés
    inputs.forEach(input => {
        input.addEventListener("change", () => {
            const item = input.closest(".setting-item");
            if(item){
                item.classList.add("modified");
                setTimeout(() => item.classList.remove("modified"), 1000);
            }
        });
    });
});
document.addEventListener('DOMContentLoaded', () => {
    const langSelect = document.getElementById('langSelect');
    
    if(langSelect) {
        langSelect.addEventListener('change', (e) => {
            const selectedLang = e.target.value;
    
            // Option 1 : Enregistrer la langue côté serveur via fetch
            fetch('/user/set-language/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Assure que csrf_token fonctionne
                },
                body: JSON.stringify({ langue: selectedLang })
            })
            .then(response => response.json())
            .then(data => {
                if(data.success) {
                    // Recharger la page pour appliquer la langue
                    location.reload();
                }
            })
            .catch(err => console.error('Erreur lors du changement de langue :', err));
    
            // Option 2 : Changer le texte côté client (si tu as un dictionnaire JS)
            // translatePage(selectedLang);
        });
    }
    
    // Fonction pour récupérer le CSRF token
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
    
    });
    