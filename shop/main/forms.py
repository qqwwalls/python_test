from django import forms


class CardForm(forms.Form):
    title = forms.CharField(
        label="Назва картки",
        min_length=3,
        max_length=80,
        help_text="Від 3 до 80 символів.",
        error_messages={
            "required": "Введіть назву картки.",
            "min_length": "Назва має містити щонайменше 3 символи.",
            "max_length": "Скоротіть назву до 80 символів.",
        },
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Наприклад, Мій перший проєкт"}),
    )
    description = forms.CharField(
        label="Опис",
        min_length=20,
        max_length=500,
        help_text="Від 20 до 500 символів. Розкажіть, чим цікава ваша картка.",
        error_messages={
            "required": "Додайте опис картки.",
            "min_length": "Розкажіть трохи більше: опис має містити щонайменше 20 символів.",
            "max_length": "Скоротіть опис до 500 символів.",
        },
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Короткий опис вашої ідеї або проєкту"}),
    )
    image = forms.ImageField(
        label="Зображення",
        help_text="JPG, PNG або WebP до 2 МБ. Розмір від 320 × 180 до 4096 × 4096 пікселів.",
        error_messages={
            "required": "Додайте зображення для картки.",
            "invalid": "Не вдалося прочитати файл. Оберіть зображення повторно.",
            "invalid_image": "Цей файл не є справним зображенням. Оберіть JPG, PNG або WebP.",
            "invalid_extension": "Дозволені лише зображення JPG, PNG або WebP.",
            "empty": "Обраний файл порожній. Завантажте інше зображення.",
        },
        widget=forms.FileInput(attrs={"class": "form-control", "accept": ".jpg,.jpeg,.png,.webp"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs["aria-describedby"] = f"id_{name}_help id_{name}_error"
        if self.is_bound:
            for name in self.errors:
                if name in self.fields:
                    self.fields[name].widget.attrs["class"] += " is-invalid"
                    self.fields[name].widget.attrs["aria-invalid"] = "true"

    def clean_image(self):
        image = self.cleaned_data["image"]
        if image.size > 2 * 1024 * 1024:
            raise forms.ValidationError("Зображення завелике. Максимальний розмір — 2 МБ.", code="too_large")
        if image.image.format not in ("JPEG", "PNG", "WEBP"):
            raise forms.ValidationError("Дозволені лише зображення JPG, PNG або WebP.", code="invalid_format")
        width, height = image.image.size
        if width < 320 or height < 180 or width > 4096 or height > 4096:
            raise forms.ValidationError(
                "Оберіть зображення від 320 × 180 до 4096 × 4096 пікселів.", code="dimensions"
            )
        return image


class RegistrationForm(forms.Form):
    name = forms.CharField(label="Ім'я", min_length=2, max_length=80,
                           widget=forms.TextInput(attrs={"autocomplete": "name"}))
    email = forms.EmailField(label="Email", max_length=254,
                             widget=forms.EmailInput(attrs={"autocomplete": "email"}))
    password = forms.CharField(label="Пароль", min_length=8, max_length=128, strip=False,
                               widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))
    password_confirm = forms.CharField(label="Підтвердження пароля", max_length=128, strip=False,
                                       widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({
                "class": "form-control",
                "aria-describedby": f"id_{name}_error",
            })

    def clean(self):
        data = super().clean()
        if data.get("password") and data.get("password_confirm"):
            if data["password"] != data["password_confirm"]:
                self.add_error("password_confirm", "Паролі не збігаються.")
        return data
