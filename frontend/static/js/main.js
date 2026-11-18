document.addEventListener('DOMContentLoaded', function () {
    const body = document.body;
    const toggle = document.getElementById('sidebar-toggle');
    const overlay = document.getElementById('sidebar-overlay');
    const collapse = document.getElementById('sidebar-collapse');

    function closeMobileSidebar() {
        body.classList.remove('sidebar-open');
        if (toggle) toggle.setAttribute('aria-expanded', 'false');
    }

    if (toggle) {
        toggle.addEventListener('click', function () {
            const open = body.classList.toggle('sidebar-open');
            toggle.setAttribute('aria-expanded', String(open));
        });
    }

    if (overlay) overlay.addEventListener('click', closeMobileSidebar);

    if (collapse) {
        collapse.addEventListener('click', function () {
            body.classList.toggle('sidebar-collapsed');
        });
    }

    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') closeMobileSidebar();
    });

    window.addEventListener('resize', function () {
        if (window.innerWidth > 900) closeMobileSidebar();
    });
});
