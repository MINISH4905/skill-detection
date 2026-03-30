document.addEventListener("DOMContentLoaded", function () {

    const password1 = document.getElementById("id_password1");
    const password2 = document.getElementById("id_password2");

    if (password1 && password2) {
        password2.addEventListener("input", function () {
            if (password1.value !== password2.value) {
                password2.style.borderColor = "red";
            } else {
                password2.style.borderColor = "green";
            }
        });
    }

});