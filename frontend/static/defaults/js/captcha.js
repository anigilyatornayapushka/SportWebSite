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

document.querySelector(".captcha-example").value = generateCaptcha(6);

const checkCaptcha = () => {
    const data1 = document.querySelector(".captcha-check");
    const data2 = document.querySelector(".captcha-example");
    if (data1.value === data2.value) {
        data1.style.cssText = "border: 1px solid #31965e";
    } else {
        data2.value = generateCaptcha(6);
        data1.value = "";
        data1.style.cssText = "border: 1px solid #752e2e";
        return true;
    }
}

document.querySelector(".captcha-example").addEventListener("copy", (event) => {
    event.preventDefault();
});
