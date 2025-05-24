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
                const name = button.getAttribute('data-name')
                tooltip.textContent = name
                tooltip.style.display = 'block'

                const rect = button.getBoundingClientRect()

                const tooltip_rect = tooltip.getBoundingClientRect()

                let tooltipWidth = tooltip_rect.width
                let tooltipHeight = tooltip_rect.height

                tooltip.style.left = rect.left + rect.width / 2 - tooltipWidth / 2 + 'px';
                tooltip.style.top = rect.top + window.scrollY - tooltipHeight - 4 + 'px';
            }, 1000)
        })

        button.addEventListener('mouseleave', () => {
            clearTimeout(timeoutId)
            tooltip.style.display = 'none'
        })
    });
})