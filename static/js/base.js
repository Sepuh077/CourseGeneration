$(document).ready(function() {
    const buttons = document.querySelectorAll('button')
    const tooltip = document.getElementById('tooltip')

    let timeoutId

    buttons.forEach(button => {
        if(!button.hasAttribute('data-name')) {
            return
        }
        button.addEventListener('mouseenter', (e) => {
            timeoutId = setTimeout(() => {
                const name = button.getAttribute('data-name');
                tooltip.textContent = name;

                const rect = button.getBoundingClientRect();
                tooltip.style.right = rect.left + 4 + 'px';
                tooltip.style.top = rect.top + window.scrollY + 'px';
                tooltip.style.display = 'block';
            }, 1000);
        });

        button.addEventListener('mouseleave', () => {
            clearTimeout(timeoutId);
            tooltip.style.display = 'none';
        });
    });
})