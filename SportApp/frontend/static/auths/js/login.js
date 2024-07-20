const form = document.querySelector("form");

form.addEventListener("submit", (event) => {
    const data1 = document.querySelector("#email");

    if (/^[a-zA-Z][a-zA-Z0-9]*@[a-z]+\.[a-z]+$/.test(data1.value)) {
        data1.style.cssText = "border: 1px solid #31965e";
        document.querySelector("#email_hint").style.cssText = "color: #31965e";
    } else {
        data1.style.cssText = "border: 1px solid #752e2e";
        document.querySelector("#email_hint").style.cssText = "color: #752e2e";
        event.preventDefault();
    }

    const data2 = document.querySelector("#password");

    if (/^[a-zA-Z0-9]{7,128}$/.test(data2.value)) {
        data2.style.border = "1px solid #31965e";
        document.querySelector("#password_hint_1").style.color = "#31965e";
    } else {
        data2.style.border = "1px solid #752e2e";
        document.querySelector("#password_hint_1").style.color = "#752e2e";
        event.preventDefault();
    }

    if (!/[a-zA-Z]/.test(data2.value) || !/[0-9]/.test(data2.value)) {
        data2.style.border = "1px solid #752e2e";
        document.querySelector("#password_hint_2").style.color = "#752e2e";
        event.preventDefault();
    } else {
        data2.style.border = "1px solid #31965e";
        document.querySelector("#password_hint_2").style.color = "#31965e";
    }
})
