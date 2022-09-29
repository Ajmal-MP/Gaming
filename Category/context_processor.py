from .models import Categories,SubCategories
from Product.models import Product
def menu_links(request):
    category_links = Categories.objects.all()
    brand_links = Product.objects.all()
    return {'category_links':category_links,'brand_links':brand_links}