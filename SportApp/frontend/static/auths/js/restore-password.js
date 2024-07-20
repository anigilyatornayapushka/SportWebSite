const stageInput = document.querySelector("#stage");

if (stageInput.value == 1) {
    const emailInput = document.querySelector("#email");
    const emailComment = document.querySelector("#comment-email")

    const form = document.querySelector("form");
    
    form.addEventListener("submit", (event) => {
        if (!/^[a-zA-Z][a-zA-Z0-9]*@[a-z]+\.[a-z]+$/.test(emailInput.value)) {
            event.preventDefault();
            emailComment.style.cssText = "color: #752e2e;";
            emailInput.style.cssText = "border: 1px solid #752e2e;";
        } else {
            emailComment.style.cssText = "color: #31965e;";
            emailInput.style.cssText = "border: 1px solid #31965e;";
        }
    })
} else if (stageInput.value == 2) {
    const resetCode = document.querySelector("#reset_code");
    const newPassword = document.querySelector("#new_password");
    const confirmPassword = document.querySelector("#confirm_password");

    const form = document.querySelector("form");
    
    form.addEventListener("submit", (event) => {
        if (!/^[0-9]{8}$/.test(resetCode.value)) {
            event.preventDefault();
            resetCode.style.cssText = "border: 1px solid #752e2e;";
            document.querySelector("#comment-reset-code").style.cssText = "color: #752e2e;";
        } else {
            resetCode.style.cssText = "border: 1px solid #31965e;";
            document.querySelector("#comment-reset-code").style.cssText = "color: #31965e;";
        }

        let newPasswordHaveError = false;

        if (! /^[a-zA-Z0-9]{7,128}$/.test(newPassword.value) ) {
            event.preventDefault();
            newPasswordHaveError = true;
            document.querySelector("#new_password_hint_1").style.cssText = "color: #752e2e;"
        } else {
            document.querySelector("#new_password_hint_1").style.cssText = "color: #31965e;"
        }

        if (!/[a-zA-Z]/.test(newPassword.value) || !/[0-9]/.test(newPassword.value)) {
            event.preventDefault();
            newPasswordHaveError = true;
            document.querySelector("#new_password_hint_2").style.cssText = "color: #752e2e;"

        } else {
            document.querySelector("#new_password_hint_2").style.cssText = "color: #31965e;"
        }

        if (newPasswordHaveError) newPassword.style.cssText = "border: 1px solid #752e2e;"
        else newPassword.style.cssText = "border: 1px solid #31965e;"

        if (newPassword.value !== confirmPassword.value) {
            event.preventDefault();
            document.querySelector("#confirm_password_hint").style.cssText = "color: #752e2e;"
            confirmPassword.style.cssText = "border: 1px solid #752e2e;"
        } else {
            document.querySelector("#confirm_password_hint").style.cssText = "color: #31965e;"
            confirmPassword.style.cssText = "border: 1px solid #31965e;"
        }
    })
}
