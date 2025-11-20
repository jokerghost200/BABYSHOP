    // Masquer automatiquement les messages après 8 secondes
    setTimeout(function() {
        const alerts = document.querySelectorAll('.fade-message');
        alerts.forEach(alert => {
            alert.style.transition = 'opacity 1s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 1000); // supprime après disparition
        });
    }, 1000); // 8 secondes = 8000 ms
