from django import forms
from .models import NetworkDevice


class NetworkDeviceForm(forms.ModelForm):
    class Meta:
        model = NetworkDevice
        fields = ["device_name", "ip_address", "device_type"]
        widgets = {
            "device_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Lab Computer 1"}),
            "ip_address": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. 192.168.1.10"}),
            "device_type": forms.Select(attrs={"class": "form-select"}),
        }
