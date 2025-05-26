const background = document.querySelector(".background")
const body = document.querySelector("#body")

function open_popup() {
    if(background) {
        background.style.display = "flex"
        body.style.overflow = "hidden"
        background.style.top = window.scrollY + "px"
    }
}

function close_popup() {
    if(background) {
        background.style.display = "none"
        body.style.overflow = "auto"
    }
}

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

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
