const form = document.querySelector("form");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    let has_error = false;
    if (checkFirstName()) has_error = true;
    if (checkLastName()) has_error = true;
    if (checkEmail()) has_error = true;
    if (checkPassword()) has_error = true;
    if (checkRepeatPassword()) has_error = true;
    if (checkCaptcha()) has_error = true;

    if (has_error) return false;

    const formData = new FormData(form);
    const data = {}
    formData.forEach((value, key) => {
        data[key] = value;
    });

    try {
        const response = await fetch('http://localhost:8000/api/v1/auths/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        
        if (response.ok) {
            document.querySelector("#message").innerHTML = '<p style="color: #31965e">Вы успешно зарегистрировались</p>';
            form.reset();
        } else {
            for (let key in result) {
                for (let err of result[key]) {
                    if (err) document.querySelector("#message").innerHTML = `<p style="color: #752e2e">${err}</p>`;
                }
            }
        }
    } catch (error) {
        document.querySelector("#message").innerHTML = `<p style="color: #752e2e">Произошла ошибка: ${error.message}</p>`;
    }
});

checkFirstName = () => {
    const data = document.querySelector("#first_name");
    if (/^[а-яА-ЯёЁ]+$/.test(data.value)) {
        data.style.cssText = "border: 1px solid #31965e";
        document.querySelector("#first_name_hint").style.cssText = "color: #31965e";
    } else {
        data.style.cssText = "border: 1px solid #752e2e";
        document.querySelector("#first_name_hint").style.cssText = "color: #752e2e";
        return true;
    }
}

checkLastName = () => {
    const data = document.querySelector("#last_name");
    if (/^[а-яА-ЯёЁ]+$/.test(data.value)) {
        data.style.cssText = "border: 1px solid #31965e";
        document.querySelector("#last_name_hint").style.cssText = "color: #31965e";
    } else {
        data.style.cssText = "border: 1px solid #752e2e";
        document.querySelector("#last_name_hint").style.cssText = "color: #752e2e";
        return true;
    }
}

checkEmail = () => {
    const data = document.querySelector("#email");
    if (/^[a-zA-Z][a-zA-Z0-9]*@[a-z]+\.[a-z]+$/.test(data.value)) {
        data.style.cssText = "border: 1px solid #31965e";
        document.querySelector("#email_hint").style.cssText = "color: #31965e";
    } else {
        data.style.cssText = "border: 1px solid #752e2e";
        document.querySelector("#email_hint").style.cssText = "color: #752e2e";
        return true;
    }
}

checkPassword = () => {
    const data = document.querySelector("#password");

    if (/^[a-zA-Z0-9]{7,128}$/.test(data.value)) {
        data.style.border = "1px solid #31965e";
        document.querySelector("#password_hint_1").style.color = "#31965e";
    } else {
        data.style.border = "1px solid #752e2e";
        document.querySelector("#password_hint_1").style.color = "#752e2e";
        return true;
    }

    if (!/[a-zA-Z]/.test(data.value) || !/[0-9]/.test(data.value)) {
        data.style.border = "1px solid #752e2e";
        document.querySelector("#password_hint_2").style.color = "#752e2e";
        return true;
    } else {
        document.querySelector("#password_hint_2").style.color = "#31965e";
    }
}

checkRepeatPassword = () => {
    const data1 = document.querySelector("#confirm_password");
    const data2 = document.querySelector("#password");
    if (data1.value === data2.value) {
        data1.style.cssText = "border: 1px solid #31965e";
        document.querySelector("#confirm_password_hint").style.cssText = "color: #31965e";
    } else {
        data1.style.cssText = "border: 1px solid #752e2e";
        document.querySelector("#confirm_password_hint").style.cssText = "color: #752e2e";
        return true;
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
