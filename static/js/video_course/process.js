$(document).ready(function() {
    let parts = window.location.href.split('/')
    const roomName = parts[parts.length - 2]
    const typingSpeed = 40;

    const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/process/'
        + roomName
        + '/'
    );

    function type_characters(element, text) {
        let index = 0;
        element.value = ""
        function type_character() {
            if (index < text.length) {
                element.value += text[index];
                index++;
                set_element_character_count(element.parentNode)
                setTimeout(type_character, typingSpeed);
            }
        }
        type_character()
    }

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data)
        let text = data.message
        let index = data.slide

        let textarea = document.querySelectorAll(".slide-textarea")[index]

        type_characters(textarea, text)
    };

    const CHARACTERS_MAX_COUNT = 800

    document.querySelectorAll('.slide-text').forEach((element, index) => {
        $(element.querySelector('.regenerate-btn')).on('click', function() {
            element.classList.add("disabled")
            $.ajax({
                method: "POST",
                type: "POST",
                url: `regenerate-text-${index}/`,
                data: {
                    "csrfmiddlewaretoken": CSRF,
                },
                success: function(response) {
                    if(response.text) {
                        type_characters(element.querySelector("textarea"), response.text)
                    }
                    element.classList.remove("disabled")
                },
                error: function(response) {
                    element.classList.remove("disabled")
                }
            })
        })
    });

    function set_element_character_count(element) {
        let text = element.querySelector("textarea").value

        element.querySelector(".characters-count").textContent = text.length
        element.querySelector(".characters-max-count").textContent = CHARACTERS_MAX_COUNT
    }

    function set_all_character_counts() {
        document.querySelectorAll('.slide-text').forEach((element) => {
            set_element_character_count(element)
        });
    }

    set_all_character_counts()

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
                // location.reload();
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
                // location.reload();
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
                // location.reload();
            }
        })
    })

    function get_texts() {
        return Array.from(document.querySelectorAll('.slides .slide textarea')).map(textarea => textarea.value)
    }
})