document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener("click", function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute("href")).scrollIntoView({
                behavior: "smooth"
            });
        });
    });

    setTimeout(function() {
        console.log("Deferred tasks executed.");
    }, 1000);

    // Removed dynamic title rotation.
});
