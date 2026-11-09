const form = document.querySelector("#registration-form");
const resultBox = document.querySelector("#registration-result");
const submitButton = form.querySelector('[type="submit"]');

function showResult(message, success) {
    resultBox.className = `registration-result mt-3 alert alert-${success ? "success" : "danger"}`;
    resultBox.textContent = message;
    resultBox.hidden = false;
}

document.querySelector("#show-password").addEventListener("change", event => {
    for (const name of ["password", "password_confirm"]) {
        form.elements[name].type = event.target.checked ? "text" : "password";
    }
});

form.addEventListener("submit", async event => {
    event.preventDefault();
    resultBox.hidden = true;
    form.querySelectorAll(".is-invalid").forEach(field => {
        field.classList.remove("is-invalid");
        field.removeAttribute("aria-invalid");
    });
    form.querySelectorAll(".invalid-feedback").forEach(error => { error.textContent = ""; });
    const data = Object.fromEntries(new FormData(form).entries());
    const csrfToken = data.csrfmiddlewaretoken;
    delete data.csrfmiddlewaretoken;
    submitButton.disabled = true;
    submitButton.textContent = "Надсилання...";
    try {
        const response = await fetch(form.action, {
            method: "POST",
            mode: "same-origin",
            credentials: "same-origin",
            headers: {"Content-Type": "application/json", "X-CSRFToken": csrfToken},
            body: JSON.stringify(data),
        });
        if (response.status === 403) throw new Error("Оновіть сторінку та надішліть форму ще раз.");
        const result = await response.json();
        if (response.ok) {
            form.reset();
            form.elements.password.type = "password";
            form.elements.password_confirm.type = "password";
            showResult(result.message, true);
        } else {
            for (const [name, messages] of Object.entries(result.errors || {})) {
                const field = form.elements.namedItem(name);
                if (!field) continue;
                field.classList.add("is-invalid");
                field.setAttribute("aria-invalid", "true");
                document.getElementById(`${field.id}_error`).textContent = messages.join(" ");
            }
            showResult(result.error || "Перевірте введені дані.", false);
            form.querySelector(".is-invalid")?.focus();
        }
    } catch (error) {
        showResult(error instanceof SyntaxError ? "Не вдалося отримати відповідь сервера." : error.message, false);
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = "Надіслати";
    }
});
