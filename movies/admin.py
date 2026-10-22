from django.contrib import admin
from django.db.models import Count, Sum, Max
from django.urls import path
from django.template.response import TemplateResponse


# Register your models here.
from .models import Movie, Review, PopularMovie

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

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