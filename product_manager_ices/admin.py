from django.contrib import admin


from product_manager_ices.models import Ices, Flavour, OrderItem

admin.site.register(Ices)
admin.site.register(Flavour)

admin.site.register(OrderItem)
