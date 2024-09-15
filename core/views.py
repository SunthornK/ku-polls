from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


def signup(request):
    """Register a new user."""
    if request.method == 'POST':
        print("POST data:", request.POST)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            print(f"User created: {username}")
            user = authenticate(username=username, password=password)
            if user is not None:
                print(f"Authenticated user: {user}")
                login(request, user)
                return redirect('polls:index')
            else:
                print("Authentication failed")
        else:
            print("Form errors:", form.errors)
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
