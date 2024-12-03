const scrollToTopBtn = document.getElementById("scrollToTop");

// Función para mostrar u ocultar el botón basado en scroll
window.addEventListener("scroll", () => {
    const isMobile = window.matchMedia("(max-width: 767px)").matches;

    if (window.scrollY > 300 && !isMobile) {
        scrollToTopBtn.style.display = "block";
    } else {
        scrollToTopBtn.style.display = "none";
    }
});

// Al hacer clic, subir suavemente
scrollToTopBtn.addEventListener("click", () => {
    window.scrollTo({
        top: 0,
        behavior: "smooth",
    });
});
