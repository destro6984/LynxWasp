from django.contrib import admin


from product_manager_ices.models import Ices, Flavour, OrderItem, Order

admin.site.register(Ices)
admin.site.register(Flavour)

admin.site.register(OrderItem)
admin.site.register(Order)