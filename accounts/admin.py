from django.contrib import admin
from django.db.models import Count
from django.db.models import Sum
from django.http import HttpRequest
from .models import TopCustomer

@admin.register(TopCustomer)
class TopCustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'movies_purchased')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        queryset = queryset.annotate(
            total_movies=Sum("order__item__quantity")
        ).order_by("-total_movies", "pk")

        top_customer = queryset.first()

        if top_customer:
            return queryset.filter(pk=top_customer.pk)

        return queryset.none()
    
    @admin.display(description="Movies Purchased")
    def movies_purchased(self, obj):
        return obj.total_movies
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request):
        return False
    
    def has_change_permission(self, request):
        return False




