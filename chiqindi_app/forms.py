from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, WasteReport, VILOYATLAR, TUMANLAR


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, label="Ism", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ismingiz'}))
    last_name = forms.CharField(max_length=50, label="Familiya", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Familiyangiz'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}))
    phone = forms.CharField(max_length=20, label="Telefon", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+998901234567'}))
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, label="Rol", widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'role', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Foydalanuvchi nomi'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Parol'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Parolni tasdiqlang'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone = self.cleaned_data['phone']
        user.role = self.cleaned_data['role']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class WasteReportForm(forms.ModelForm):
    latitude = forms.FloatField(widget=forms.HiddenInput())
    longitude = forms.FloatField(widget=forms.HiddenInput())
    viloyat = forms.ChoiceField(
        choices=[('', '-- Viloyatni tanlang --')] + list(VILOYATLAR),
        label="Viloyat",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_viloyat'})
    )
    tuman = forms.CharField(
        max_length=100, label="Tuman", required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'id_tuman', 'placeholder': 'Tuman nomi'})
    )

    class Meta:
        model = WasteReport
        fields = ['latitude', 'longitude', 'waste_type', 'size', 'viloyat', 'tuman', 'address', 'description', 'image']
        widgets = {
            'waste_type': forms.Select(attrs={'class': 'form-select'}),
            'size': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ko\'cha, uy raqami'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Qo\'shimcha ma\'lumot...'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def clean_viloyat(self):
        v = self.cleaned_data.get('viloyat')
        if not v:
            raise forms.ValidationError("Viloyatni tanlang")
        return v


class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = WasteReport
        fields = ['status', 'authority_note', 'assigned_to']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'authority_note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = CustomUser.objects.filter(role=CustomUser.ROLE_AUTHORITY)
        self.fields['assigned_to'].required = False
        self.fields['authority_note'].required = False


class FilterForm(forms.Form):
    viloyat = forms.ChoiceField(
        choices=[('', 'Barcha viloyatlar')] + list(VILOYATLAR),
        required=False, label="Viloyat",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    tuman = forms.CharField(
        required=False, label="Tuman",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tuman bo\'yicha qidirish'})
    )
    status = forms.ChoiceField(
        choices=[('', 'Barcha holatlar')] + WasteReport.STATUS_CHOICES,
        required=False, label="Holat",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    waste_type = forms.ChoiceField(
        choices=[('', 'Barcha turlar')] + WasteReport.WASTE_TYPE_CHOICES,
        required=False, label="Chiqindi turi",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
