from django.contrib import admin
from django.contrib.auth.models import User

from django.db.models import Count, Value
from django.db.models.aggregates import Sum
from django.db.models.functions import Coalesce

# Register your models here.
from .models import Movie, Review, TopPurchasingUsers
from cart.models import Item, Order


class MovieAdmin(admin.ModelAdmin):
   ordering = ['name']
   search_fields = ['name']


class TopPurchasingUsersAdmin(admin.ModelAdmin):
   list_display = ['username', 'purchase_count']
   search_fields = ['username']
   change_list_template = 'admin/purchase_count.html'

   def changelist_view(self, request, extra_context = None):
          request.GET = request.GET.copy()
          size = request.GET.pop('size', [None])[0]
          if size and size.isdigit() and int(size) > 0:
              request.size = int(size)
          else:
              request.size = None
          return super().changelist_view(request, extra_context)
       
   def get_queryset(self, request):
      queryset = self.model._default_manager.get_queryset().annotate(purchase_count = Coalesce(Sum('order__item__quantity'), Value(0)))
      size = getattr(request, 'size', None)
      if (size):
          short_list = list(queryset.order_by('-purchase_count', 'pk').values_list('pk', flat = True) [:size])
          queryset = queryset.filter(pk__in = short_list).order_by('-purchase_count', 'pk')    
    
      return queryset
   
   def get_ordering(self, request):
       return ['-purchase_count', 'pk']

   @admin.display(description="Purchase Count", ordering = 'purchase_count')
   def purchase_count(self, obj):
        return obj.purchase_count

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
admin.site.register(TopPurchasingUsers, TopPurchasingUsersAdmin)
