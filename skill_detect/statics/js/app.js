/* =====================================================
   EDUNET - Global App JavaScript
   Used across all templates via base.html
===================================================== */

document.addEventListener("DOMContentLoaded", () => {

    /* ===============================
       Set Current Date in Header
    =============================== */
    const dateElement = document.getElementById("current-date");

    if (dateElement) {
        const today = new Date();
        const options = {
            weekday: "short",
            day: "numeric",
            month: "short"
        };

        dateElement.textContent =
            today.toLocaleDateString("en-US", options);
    }


    /* ===============================
       Period Selector (Dashboard)
    =============================== */
    const periodSelect = document.getElementById("period-select");

    if (periodSelect) {
        periodSelect.addEventListener("change", function () {

            console.log("Period changed to:", this.value);

            // Future:
            // fetch(`/api/xp-data/?period=${this.value}`)
            //     .then(res => res.json())
            //     .then(updateChart);
        });
    }


    /* ===============================
       Auto Hide Alert Messages
    =============================== */
    const messages = document.querySelectorAll(".alert");

    messages.forEach((message) => {
        setTimeout(() => {
            message.style.transition = "opacity 0.5s";
            message.style.opacity = "0";

            setTimeout(() => {
                message.remove();
            }, 500);

        }, 5000);
    });


    /* ===============================
       Form Validation
    =============================== */
    const forms = document.querySelectorAll("form");

    forms.forEach((form) => {
        form.addEventListener("submit", (e) => {

            const requiredFields =
                form.querySelectorAll("[required]");

            let isValid = true;

            requiredFields.forEach((field) => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = "#E74C3C";
                } else {
                    field.style.borderColor = "";
                }
            });

            if (!isValid) {
                e.preventDefault();
                alert("Please fill in all required fields.");
            }
        });
    });

});


/* =====================================================
   Utility Functions (Global)
===================================================== */

/* Format Date */
function formatDate(date) {
    const options = {
        year: "numeric",
        month: "short",
        day: "numeric"
    };

    return new Date(date).toLocaleDateString("en-US", options);
}


/* Time Ago Formatter */
function timeAgo(date) {
    const seconds =
        Math.floor((new Date() - new Date(date)) / 1000);

    if (seconds < 60) return "just now";
    if (seconds < 3600) return Math.floor(seconds / 60) + "m ago";
    if (seconds < 86400) return Math.floor(seconds / 3600) + "h ago";
    if (seconds < 604800) return Math.floor(seconds / 86400) + "d ago";

    return formatDate(date);
}


/* =====================================================
   Django CSRF Helper (Needed for POST requests)
===================================================== */

function getCSRFToken() {
    return document.cookie
        .split("; ")
        .find(row => row.startsWith("csrftoken"))
        ?.split("=")[1];
}