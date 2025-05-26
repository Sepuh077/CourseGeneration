function sendResetEmail() {
    const email = document.getElementById("reset-email").value;

    fetch("/user/api/password-reset/", {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": getCookie("csrftoken") },
        body: JSON.stringify({ email })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("reset-msg").textContent = data.message;
    });
}

document.getElementById("send-link").onclick = sendResetEmail