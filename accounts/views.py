from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
from .models import CustomUser


def register_view(request):
    """Страница регистрации"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} успешно создан!')
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """Страница входа"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        user = None
        
        # Сначала пробуем аутентифицировать по username
        if username:
            user = authenticate(request, username=username, password=password)
        
        # Если не нашли по username, пробуем по email
        if user is None and username:
            try:
                user_obj = CustomUser.objects.get(email=username)
                user = authenticate(request, username=user_obj.username, password=password)
            except CustomUser.DoesNotExist:
                pass
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Неверный логин или пароль')
            form = UserLoginForm()
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """Выход из системы"""
    from django.contrib.auth import logout
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы')
    return redirect('login')


@login_required
def home_view(request):
    """Главная страница"""
    return render(request, 'accounts/home.html')
