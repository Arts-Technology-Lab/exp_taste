var API_URL = "https://www.google.com/recaptcha/api/siteverify"
var SITE_KEY = "6Lc1948cAAAAAHdTlWNiEwfWGPWTJcT7ShZ_SAmB"
function enableSubmit(token) {
    console.log(token)
    submitButton = document.getElementById('submit-id-submit');
    submitButton.disabled = false;
}

function captchaExpired() {
    submitButton = document.getElementById('submit-id-submit');
    submitButton.disabled = true;
}
