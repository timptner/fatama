document.addEventListener('DOMContentLoaded', () => {

    const $menu = document.getElementById('accountsMenu');
    const $navLinks = $menu.querySelectorAll('a');

    $navLinks.forEach(el => {
        if (document.URL === el.href) {
            el.classList.add('is-active');
        }
    });

});
