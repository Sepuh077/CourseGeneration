$(document).ready(function() {
    const drop_area = document.getElementById('upload-document-container')
    const file_name_cnt = document.getElementById('file-upload-filename')
    const file_upload = document.getElementById('upload-document-input')

    if(drop_area) {
        function handle_file(files) {
            if (files.length > 0) {
                let file_name = files[0].name
                file_name_cnt.textContent = file_name
                $('.submit-slides-file').removeClass('disabled-button')
            }
        }

        file_upload.addEventListener('change', function () {
            handle_file(this.files)
        })

        $.each(['dragenter', 'dragover', 'dragleave', 'drop'], function(i, event) {
            drop_area.addEventListener(event, prevent_defaults, false)
            document.body.addEventListener(event, prevent_defaults, false)
        })

        $.each(['dragenter', 'dragover'], function(i, event) {
            drop_area.addEventListener(event, () => highlight(drop_area), false)
        })

        $.each(['dragleave', 'drop'], function(i, event) {
            drop_area.addEventListener(event, () => unhighlight(drop_area), false)
        })

        drop_area.addEventListener('drop', handle_drop, false)

        function handle_drop(e) {
            const dt = e.dataTransfer
            const files = dt.files

            handle_file(files)
            file_upload.files = files
        }

        function prevent_defaults(e) {
            e.preventDefault()
            e.stopPropagation()
        }

        function highlight(element) {
            element.classList.add('dragover')
        }

        function unhighlight(element) {
            element.classList.remove('dragover')
        }
    }
})