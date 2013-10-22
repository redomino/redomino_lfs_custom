from django.template import Library
from lfs.page.models import Page

register = Library()

@register.inclusion_tag('lfs/footer/footer.html', takes_context=True)
def lfs_footer(context):
    from lfs.caching.utils import lfs_get_object_or_404
    try:
        page = lfs_get_object_or_404(Page, slug='footer-text')
        if page and page.active:
            return {
                    "page": page,
                   }
    except:
        return False

