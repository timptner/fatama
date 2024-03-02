document.addEventListener('DOMContentLoaded', () => {

    const $navbar = document.getElementById('mainNavbar');
    const $navbarItems = $navbar.querySelectorAll('.navbar-item');

    $navbarItems.forEach(el => {
        if (document.URL.startsWith(el.href)) {
            el.classList.add('is-active');
        }
    });

});
