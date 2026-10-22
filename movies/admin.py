from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models.aggregates import Sum
from django.db.models.functions import Coalesce
# Register your models here.
from .models import Movie, Review, TopPurchasingUsers
from cart.models import Item, Order

class MovieAdmin(admin.ModelAdmin):
  ordering = ['name']
  search_fields = ['name']

class TopPurchasingUsersAdmin(admin.ModelAdmin):
    change_list_template = 'admin/purchase_count.html'
    list_display = ['username', 'purchase_count']
    search_fields = ['username']

    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        request.top_size = request.GET.pop("size", [None])[0]
        return super().changelist_view(request, extra_context)

    def get_queryset(self, request):
        qs = super().get_queryset(request).annotate(
            total_purchases=Sum("order__item__quantity")
        ).order_by("-total_purchases", "pk")

        size = getattr(request, "top_size", None)
        if size and size.isdigit() and int(size) > 0:
            top_ids = list(qs.values_list("pk", flat=True)[:int(size)])
            qs = qs.filter(pk__in=top_ids)   
        return qs

    def purchase_count(self, obj):
        return obj.total_purchases or 0
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
admin.site.register(TopPurchasingUsers, TopPurchasingUsersAdmin)