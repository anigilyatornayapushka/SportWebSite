const form = document.querySelector("form");

form.addEventListener("submit", (event) => {
    const oldPassword = document.body.querySelector("#old_password").value;
    const newPassword = document.body.querySelector("#new_password").value;
    const confirmPassword = document.body.querySelector("#confirm_password").value;

    let oldPasswordHaveError = false;

    if (! /^[a-zA-Z0-9]{7,128}$/.test(oldPassword) ) {
        event.preventDefault();
        oldPasswordHaveError = true;
        document.querySelector("#old_password_hint_1").style.cssText = "color: #752e2e;"
    } else {
        document.querySelector("#old_password_hint_1").style.cssText = "color: #31965e;"
    }
    
    if (!/[a-zA-Z]/.test(oldPassword) || !/[0-9]/.test(oldPassword)) {
        event.preventDefault();
        oldPasswordHaveError = true;
        document.querySelector("#old_password_hint_2").style.cssText = "color: #752e2e;"
    } else {
        document.querySelector("#old_password_hint_2").style.cssText = "color: #31965e;"
    }

    if (oldPasswordHaveError) document.querySelector("#old_password").style.cssText = "border: 1px solid #752e2e;"
    else document.querySelector("#old_password").style.cssText = "border: 1px solid #31965e;"

    let newPasswordHaveError = false;

    if (! /^[a-zA-Z0-9]{7,128}$/.test(newPassword) ) {
        event.preventDefault();
        newPasswordHaveError = true;
        document.querySelector("#new_password_hint_1").style.cssText = "color: #752e2e;"
    } else {
        document.querySelector("#new_password_hint_1").style.cssText = "color: #31965e;"
        document.querySelector("#new_password").style.cssText = "border: 1px solid #31965e;"
    }

    if (!/[a-zA-Z]/.test(newPassword) || !/[0-9]/.test(newPassword)) {
        event.preventDefault();
        newPasswordHaveError = true;
        document.querySelector("#new_password_hint_2").style.cssText = "color: #752e2e;"
        
    } else {
        document.querySelector("#new_password_hint_2").style.cssText = "color: #31965e;"
    }

    if (newPasswordHaveError) document.querySelector("#new_password").style.cssText = "border: 1px solid #752e2e;"
    else document.querySelector("#new_password").style.cssText = "border: 1px solid #31965e;"

    if (newPassword !== confirmPassword) {
        event.preventDefault();
        document.querySelector("#confirm_password_hint").style.cssText = "color: #752e2e;"
        document.querySelector("#confirm_password").style.cssText = "border: 1px solid #752e2e;"
    } else {
        document.querySelector("#confirm_password_hint").style.cssText = "color: #31965e;"
        document.querySelector("#confirm_password").style.cssText = "border: 1px solid #31965e;"
    }
})
