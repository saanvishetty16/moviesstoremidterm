from django.contrib import admin
from django.db.models import Count, Sum, Max
from django.urls import path
from django.template.response import TemplateResponse
from django.contrib.auth.models import User


# Register your models here.
from .models import Movie, Review, PopularMovie, MostCommenter

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

@admin.register(PopularMovie)
class PopularMovieAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path('', self.admin_site.admin_view(self.popular_movie_view))]
        return my_urls + urls

    def popular_movie_view(self, request):
        bought = Movie.objects.annotate(total=Sum('item__quantity'))
        reviewed = Movie.objects.annotate(total=Count('review'))

        top_bought = bought.aggregate(top=Max('total'))['top']
        top_reviewed = reviewed.aggregate(top=Max('total'))['top']

        most_purchased = (bought.filter(total=top_bought).order_by('name')) if top_bought else bought.none()
        most_reviewed = (reviewed.filter(total=top_reviewed).order_by('name')) if top_reviewed else reviewed.none()

        context = {
        'title': 'Popular Movies',
        'opts': self.model._meta,
        'most_purchased': most_purchased,
        'most_reviewed': most_reviewed,
        }
        return TemplateResponse(request, 'admin/movies/popularmovies/popular_movies.html', context)
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request):
        return False
    
    def has_change_permission(self, request):
        return False

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
admin.site.register(MostCommenter, CommentEngagementAdmin)
