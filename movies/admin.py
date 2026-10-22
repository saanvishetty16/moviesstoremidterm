from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import Count

# Register your models here.
from .models import Movie, Review, MostCommenter

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

class CommentEngagementAdmin(admin.ModelAdmin):
   list_display = ('username', 'number_of_comments_posted')
   def get_queryset(self, request):
       queryset = super().get_queryset(request)
       queryset= queryset.annotate(comment_count=Count("review")).filter(comment_count__gt=0).order_by("-comment_count", "pk")


       most_commenter = queryset.first()
       if most_commenter is not None:
        return queryset.filter(pk=most_commenter.pk)
    
       return queryset.none()


   def number_of_comments_posted(self, obj):
       return obj.comment_count
  
   def has_add_permission(self, request):
       return False
  
   def has_delete_permission(self, request):
       return False
  
   def has_change_permission(self, request):
       return False


admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
admin.site.register(MostCommenter, CommentEngagementAdmin)
