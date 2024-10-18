from django import forms
from .models import PWD

class PWDForm(forms.ModelForm):
    mac_address = forms.CharField(
        max_length=17,
        help_text="Enter MAC address in format XX:XX:XX:XX:XX:XX"
    )

    class Meta:
        model = PWD
        fields = ['name', 'phone_number', 'mac_address', 'id_number']

    def clean_mac_address(self):
        mac_address_str = self.cleaned_data['mac_address']
        # Validate the MAC address format
        if not self.validate_mac_address(mac_address_str):
            raise forms.ValidationError("Invalid MAC address format. Please use format XX:XX:XX:XX:XX:XX.")
        return mac_address_str  # Return the string for storage

    def validate_mac_address(self, mac):
        """Check if the provided MAC address is valid."""
        # A simple regex to check the format (XX:XX:XX:XX:XX:XX)
        import re
        pattern = r'^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$'
        return re.match(pattern, mac) is not None

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance