from .models import Category
def menu_links(request):
   links = Category.objects.all() # need all the category
   return {'links': links} # return like link = home , page like ntaht act as key and value pair



