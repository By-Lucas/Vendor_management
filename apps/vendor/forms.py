from django import forms
from vendor.model.vendor_models import Vendor


class VendorForm(forms.ModelForm):
    #vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    class Meta:
        model = Vendor
        fields = ['vendor_name']