from django.conf import settings
from django.utils.translation import ugettext as _

settings.POSTAL_ADDRESS_STATE = getattr(settings, 'POSTAL_ADDRESS_STATE', (_("Province"), True))
settings.SHOW_VAT = getattr(settings, 'SHOW_VAT', False)


from lfs.customer.forms import AddressForm
from django import forms

AddressForm.shipping_firstname = forms.CharField(label=_(u"First Name"), required=False, max_length=50)
AddressForm.base_fields['shipping_firstname'] = AddressForm.shipping_firstname
AddressForm.shipping_lastname = forms.CharField(label=_(u"Last Name"), required=False, max_length=50)
AddressForm.base_fields['shipping_lastname'] = AddressForm.shipping_lastname


from lfs.manage.voucher.forms import VoucherForm

VoucherForm.amount = forms.IntegerField(label=_(u"Voucher quantity"), required=True)
VoucherForm.value = forms.FloatField(label=_(u"Voucher value"), required=True)
VoucherForm.effective_from = forms.FloatField(label=_(u"Voucher effective from"), required=True)
VoucherForm.limit = forms.IntegerField(label=_(u"Voucher limit"), initial=1, required=True)

VoucherForm.base_fields['amount'] = VoucherForm.amount
VoucherForm.base_fields['value'] = VoucherForm.value
VoucherForm.base_fields['effective_from'] = VoucherForm.effective_from
VoucherForm.base_fields['limit'] = VoucherForm.limit

