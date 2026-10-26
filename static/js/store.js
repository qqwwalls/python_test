(() => {
    const products = JSON.parse(document.querySelector("#product-data").textContent);
    const productMap = new Map(products.map(product => [product.id, product]));
    const grid = document.querySelector("#product-grid");
    const cards = new Map([...grid.children].map(card => [Number(card.dataset.productId), card]));
    const search = document.querySelector("#search");
    const minPrice = document.querySelector("#min-price");
    const maxPrice = document.querySelector("#max-price");
    const inStock = document.querySelector("#in-stock");
    const sort = document.querySelector("#sort");
    const profileForm = document.querySelector("#profile-form");
    const cartKey = "fruitmarket-cart";
    let category = "all";
    let toastTimer;

    function readSaved(key, fallback) {
        try {
            return JSON.parse(localStorage.getItem(key)) ?? fallback;
        } catch {
            return fallback;
        }
    }

    function save(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch {
            return false;
        }
    }

    const savedCart = readSaved(cartKey, {});
    let cart = {};
    for (const product of products) {
        const quantity = savedCart && savedCart[product.id];
        if (Number.isInteger(quantity) && quantity > 0 && quantity <= 99) {
            cart[product.id] = quantity;
        }
    }

    function icons() {
        window.lucide?.createIcons();
    }

    function element(tag, className, text) {
        const node = document.createElement(tag);
        if (className) node.className = className;
        if (text !== undefined) node.textContent = text;
        return node;
    }

    function iconButton(name, label, className = "") {
        const button = element("button", className);
        button.type = "button";
        button.setAttribute("aria-label", label);
        button.title = label;
        const icon = element("i");
        icon.dataset.lucide = name;
        button.append(icon);
        return button;
    }

    function money(value) {
        return `${new Intl.NumberFormat("uk-UA").format(value)} грн`;
    }

    function imageFor(product) {
        return cards.get(product.id).querySelector("img").src;
    }

    function notify(message) {
        const toast = document.querySelector("#toast");
        toast.querySelector("span").textContent = message;
        toast.classList.add("visible");
        clearTimeout(toastTimer);
        toastTimer = setTimeout(() => toast.classList.remove("visible"), 2600);
    }

    function openDialog(id) {
        document.querySelectorAll("dialog[open]").forEach(dialog => dialog.close());
        if (id === "cart-dialog") renderCart();
        if (id === "profile-dialog") {
            const profile = readSaved("fruitmarket-profile", {});
            profileForm.elements.name.value = typeof profile?.name === "string" ? profile.name : "";
            profileForm.elements.email.value = typeof profile?.email === "string" ? profile.email : "";
        }
        document.getElementById(id).showModal();
        document.body.classList.add("has-dialog");
    }

    function renderCart() {
        const items = document.querySelector("#cart-items");
        items.replaceChildren();
        let total = 0;
        let count = 0;
        for (const [id, quantity] of Object.entries(cart)) {
            const product = productMap.get(Number(id));
            if (!product) continue;
            count += quantity;
            total += product.price * quantity;
            const row = element("article", "cart-item");
            const image = element("img");
            image.src = imageFor(product);
            image.alt = product.name;
            const info = element("div");
            info.append(element("h3", "", product.name));
            info.append(element("p", "item-price", `${money(product.price)} / кг`));
            const controls = element("div", "quantity-control");
            const minus = iconButton("minus", `Зменшити кількість: ${product.name}`);
            const plus = iconButton("plus", `Збільшити кількість: ${product.name}`);
            minus.addEventListener("click", () => changeQuantity(product.id, -1));
            plus.addEventListener("click", () => changeQuantity(product.id, 1));
            plus.disabled = quantity >= 99;
            controls.append(minus, element("span", "", `${quantity} кг`), plus);
            info.append(controls);
            const remove = iconButton("trash-2", `Видалити: ${product.name}`, "icon-button remove-item");
            remove.addEventListener("click", () => {
                delete cart[product.id];
                updateCart();
            });
            row.append(image, info, remove);
            items.append(row);
        }
        document.querySelector("#cart-count").textContent = count;
        document.querySelector("#cart-count").hidden = count === 0;
        document.querySelector("#cart-title-count").textContent = count ? `(${count})` : "";
        document.querySelector("#cart-toggle").setAttribute("aria-label", `Відкрити кошик: ${count} кг`);
        document.querySelector("#cart-total").textContent = money(total);
        document.querySelector("#cart-footer").hidden = count === 0;
        if (!count) {
            const empty = element("div", "cart-empty");
            const icon = element("i");
            icon.dataset.lucide = "shopping-basket";
            const button = element("button", "primary-button", "Продовжити покупки");
            button.type = "button";
            button.addEventListener("click", () => {
                document.querySelector("#cart-dialog").close();
                document.querySelector("#catalog").scrollIntoView({behavior: "smooth"});
            });
            empty.append(icon, element("h3", "", "Кошик порожній"), button);
            items.append(empty);
        }
        icons();
    }

    function updateCart() {
        save(cartKey, cart);
        renderCart();
    }

    function changeQuantity(id, delta) {
        cart[id] = Math.min(99, (cart[id] || 0) + delta);
        if (cart[id] <= 0) delete cart[id];
        updateCart();
    }

    function addToCart(id, button) {
        const product = productMap.get(Number(id));
        if (!product?.available) return;
        if ((cart[product.id] || 0) >= 99) {
            notify("У кошику вже 99 кг цього товару");
            return;
        }
        changeQuantity(product.id, 1);
        notify(`${product.name} додано до кошика`);
        const label = button?.querySelector("span");
        if (label) {
            label.textContent = "Додано";
            setTimeout(() => { label.textContent = "Додати в кошик"; }, 1000);
        }
    }

    function applyFilters() {
        const query = search.value.trim().toLocaleLowerCase("uk");
        let visible = products.filter(product =>
            (category === "all" || product.categories.includes(category)) &&
            product.name.toLocaleLowerCase("uk").includes(query) &&
            product.price >= Number(minPrice.value) && product.price <= Number(maxPrice.value) &&
            (!inStock.checked || product.available)
        );
        const comparators = {
            "price-asc": (a, b) => a.price - b.price,
            "price-desc": (a, b) => b.price - a.price,
            rating: (a, b) => b.rating - a.rating || b.reviews - a.reviews,
            name: (a, b) => a.name.localeCompare(b.name, "uk"),
            popular: (a, b) => a.id - b.id,
        };
        visible.sort(comparators[sort.value] || comparators.popular);
        for (const card of cards.values()) card.hidden = true;
        for (const product of visible) {
            const card = cards.get(product.id);
            card.hidden = false;
            grid.append(card);
        }
        const selected = document.querySelector(`[data-category="${category}"]`);
        const categoryName = selected.querySelector("span").textContent;
        document.querySelector("#catalog-title").textContent = category === "all" ? "Фрукти" : categoryName;
        const noun = visible.length === 1 ? "товар" : visible.length >= 2 && visible.length <= 4 ? "товари" : "товарів";
        document.querySelector("#results-count").textContent = `Знайдено ${visible.length} ${noun}`;
        document.querySelector("#empty-state").hidden = visible.length !== 0;
        const active = category !== "all" || query || minPrice.value !== "20" || maxPrice.value !== "350" || !inStock.checked;
        document.querySelector("#active-filters").hidden = !active;
        const summary = [];
        if (category !== "all") summary.push(categoryName);
        if (query) summary.push(`«${search.value.trim()}»`);
        if (minPrice.value !== "20" || maxPrice.value !== "350") summary.push(`${minPrice.value}–${maxPrice.value} грн`);
        document.querySelector("#filter-summary").textContent = summary.join(" · ");
        document.querySelectorAll("[data-category]").forEach(button => {
            const selected = button.dataset.category === category;
            button.classList.toggle("selected", selected);
            button.setAttribute("aria-pressed", selected);
        });
        document.querySelector("#min-price-label").textContent = money(Number(minPrice.value));
        document.querySelector("#max-price-label").textContent = money(Number(maxPrice.value));
        document.querySelector("#price-range").style.setProperty("--low", `${(minPrice.value - 20) / 330 * 100}%`);
        document.querySelector("#price-range").style.setProperty("--high", `${(maxPrice.value - 20) / 330 * 100}%`);
    }

    function resetFilters() {
        category = "all";
        search.value = "";
        minPrice.value = 20;
        maxPrice.value = 350;
        inStock.checked = true;
        sort.value = "popular";
        applyFilters();
    }

    function showDetails(id) {
        const product = productMap.get(Number(id));
        if (!product) return;
        document.querySelector("#detail-name").textContent = product.name;
        document.querySelector("#detail-description").textContent = product.description;
        document.querySelector("#detail-price").textContent = `${money(product.price)} / кг`;
        const image = document.querySelector("#detail-image");
        image.src = imageFor(product);
        image.alt = product.name;
        document.querySelector("#detail-add").dataset.add = product.id;
        openDialog("product-dialog");
    }

    const info = {
        about: {title: "Про FruitMarket", paragraphs: ["Свіжі фрукти та ягоди для кожного дня.", "У нашому асортименті — яблука, цитрусові, тропічні фрукти та добірні ягоди."]},
        delivery: {title: "Доставка", paragraphs: ["Доставляємо фрукти у зручний для вас час.", "Вартість та час доставки залежать від адреси й обсягу замовлення та узгоджуються окремо."]},
        contacts: {title: "Контакти", paragraphs: ["FruitMarket", "Електронна пошта: hello@fruitmarket.example", "Понеділок — субота, 09:00–19:00"]},
    };

    document.addEventListener("click", event => {
        const button = event.target.closest("button");
        if (!button) return;
        if (button.hasAttribute("data-add")) addToCart(button.dataset.add, button);
        else if (button.hasAttribute("data-details")) showDetails(button.dataset.details);
        else if (button.hasAttribute("data-category")) { category = button.dataset.category; applyFilters(); }
        else if (button.hasAttribute("data-reset")) resetFilters();
        else if (button.hasAttribute("data-open")) openDialog(button.dataset.open);
        else if (button.hasAttribute("data-close")) button.closest("dialog").close();
        else if (button.hasAttribute("data-view")) {
            grid.classList.toggle("is-list", button.dataset.view === "list");
            document.querySelectorAll("[data-view]").forEach(item => {
                const active = item === button;
                item.classList.toggle("active", active);
                item.setAttribute("aria-pressed", active);
            });
        } else if (button.hasAttribute("data-info")) {
            const content = info[button.dataset.info];
            document.querySelector("#info-title").textContent = content.title;
            document.querySelector("#info-content").replaceChildren(...content.paragraphs.map(text => element("p", "", text)));
            openDialog("info-dialog");
        }
    });

    search.addEventListener("input", applyFilters);
    document.querySelector("#search-form").addEventListener("submit", event => {
        event.preventDefault();
        applyFilters();
        document.querySelector("#catalog").scrollIntoView({behavior: "smooth"});
    });
    minPrice.addEventListener("input", () => {
        if (Number(minPrice.value) > Number(maxPrice.value)) minPrice.value = maxPrice.value;
        applyFilters();
    });
    maxPrice.addEventListener("input", () => {
        if (Number(maxPrice.value) < Number(minPrice.value)) maxPrice.value = minPrice.value;
        applyFilters();
    });
    inStock.addEventListener("change", applyFilters);
    sort.addEventListener("change", applyFilters);
    document.querySelector("#clear-cart").addEventListener("click", () => {
        cart = {};
        updateCart();
        notify("Кошик очищено");
    });
    profileForm.addEventListener("submit", event => {
        event.preventDefault();
        const profile = {name: profileForm.elements.name.value.trim(), email: profileForm.elements.email.value.trim()};
        if (!profile.name) { profileForm.elements.name.focus(); return; }
        if (save("fruitmarket-profile", profile)) {
            document.querySelector("#profile-dialog").close();
            notify("Дані збережено");
        } else notify("Не вдалося зберегти дані");
    });
    document.querySelectorAll("dialog").forEach(dialog => {
        dialog.addEventListener("click", event => {
            if (event.target !== dialog) return;
            const rect = dialog.getBoundingClientRect();
            if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
        });
        dialog.addEventListener("close", () => document.body.classList.toggle("has-dialog", Boolean(document.querySelector("dialog[open]"))));
    });
    document.querySelector("#menu-toggle").addEventListener("click", event => {
        const button = event.currentTarget;
        const expanded = document.querySelector("#site-nav").classList.toggle("is-open");
        button.setAttribute("aria-expanded", expanded);
    });
    document.querySelector("#site-nav").addEventListener("click", () => {
        document.querySelector("#site-nav").classList.remove("is-open");
        document.querySelector("#menu-toggle").setAttribute("aria-expanded", "false");
    });
    document.querySelector("#filter-toggle").addEventListener("click", event => {
        const expanded = document.querySelector("#filters").classList.toggle("is-open");
        event.currentTarget.setAttribute("aria-expanded", expanded);
    });
    applyFilters();
    renderCart();
    icons();
})();
