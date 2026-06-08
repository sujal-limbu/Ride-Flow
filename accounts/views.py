from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import DashBoard
from .forms import ProfilePictureForm

User = get_user_model()

# Registration View
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Password Validation
        if password1 != password2:
            messages.error(request, "Passwords did not match")
            return redirect('register')

        # Check User Exist or not
        if User.objects.filter(username=username).exists():
            messages.error(request, "User already exists")
            return redirect('register')

        # Saving User info to DB
        User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            password=password1,
        )
        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'accounts/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')  # stay on login, not index

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def dashboard_info(request):
    if request.method == 'POST':
        if request.POST.get('remove_picture'):
            if request.user.profile_picture:
                request.user.profile_picture.delete(save=False)
                request.user.profile_picture = None
                request.user.save()
            return redirect('dashboard')

        # Upload new picture
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfilePictureForm(instance=request.user)

    context = {'form': form}
    return render(request, 'accounts/dashboard.html', context)

@login_required
def delete_dashboard(request, pk):
    dashboard = get_object_or_404(DashBoard, id=pk, user=request.user)  # Security: only own images
    dashboard.delete()
    return redirect('dashboard')   # Redirect back to dashboard