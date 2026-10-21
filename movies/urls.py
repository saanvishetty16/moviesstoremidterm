from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='movies.index'),
    path('<int:id>/', views.show, name='movies.show'),
    path('<int:id>/review/create/', views.create_review,
        name='movies.create_review'),
    path('<int:id>/review/<int:review_id>/edit/',
        views.edit_review, name='movies.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/', views.delete_review, name='movies.delete_review'),
    path('clear/', views.clear, name='cart.clear'),
    path('<int:id>/review/<int:review_id>/report/', views.report_review, name='movies.report_review'),
    path('<int:id>/rate/', views.make_rating, name="movies.make_rating"),
]
