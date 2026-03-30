from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('products:product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('products:product_list')
    return redirect('products:product_list')

def register_view(request):
    # Placeholder for registration logic
    return render(request, 'accounts/register.html')

@login_required
def profile_view(request):
    # This matches the 'profile' name in your urls.py
    return render(request, 'accounts/profile.html', {'user': request.user})