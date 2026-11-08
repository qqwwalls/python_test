const menu = document.querySelector("#cv-menu");

menu.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener("click", () => {
        if (menu.classList.contains("show") && window.bootstrap) {
            bootstrap.Collapse.getOrCreateInstance(menu, {toggle: false}).hide();
        }
    });
});
