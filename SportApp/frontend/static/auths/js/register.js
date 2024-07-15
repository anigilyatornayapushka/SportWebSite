function randomRange(start, end) { // [start; end)
    let n = Math.floor(Math.random() * (end - start)) + start;
    return n;
}

function generateCaptcha(length) {
    let code = "";
    for (let i = 0; i < length; ++i) {
        let symbol = "abcdefhijklmnopqrstuvwxyz123456789"[randomRange(0, 34)]
        if (randomRange(0, 2)) code += symbol;
        else code += symbol.toUpperCase();
    }
    return code;
}

document.querySelector(".captcha-example").textContent = generateCaptcha(6);

const form = document.querySelector("form");

form.addEventListener("submit", (event) => {
    let have_error = false;
    if (checkFirstName() == true) have_error = true;
    if (checkLastName() == true) have_error = true;
    if (checkEmail() == true) have_error = true;
    if (checkPassword() == true) have_error = true;
    if (checkRepeatPassword() == true) have_error = true;
    if (checkCaptcha() == true) have_error = true;

    if (have_error == true) event.preventDefault();
});

checkFirstName = () => {
    const data = document.querySelector("#first_name");
    if (/^[а-яА-ЯёЁ]+$/.test(data.value)) {
        data.style.cssText = "border: 1px solid #31965e";
        document.querySelector("#first_name_hint").style.cssText = "color: #31965e";
        return false;
    }
    data.style.cssText = "border: 1px solid #752e2e";
    document.querySelector("#first_name_hint").style.cssText = "color: #752e2e";
    return true;
}

checkLastName = () => {
    const data = document.querySelector("#last_name");
    if (/^[а-яА-ЯёЁ]+$/.test(data.value)) {
        data.style.cssText = "border: 1px solid #31965e";
        document.querySelector("#last_name_hint").style.cssText = "color: #31965e";
        return false;
    }
    data.style.cssText = "border: 1px solid #752e2e";
    document.querySelector("#last_name_hint").style.cssText = "color: #752e2e";
    return true;
}

checkEmail = () => {
    const data = document.querySelector("#email");
    if (/^[a-zA-Z][a-zA-Z0-9]*@[a-z]+\.[a-z]+$/.test(data.value)) {
        data.style.cssText = "border: 1px solid #31965e";
        document.querySelector("#email_hint").style.cssText = "color: #31965e";
        return false;
    }
    data.style.cssText = "border: 1px solid #752e2e";
    document.querySelector("#email_hint").style.cssText = "color: #752e2e";
    return true;
}

checkPassword = () => {
    const data = document.querySelector("#password");
    let have_error = false;

    if (/^[a-zA-Z0-9]{7,}$/.test(data.value)) {
        data.style.border = "1px solid #31965e";
        document.querySelector("#password_hint_1").style.color = "#31965e";
    } else {
        data.style.border = "1px solid #752e2e";
        document.querySelector("#password_hint_1").style.color = "#752e2e";
        have_error = true;
    }

    if (!/[a-zA-Z]/.test(data.value) || !/[0-9]/.test(data.value)) {
        data.style.border = "1px solid #752e2e";
        document.querySelector("#password_hint_2").style.color = "#752e2e";
        have_error = true;
    } else {
        document.querySelector("#password_hint_2").style.color = "#31965e";
    }

    return have_error;
}

checkRepeatPassword = () => {
    const data1 = document.querySelector("#confirm_password");
    const data2 = document.querySelector("#password");
    if (data1.value === data2.value) {
        data1.style.cssText = "border: 1px solid #31965e";
        document.querySelector("#confirm_password_hint").style.cssText = "color: #31965e";
        return false;
    }
    data1.style.cssText = "border: 1px solid #752e2e";
    document.querySelector("#confirm_password_hint").style.cssText = "color: #752e2e";
    return true;
}

checkCaptcha = () => {
    const data1 = document.querySelector(".captcha-check");
    const data2 = document.querySelector(".captcha-example");
    if (data1.value === data2.textContent) {
        data1.style.cssText = "border: 1px solid #31965e";
        return false;
    }
    data2.textContent = generateCaptcha(6);
    data1.value = "";
    data1.style.cssText = "border: 1px solid #752e2e";
    return true;
}

document.querySelector("#first_name").addEventListener("input", () => {
    let input = document.querySelector("#first_name").value
    document.querySelector("#first_name").value = input.charAt(0).toUpperCase() + input.slice(1).toLowerCase();
})

document.querySelector("#last_name").addEventListener("input", () => {
    let input = document.querySelector("#last_name").value
    document.querySelector("#last_name").value = input.charAt(0).toUpperCase() + input.slice(1).toLowerCase();
})
