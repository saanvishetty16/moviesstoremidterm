from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Rating
from django.contrib.auth.decorators import login_required
from django.db.models import Avg



# Create your views here.

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    user_rating_object = Rating.objects.filter(movie=movie, user=request.user).first()
    user_rating_value = user_rating_object.rating if user_rating_object else None
    avg_rating_dict = Rating.objects.filter(movie=movie).aggregate(Avg('rating'))
    avg_rating = avg_rating_dict['rating__avg']
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    template_data['user_rating'] = user_rating_value
    template_data['avg_rating'] = round(avg_rating, 2) if avg_rating else "No ratings yet"
    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def make_rating(request, id):
    movie = Movie.objects.get(id=id)
    if request.method == 'POST':
        print("Data:", request.POST)
        rating_value =  request.POST.get("rating")
        print("rating val:", rating_value)
        if rating_value:
            Rating.objects.update_or_create(
                movie = movie,
                user = request.user,
                defaults = {'rating': int(rating_value)}
            )
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment']!= '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)


@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)


@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

def clear(request):
    request.session['cart'] = {}
    return redirect('cart.index')

@login_required
def report_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    return redirect('movies.show', id=id)