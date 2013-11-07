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


from django.shortcuts import render_to_response
from django.contrib.auth.forms import PasswordChangeForm
from lfs.customer import views
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

@login_required
def password(request, template_name="lfs/customer/password.html"):
    """Changes the password of current user.
    """
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("lfs_my_account")+'?confirm=1')
    else:
        form = PasswordChangeForm(request.user)

    return render_to_response(template_name, RequestContext(request, {
        "form": form
    }))

views.password = password


