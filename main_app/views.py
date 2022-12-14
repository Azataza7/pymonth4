from django.shortcuts import render, HttpResponse, Http404, redirect
from .forms import FilmCreateForm, UserCreateForm, LoginForm
from main_app.models import Film, Comments, Category
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def general_page(request):
    return HttpResponse('<h4> Main page </h4>')


def about_us_view(request):
    return render(request, 'about_us.html')


PAGE_SIZE = 8


def films_view(request):
    page = int(request.GET.get('page', 1))
    movie_list = Film.objects.all()
    movie_per_page = movie_list[PAGE_SIZE * (page-1):PAGE_SIZE * page]
    if movie_list.count() % PAGE_SIZE == 0:
        count_button = movie_list.count() // PAGE_SIZE
    else:
        count_button = movie_list.count() // PAGE_SIZE + 1
    context = {
        'title': 'Movies',
        'movie_list': movie_per_page,
        'next': page + 1,
        'next_disabled': 'disabled' if page >= count_button else '',
        'previous': page - 1,
        'previous_disabled': 'disabled' if page == 1 else '',
        'page': page,
        'categories': Category.objects.all(),
        'buttons': [i for i in range(1, count_button + 1)],
    }
    return render(request, 'films.html', context=context)


def film_item_view(request, id):
    detail = Film.objects.get(id=id)
    if request.method == 'GET':
        context = {
            'film_id': detail,
            'comments': Comments.objects.filter(films_id=id)
        }
        return render(request, 'detail.html', context=context)
    else:
        text = request.POST.get('text')
        rate_user = request.POST.get('rate_user')
        Comments.objects.create(
            text=text,
            rate_user=rate_user,
            films_id=id,
        )

        return redirect(f'/films/{id}/')


def category_films_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except:
        raise Http404()
    context = {
        'title': category.title,
        'movie_list': Film.objects.filter(category_id=id),
        'categories': Category.objects.all()
    }
    return render(request, 'films.html', context=context)


@login_required(login_url='/login/')
def create_film_view(request):
    if request.method == 'GET':
        context = {
            'form': FilmCreateForm()
        }
        return render(request, 'add_film.html', context=context)
    else:
        form = FilmCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/add_film/')
        return render(request, 'add_film.html', context={
            'form': form
        })


def register_view(request):
    context = {
        'form': UserCreateForm()
    }
    if request.method == 'POST':
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, password=password,
                                     email=email, is_active=True)
            return redirect('/login/')
        else:
            context = {
                'form': form
            }
    return render(request, 'register.html', context=context)


def login_view(request):
    context = {
        'form': LoginForm()
    }
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('/films/')
            return redirect('/login/')
    return render(request, 'login.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('/films/')


def search_view(request):
    search = request.GET.get('search_word', '')
    movie_list = Film.objects.filter(Q(title__icontains=search)
                                     | Q(title__icontains=search))
    context = {
        'title': 'Results of search' if movie_list else 'Films not found',
        'movie_list': movie_list,
        'categories': Category.objects.all()
    }
    return render(request, 'search.html', context=context)
