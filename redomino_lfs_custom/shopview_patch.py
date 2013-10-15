from lfs.core import views
from django.shortcuts import render_to_response
from lfs.caching.utils import lfs_get_object_or_404
from lfs.catalog.models import Category
from lfs.core.models import Shop
from django.template import RequestContext

from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.core.cache import cache
from django.conf import settings
from lfs.core.utils import lfs_pagination
from django.template.loader import render_to_string
import lfs

def shop_view(request,slug="", start=1, template_name="lfs/shop/shop.html"):
    """Displays the shop.
    """

    shop = lfs_get_object_or_404(Shop, pk=1)
    #category = lfs_get_object_or_404(Category, slug='home-products')

    #all_products = category.get_all_products()



    #last_category = request.session.get("last_category")
    #if (last_category is None) or (last_category.slug != slug):
    #    if "product-filter" in request.session:
    #        del request.session["product-filter"]
    #    if "price-filter" in request.session:
    #        del request.session["price-filter"]

    try:
        default_sorting = settings.LFS_PRODUCTS_SORTING
    except AttributeError:
        default_sorting = "price"
    #sorting = request.session.get("sorting", default_sorting)
    sorting = default_sorting

    #product_filter = request.session.get("product-filter", {})
    #product_filter = product_filter.items()
    product_filter = {}

    cache_key = "%s-category-products-%s" % (settings.CACHE_MIDDLEWARE_KEY_PREFIX, slug)
    sub_cache_key = "%s-start-%s-sorting-%s" % (settings.CACHE_MIDDLEWARE_KEY_PREFIX, start, sorting)

    filter_key = ["%s-%s" % (i[0], i[1]) for i in product_filter]
    if filter_key:
        sub_cache_key += "-%s" % "-".join(filter_key)

    price_filter = request.session.get("price-filter")
    if price_filter:
        sub_cache_key += "-%s-%s" % (price_filter["min"], price_filter["max"])

    temp = cache.get(cache_key)
    if temp is not None:
        try:
            return temp[sub_cache_key]
        except KeyError:
            pass
    else:
        temp = dict()

    category = lfs_get_object_or_404(Category, slug='home-products')

    # Calculates parameters for display.
    try:
        start = int(start)
    except (ValueError, TypeError):
        start = 1

    format_info = category.get_format_info()
    amount_of_rows = format_info["product_rows"]
    amount_of_cols = format_info["product_cols"]
    amount = amount_of_rows * amount_of_cols

    all_products = lfs.catalog.utils.get_filtered_products_for_category(
        category, product_filter, price_filter, sorting)

    # prepare paginator
    paginator = Paginator(all_products, amount)

    try:
        current_page = paginator.page(start)
    except (EmptyPage, InvalidPage):
        current_page = paginator.page(paginator.num_pages)

    # Calculate products
    row = []
    products = []
    for i, product in enumerate(current_page.object_list):
        if product.is_product_with_variants():
            default_variant = product.get_variant_for_category(request)
            if default_variant:
                product = default_variant

        image = None
        product_image = product.get_image()
        if product_image:
            image = product_image.image
        row.append({
            "obj": product,
            "slug": product.slug,
            "name": product.get_name(),
            "image": image,
            "price_unit": product.price_unit,
            "price_includes_tax": product.price_includes_tax(request),
        })
        if (i + 1) % amount_of_cols == 0:
            products.append(row)
            row = []

    if len(row) > 0:
        products.append(row)

    amount_of_products = all_products.count()

    # Calculate urls
    pagination_data = lfs_pagination(request, current_page, url=category.get_absolute_url())

    #render_template = category.get_template_name()
    #if render_template != None:
    #    template_name = render_template

    return render_to_response(template_name, RequestContext(request, {
        "category": category,
        "products": products,
        "amount_of_products": amount_of_products,
        "pagination": pagination_data,
        "all_products": all_products,
        "shop":shop
    }))

    #temp[sub_cache_key] = result
    #cache.set(cache_key, temp)

    #return result

    #home_products = gethome_products(request,slug="home-products", start=1, template_name="lfs/shop/shop.html")

    #return render_to_response(template_name, RequestContext(request, {
    #    "shop":shop,
    #    "category": home_products,
    #    "products": all_products,
    #    "amount_of_products": amount_of_products,
    #    "all_products": all_products,
    #}))

views.shop_view = shop_view
