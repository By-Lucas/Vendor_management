from django import forms
from vendor.model.vendor_models import Vendor
from vendor.model.product_value_model import VendorProductValue



class VendorForm(forms.ModelForm):
    #vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    class Meta:
        model = Vendor
        fields = ['vendor_name']

class VendorProductValueForm(forms.ModelForm):
    class Meta:
        model = VendorProductValue
        fields = '__all__'