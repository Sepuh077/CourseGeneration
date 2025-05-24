$(document).ready(function() {
    let parts = window.location.href.split('/')
    const roomName = parts[parts.length - 2]
    const typingSpeed = 40;
    const element_rotate_loading_class = "element-rotate-loading"
    const disabled = "disabled"

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

        let index = data.slide
        let cnt = document.querySelectorAll('.slide-text')[index]
        
        let text = data.message
        
        if(text) {
            let textarea = cnt.querySelector(".slide-textarea")

            type_characters(textarea, text)
        }
        show_generate_info(cnt, data.skip, data.error)
        show_regenerate_button(cnt)
    };

    function hide_generate_infos(element) {
        element.querySelectorAll('.slide-generation-info').forEach(e => {
            e.style.display = "none"
        })
    }

    function show_generate_info(element, skip=false, error=false) {
        hide_generate_infos(element)
        if(error) {
            element.querySelector('.generate-error').style.display = "block"
        }
        else if(skip) {
            element.querySelector('.generate-skip').style.display = "block"
        }
        else {
            element.querySelector('.generate-done').style.display = "block"
        }
    }

    const CHARACTERS_MAX_COUNT = 800

    document.querySelectorAll('.slide-text').forEach((element, index) => {
        $(element.querySelector('.regenerate-btn')).on('click', function() {
            let btn = this
            let icon = btn.querySelector('i')
            hide_generate_infos(element)
            btn.classList.add(disabled)
            icon.classList.add(element_rotate_loading_class)

            $.ajax({
                method: "POST",
                type: "POST",
                url: `regenerate-text-${index}/`,
                data: {
                    "csrfmiddlewaretoken": CSRF,
                },
                success: function(response) {
                    type_characters(element.querySelector("textarea"), response.text)
                    show_generate_info(element, false, false)
                },
                error: function(response) {
                    show_generate_info(element, false, true)
                },
                complete: function() {
                    btn.classList.remove(disabled)
                    icon.classList.remove(element_rotate_loading_class)
                }
            })
        })
    });

    function show_regenerate_button(element) {
        let regenerate_btn = element.querySelector('.regenerate-btn')
        regenerate_btn.style.display = "block"
    }

    function set_element_character_count(element) {
        let text = element.querySelector("textarea").value

        element.querySelector(".characters-count").textContent = text.length
        element.querySelector(".characters-max-count").textContent = CHARACTERS_MAX_COUNT

        if(text.length > 0) {
            show_regenerate_button(element)
        }
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
        this.classList.add(disabled)
        $.ajax({
            method: "POST",
            type: "POST",
            url: "generate-texts/",
            data: {
                "csrfmiddlewaretoken": CSRF,
                "data": JSON.stringify(get_texts())
            },
            complete: function() {
                // location.reload();
                $('.second-step-buttons').show()
                $(this).hide()
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
