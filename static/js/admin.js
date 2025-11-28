const toggleBtn = document.getElementById("toggleSidebar");
const sidebar = document.querySelector(".sidebar");
const articlesLink = document.querySelector('[href="#submenuArticles"]'); // correction du nom

// === Toggle sidebar ===
toggleBtn.addEventListener("click", () => {
    if (window.innerWidth <= 992) {
        // Mode mobile : sidebar coulissante
        sidebar.classList.toggle("active");
        document.body.classList.toggle("sidebar-open");
    } else {
        // Mode desktop : sidebar pliable
        sidebar.classList.toggle("collapsed");

        // ✅ Si on replie la sidebar -> fermer tous les sous-menus ouverts
        if (sidebar.classList.contains("collapsed")) {
            document.querySelectorAll(".collapse.show").forEach(menu => {
                const collapse = bootstrap.Collapse.getInstance(menu);
                if (collapse) collapse.hide();
                else new bootstrap.Collapse(menu, { toggle: false }).hide();
            });
        }
    }
});

// === Fermer sidebar si clic à l’extérieur sur mobile ===
document.addEventListener("click", (e) => {
    if (window.innerWidth <= 992 && !sidebar.contains(e.target) && !toggleBtn.contains(e.target)) {
        sidebar.classList.remove("active");
        document.body.classList.remove("sidebar-open");
    }
});

// === Quand on clique sur "Articles" et que la sidebar est repliée ===
if (articlesLink) {
    articlesLink.addEventListener("click", (e) => {
        const isCollapsed = sidebar.classList.contains("collapsed");
        if (isCollapsed && window.innerWidth > 992) {
            e.preventDefault(); // Empêche le collapse immédiat
            sidebar.classList.remove("collapsed");

            // ✅ Après un petit délai, ouvre le sous-menu Articles
            setTimeout(() => {
                const submenu = new bootstrap.Collapse(document.getElementById("submenuArticles"), {
                    show: true
                });
            }, 300);
        }
    });
}
// === Sidebar hover desktop ===
if (window.innerWidth > 992) {
    sidebar.addEventListener("mouseenter", () => {
        sidebar.classList.add("expanded");
        sidebar.classList.remove("collapsed");
    });

    sidebar.addEventListener("mouseleave", () => {
        sidebar.classList.remove("expanded");
        sidebar.classList.add("collapsed");

        // fermer tous les sous-menus ouverts
        document.querySelectorAll(".collapse.show").forEach(menu => {
            const collapse = bootstrap.Collapse.getInstance(menu);
            if (collapse) collapse.hide();
            else new bootstrap.Collapse(menu, { toggle: false }).hide();
        });
    });
}
