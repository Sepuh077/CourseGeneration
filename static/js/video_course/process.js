$(document).ready(function() {
    const selected_voice = document.getElementById("selected-voice")
    const selected_audio_avatar_bg = document.getElementById("selected-voice-img-bg")
    const selected_audio_avatar = document.getElementById("selected-voice-img-cnt")
    const selected_audio_play_icon = selected_audio_avatar_bg.querySelector("i")
    const generate_texts = document.getElementById("generate-texts")
    const voices_cnt = document.getElementById("voices")
    const voices_dropdown = document.getElementById("voices-dropdown")
    const generate_video_loading_cnt = document.getElementById("generate-video-loading-cnt")
    const draft_saved_msg = $('#draft-saved')
    const draft_not_saved_msg = $('#draft-not-saved')
    let parts = window.location.href.split('/')
    const roomName = parts[parts.length - 2]
    const typingSpeed = 15;
    const element_rotate_loading_class = "element-rotate-loading"
    const disabled = "disabled"
    let start_generation = false
    let sent_msg = false

    let audio

    // const chatSocket = new WebSocket(
    //     'ws://'
    //     + window.location.host
    //     + '/ws/process/'
    //     + roomName
    //     + '/'
    // );

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

    // chatSocket.onmessage = function(e) {
    //     const data = JSON.parse(e.data)

    //     let index = data.slide
    //     let cnt = document.querySelectorAll('.slide-text')[index]
        
    //     let text = data.message
        
    //     if(text) {
    //         let textarea = cnt.querySelector(".slide-textarea")

    //         type_characters(textarea, text)
    //     }
    //     show_generate_info(cnt, data.skip, data.error)
    //     show_regenerate_button(cnt)
    //     sent_msg = true
    // };

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

    function regenerate_text(index, force = true, for_all = false) {
        let element = document.querySelectorAll('.slide-text')[index]
        if(!element) {
            generate_texts.classList.remove(disabled)
            return
        }
        generate_texts.classList.add(disabled)
        let btn = element.querySelector('.regenerate-btn')
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
                "force": force,
                "data": (for_all && index == 0) ? JSON.stringify(get_texts()) : "[]"
            },
            success: function(response) {
                let skipped = response.skipped
                if(!skipped) {
                    type_characters(element.querySelector("textarea"), response.text)
                }
                show_generate_info(element, skipped, false)
                if(for_all) {
                    regenerate_text(index + 1, force, for_all)
                }
                else {
                    generate_texts.classList.remove(disabled)
                }
            },
            error: function(response) {
                show_generate_info(element, false, true)
                generate_texts.classList.remove(disabled)
            },
            complete: function() {
                btn.classList.remove(disabled)
                icon.classList.remove(element_rotate_loading_class)
            }
        })
    }

    document.querySelectorAll('.slide-text').forEach((element, index) => {
        $(element.querySelector('.regenerate-btn')).on('click', function() {
            regenerate_text(index, true)
        })
    });

    generate_texts.onclick = function() {
        regenerate_text(0, false, true)
    }

    // function show_regenerate_button(element) {
    //     let regenerate_btn = element.querySelector('.regenerate-btn')
    //     regenerate_btn.style.display = "block"
    // }

    function set_element_character_count(element) {
        let text = element.querySelector("textarea").value

        element.querySelector(".characters-count").textContent = text.length
        element.querySelector(".characters-max-count").textContent = CHARACTERS_MAX_COUNT

        // if(text.length > 0) {
        //     show_regenerate_button(element)
        // }
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

    // $('#generate-texts').on('click', function() {
    //     start_generation = true
    //     sent_msg = false
    //     this.classList.add(disabled)
    //     let element = this
    //     $.ajax({
    //         method: "POST",
    //         type: "POST",
    //         url: "generate-texts/",
    //         data: {
    //             "csrfmiddlewaretoken": CSRF,
    //             "data": JSON.stringify(get_texts())
    //         },
    //         success: function() {
    //             $('.second-step-buttons').show()
    //             $(element).hide()
    //             if(!sent_msg) {
    //                 location.reload()
    //             }
    //         },
    //         error: function() {

    //         },
    //         complete: function() {
    //             element.classList.remove(disabled)
    //         }
    //     })
    // })

    $('#generate-video').on('click', function() {
        let btn = this
        btn.classList.add(disabled)
        let voice_id = selected_voice.getAttribute("data-id")
        generate_video_loading_cnt.style.display = "block"
        generate_video_loading_cnt.querySelector(".generate-video-loading-bar").classList.add("start-loading")
        $.ajax({
            method: "POST",
            type: "POST",
            url: "generate-video/",
            data: {
                "csrfmiddlewaretoken": CSRF,
                "data": JSON.stringify(get_texts()),
                "voice_id": voice_id
            },
            success: function(response) {
                if(response.link) {
                    window.location.href = response.link
                }
            },
            error: function() {
                let err = document.getElementById("generate-video-error")
                err.style.display = "flex"
                setTimeout(() => {
                    err.style.display = "none"
                }, 5000);
            },
            complete: function() {
                btn.classList.remove(disabled)
                generate_video_loading_cnt.style.display = "none"
                generate_video_loading_cnt.querySelector(".generate-video-loading-bar").classList.remove("start-loading")
            }
        })
    })

    $('#update-texts').on('click', function() {
        let element = this;
        element.classList.add(disabled)
        $.ajax({
            method: "POST",
            type: "POST",
            url: "update-texts/",
            data: {
                "csrfmiddlewaretoken": CSRF,
                "data": JSON.stringify(get_texts())
            },
            success: function() {
                draft_saved_msg.fadeIn(200).delay(1000).fadeOut(200)
            },
            error: function() {
                draft_not_saved_msg.fadeIn(200).delay(1000).fadeOut(200)
            },
            complete: function() {
                element.classList.remove(disabled)
            }
        })
    })

    $("#choose-voice").on("click", function() {
        let texts = get_texts()
        for(let i = 0; i < texts.length; ++i) {
            if(texts[i].trim()) {
                open_popup()
                return
            }
        }
    })
    $('.close-popup-icon').on("click", close_popup)

    function get_texts() {
        return Array.from(document.querySelectorAll('.slides .slide textarea')).map(textarea => textarea.value)
    }

    function load_voices() {
        $.ajax({
            method: "GET",
            type: "GET",
            url: "/get-voices/",
            success: function(response) {
                response.voices.forEach((voice, index) => {
                    let button = document.createElement('button')
                    button.className = 'voice'
                    button.dataset.id = voice.id

                    let img = document.createElement('img')
                    img.src = voice.avatar
                    img.loading = 'lazy'

                    let nameDiv = document.createElement('div')
                    nameDiv.className = 'voice-name'
                    nameDiv.textContent = voice.name

                    button.appendChild(img)
                    button.appendChild(nameDiv)
                    voices_cnt.appendChild(button)

                    if(index == 0) {
                        select_voice(button)
                    }
                })

            }
        })
    }

    load_voices()

    function select_voice(element) {
        let voice_cnt = selected_voice
        voice_cnt.setAttribute("data-id", element.getAttribute("data-id"))
        voice_cnt.querySelector("img").src = element.querySelector("img").src

        let name = element.querySelector(".voice-name").textContent.trim()
        voice_cnt.querySelector(".selected-voice-name").textContent = name

        stop_audio()

        audio = new Audio(`/static/voices/${name}.wav`)

        audio.onerror = function(e) {
            console.error('Audio load error');
        };

        audio.addEventListener('ended', function () {
            selected_audio_play_icon.classList.remove("fa-pause")
            selected_audio_play_icon.classList.add("fa-play")
        });
    }

    function stop_audio() {
        if(audio && !audio.paused) {
            audio.pause()
            selected_audio_play_icon.classList.remove("fa-pause")
            selected_audio_play_icon.classList.add("fa-play")
        }
    }

    $(".selected-voice-img-cnt").on("click", function() {
        if(audio) {
            if (!audio.paused) {
                audio.pause();
                selected_audio_play_icon.classList.remove("fa-pause")
                selected_audio_play_icon.classList.add("fa-play")
            } else {
                audio.play().then(() => {
                    selected_audio_play_icon.classList.add("fa-pause")
                    selected_audio_play_icon.classList.remove("fa-play")
                }).catch(err => {
                    console.error("Play error:", err);
                });
            }
        }
    })

    selected_audio_avatar.addEventListener('mouseover', function () {
        selected_audio_avatar_bg.style.display = 'flex'
    });

    selected_audio_avatar.addEventListener('mouseout', function () {
        selected_audio_avatar_bg.style.display = 'none'
    });

    voices_dropdown.onclick = function() {
        if($(voices_cnt).is(":hidden")) {
            voices_cnt.style.display = "flex"
            voices_dropdown.classList.add("rotate_90deg")
        }
        else {
            voices_cnt.style.display = "none"
            voices_dropdown.classList.remove("rotate_90deg")
        }
    }

    $(document).on("click", ".voice", function() {
        select_voice(this)
        voices_cnt.style.display = "none"
        voices_dropdown.classList.remove("rotate_90deg")
    })

})
