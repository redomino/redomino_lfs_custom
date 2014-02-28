from django.conf import settings
from django.core.cache import cache
from django.template.loader import render_to_string                                                                                                                                           
from django.template import RequestContext                                                                                                                                                    

from lfs.catalog.models import ProductPropertyValue                                                                                                                                           
from lfs.catalog.settings import PROPERTY_VALUE_TYPE_FILTER
from lfs.catalog.settings import PROPERTY_VALUE_TYPE_DEFAULT                                                                                                                                  

def product_inline(request, product, template_name="lfs/catalog/products/product_inline.html"):
    """
    Part of the product view, which displays the actual data of the product.

    This is factored out to be able to better cached and in might in future used
    used to be updated via ajax requests.
    """
    cache_key = "%s-product-inline-%s-%s" % (settings.CACHE_MIDDLEWARE_KEY_PREFIX, request.user.is_superuser, product.id)
    result = cache.get(cache_key)
    if result is not None:
        return result

    # Switching to default variant
    if product.is_product_with_variants():
        temp = product.get_default_variant()
        product = temp if temp else product

    properties = []
    variants = []

    display_variants_list = True
    if product.is_variant():
        parent = product.parent
        if parent.variants_display_type == 'SELECT':
            display_variants_list = False
            # Get all properties (sorted). We need to traverse through all
            # property/options to select the options of the current variant.
            for property in parent.get_property_select_fields():
                options = []
                for property_option in property.options.all():
                    if product.has_option(property, property_option):
                        selected = True
                    else:
                        selected = False
                    options.append({
                        "id": property_option.id,
                        "name": property_option.name,
                        "selected": selected,
                    })
                properties.append({
                    "id": property.id,
                    "name": property.name,
                    "title": property.title,
                    "unit": property.unit,
                    "options": options,
                })
        else:
            properties = parent.get_property_select_fields()
            variants = parent.get_variants()

    elif product.is_configurable_product():
        for property in product.get_configurable_properties():
            options = []
            try:
                ppv = ProductPropertyValue.objects.get(product=product, property=property, type=PROPERTY_VALUE_TYPE_DEFAULT)
                ppv_value = ppv.value
            except ProductPropertyValue.DoesNotExist:
                ppv = None
                ppv_value = ""

            # Only selected properties are shown
            try:                                                                                                                                                                              
                ppvs = ProductPropertyValue.objects.filter(property=property, product=product, type=PROPERTY_VALUE_TYPE_FILTER)                                                               
                value_ids = [ppv.value for ppv in ppvs]                                                                                                                                       
            except ProductPropertyValue.DoesNotExist:                                                                                                                                         
                value_ids = ppvs = []                                                                                                                                                         
                                                                                                                                                                                              
            for property_option in [property_option for property_option in property.options.all() if str(property_option.id) in value_ids]:
                if ppv_value == str(property_option.id):
                    selected = True
                else:
                    selected = False

                options.append({
                    "id": property_option.id,
                    "name": property_option.name,
                    "price": property_option.price,
                    "selected": selected,
                })
            properties.append({
                "obj": property,
                "id": property.id,
                "name": property.name,
                "title": property.title,
                "unit": property.unit,
                "display_price": property.display_price,
                "options": options,
                "value": ppv_value,
            })

    if product.get_template_name() != None:
        template_name = product.get_template_name()

    if product.get_active_packing_unit():
        packing_result = calculate_packing(request, product.id, 1, True, True)
    else:
        packing_result = ""

    # attachments
    attachments = product.get_attachments()

    result = render_to_string(template_name, RequestContext(request, {
        "product": product,
        "variants": variants,
        "product_accessories": product.get_accessories(),
        "properties": properties,
        "packing_result": packing_result,
        "attachments": attachments,
        "quantity": product.get_clean_quantity(1),
        "price_includes_tax": product.price_includes_tax(request),
        "price_unit": product.get_price_unit(),
        "unit": product.get_unit(),
        "display_variants_list": display_variants_list,
        "for_sale": product.get_for_sale(),
    }))

    cache.set(cache_key, result)
    return result


from lfs.catalog import views
views.product_inline = product_inline

