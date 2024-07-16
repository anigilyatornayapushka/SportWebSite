const form = document.querySelector("form");

form.addEventListener("submit", (event) => {
    checkFirstName(event);
    checkLastName(event);
    checkEmail(event);
    checkPassword(event);
    checkRepeatPassword(event);
});

checkFirstName = (event) => {
    const data = document.querySelector("#first_name");
    if (/^[а-яА-ЯёЁ]+$/.test(data.value)) {
        data.style.cssText = "border: 1px solid #31965e";
        document.querySelector("#first_name_hint").style.cssText = "color: #31965e";
    } else {
        data.style.cssText = "border: 1px solid #752e2e";
        document.querySelector("#first_name_hint").style.cssText = "color: #752e2e";
        event.preventDefault();
    }
}

checkLastName = (event) => {
    const data = document.querySelector("#last_name");
    if (/^[а-яА-ЯёЁ]+$/.test(data.value)) {
        data.style.cssText = "border: 1px solid #31965e";
        document.querySelector("#last_name_hint").style.cssText = "color: #31965e";
    } else {
        data.style.cssText = "border: 1px solid #752e2e";
        document.querySelector("#last_name_hint").style.cssText = "color: #752e2e";
        event.preventDefault();
    }
}

checkEmail = (event) => {
    const data = document.querySelector("#email");
    if (/^[a-zA-Z][a-zA-Z0-9]*@[a-z]+\.[a-z]+$/.test(data.value)) {
        data.style.cssText = "border: 1px solid #31965e";
        document.querySelector("#email_hint").style.cssText = "color: #31965e";
    } else {
        data.style.cssText = "border: 1px solid #752e2e";
        document.querySelector("#email_hint").style.cssText = "color: #752e2e";
        event.preventDefault();
    }
}

checkPassword = (event) => {
    const data = document.querySelector("#password");

    if (/^[a-zA-Z0-9]{7,}$/.test(data.value)) {
        data.style.border = "1px solid #31965e";
        document.querySelector("#password_hint_1").style.color = "#31965e";
    } else {
        data.style.border = "1px solid #752e2e";
        document.querySelector("#password_hint_1").style.color = "#752e2e";
        event.preventDefault();
    }

    if (!/[a-zA-Z]/.test(data.value) || !/[0-9]/.test(data.value)) {
        data.style.border = "1px solid #752e2e";
        document.querySelector("#password_hint_2").style.color = "#752e2e";
        event.preventDefault();
    } else {
        document.querySelector("#password_hint_2").style.color = "#31965e";
    }
}

checkRepeatPassword = (event) => {
    const data1 = document.querySelector("#confirm_password");
    const data2 = document.querySelector("#password");
    if (data1.value === data2.value) {
        data1.style.cssText = "border: 1px solid #31965e";
        document.querySelector("#confirm_password_hint").style.cssText = "color: #31965e";
    } else {
        data1.style.cssText = "border: 1px solid #752e2e";
        document.querySelector("#confirm_password_hint").style.cssText = "color: #752e2e";
        event.preventDefault();
    }
}

document.querySelector("#first_name").addEventListener("input", () => {
    let input = document.querySelector("#first_name").value
    document.querySelector("#first_name").value = input.charAt(0).toUpperCase() + input.slice(1).toLowerCase();
})

document.querySelector("#last_name").addEventListener("input", () => {
    let input = document.querySelector("#last_name").value
    document.querySelector("#last_name").value = input.charAt(0).toUpperCase() + input.slice(1).toLowerCase();
})
