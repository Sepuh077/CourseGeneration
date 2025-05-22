$(document).ready(function() {
    const CHARACTERS_MAX_COUNT = 800

    document.querySelectorAll('.slide-text').forEach((element, index) => {
        let text = element.querySelector("textarea").value

        element.querySelector(".characters-count").textContent = text.length
        element.querySelector(".characters-max-count").textContent = CHARACTERS_MAX_COUNT

        $(element.querySelector('.regenerate-btn')).on('click', function() {
            $.ajax({
                method: "POST",
                type: "POST",
                url: `regenerate-text-${index}/`,
                data: {
                    "csrfmiddlewaretoken": CSRF,
                },
                complete: function() {
                    location.reload();
                }
            })
        })
    });

    $("textarea").on("input", function() {
        if(this.value.length > CHARACTERS_MAX_COUNT) {
            this.value = this.value.slice(0, CHARACTERS_MAX_COUNT)
        }
        let text = this.value
        this.parentNode.querySelector(".characters-count").textContent = text.length
        this.parentNode.querySelector(".characters-max-count").textContent = CHARACTERS_MAX_COUNT
    })

    $('#generate-texts').on('click', function() {
        $.ajax({
            method: "POST",
            type: "POST",
            url: "generate-texts/",
            data: {
                "csrfmiddlewaretoken": CSRF
            },
            complete: function() {
                location.reload();
            }
        })
    })

    $('#generate-video').on('click', function() {
        $.ajax({
            method: "POST",
            type: "POST",
            url: "generate-video/",
            data: {
                "csrfmiddlewaretoken": CSRF,
                "data": JSON.stringify(get_texts())
            },
            complete: function() {
                location.reload();
            }
        })
    })

    $('#update-texts').on('click', function() {
        $.ajax({
            method: "POST",
            type: "POST",
            url: "update-texts/",
            data: {
                "csrfmiddlewaretoken": CSRF,
                "data": JSON.stringify(get_texts())
            },
            complete: function() {
                location.reload();
            }
        })
    })

    function get_texts() {
        return Array.from(document.querySelectorAll('.slides .slide textarea')).map(textarea => textarea.value)
    }
})