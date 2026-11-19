document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-toggle-new]').forEach(function (button) {
        const fieldName = button.getAttribute('data-toggle-new');
        const row = document.getElementById(fieldName + '_row');
        const input = document.getElementById('id_' + fieldName);
        if (!row || !input) return;

        button.addEventListener('click', function () {
            const isOpen = !row.hidden;
            row.hidden = isOpen;

            if (isOpen) {
                input.value = '';
                button.classList.remove('active');
                button.setAttribute('aria-expanded', 'false');
            } else {
                input.focus();
                button.classList.add('active');
                button.setAttribute('aria-expanded', 'true');
            }
        });
    });
});
