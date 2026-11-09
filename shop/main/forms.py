from django import forms


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
