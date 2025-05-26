$(document).ready(function() {
    $("#reset-password").on("click", function() {
        let password1 = document.getElementById("new-password").value
        let password2 = document.getElementById("new-password-2").value
        if(password1 == password2) {
            const urlParams = new URLSearchParams(window.location.search);
            const uid = urlParams.get("uid");
            const token = urlParams.get("token");
            $.ajax({
                method: "POST",
                type: "POST",
                url: "/user/api/password-reset-confirm/",
                data: {
                    "new_password": password1,
                    "uid": uid,
                    "token": token
                },
                dataType: "application/json",
                complete: function(response) {
                    if(response.status == 200) {
                        window.location.href = "/user/login/"
                    }
                }
            })
        }
    })
})