// ---------- Бургер-меню ----------
const burger = document.getElementById("burger");
const nav = document.getElementById("nav");

function toggleMenu(open) {
  burger.classList.toggle("is-open", open);
  nav.classList.toggle("is-open", open);
  burger.setAttribute("aria-expanded", String(open));
}

burger.addEventListener("click", () => toggleMenu(!nav.classList.contains("is-open")));
nav.addEventListener("click", (event) => {
  if (event.target.closest("a")) toggleMenu(false);
});

// ---------- «Заказать» у услуги подставляет её в форму ----------
const serviceSelect = document.querySelector('select[name="service"]');

document.querySelectorAll("[data-service]").forEach((link) => {
  link.addEventListener("click", () => {
    if (serviceSelect) serviceSelect.value = link.dataset.service;
  });
});

// ---------- Маска телефона ----------
const phoneInput = document.querySelector('input[name="phone"]');

if (phoneInput) {
  phoneInput.addEventListener("input", () => {
    let digits = phoneInput.value.replace(/\D/g, "");
    if (digits.startsWith("8")) digits = "7" + digits.slice(1);
    if (digits && !digits.startsWith("7")) digits = "7" + digits;
    digits = digits.slice(0, 11);

    const p = [digits.slice(1, 4), digits.slice(4, 7), digits.slice(7, 9), digits.slice(9, 11)];
    let result = digits ? "+7" : "";
    if (p[0]) result += ` (${p[0]}`;
    if (p[0].length === 3) result += ")";
    if (p[1]) result += ` ${p[1]}`;
    if (p[2]) result += `-${p[2]}`;
    if (p[3]) result += `-${p[3]}`;
    phoneInput.value = result;
  });
}
