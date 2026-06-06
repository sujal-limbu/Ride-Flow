from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from .models import Vehicle, VehicleImage,Review


def index(request):
    return render(request, 'core/home.html')

def profile(request):
    return render(request, 'core/profile.html')

@login_required
def vehicle_list(request):
    vehicles = Vehicle.objects.prefetch_related('images').all()

    if request.GET.get('name'):
        vehicles = vehicles.filter(name__icontains=request.GET['name'])
    if request.GET.get('location'):
        vehicles = vehicles.filter(location_name__icontains=request.GET['location'])
    if request.GET.get('min_price'):
        vehicles = vehicles.filter(price_per_day__gte=request.GET['min_price'])
    if request.GET.get('max_price'):
        vehicles = vehicles.filter(price_per_day__lte=request.GET['max_price'])

    return render(request, 'core/vehicle_list.html', {'vehicles': vehicles})

@login_required
def add_vehicle(request):
    if request.method == 'POST':
        vehicle = Vehicle.objects.create(
            owner         = request.user,
            name          = request.POST.get('name'),
            vehicle_type  = request.POST.get('vehicle_type'),
            year          = request.POST.get('year'),
            price_per_day = request.POST.get('price_per_day'),
            description   = request.POST.get('description'),
            latitude      = request.POST.get('latitude'),
            longitude     = request.POST.get('longitude'),
            location_name = request.POST.get('location_name'),
        )
        for image in request.FILES.getlist('images'):
            VehicleImage.objects.create(vehicle=vehicle, image=image)
        return redirect('vehicle_list')

    return render(request, 'core/add_vehicle.html')


@login_required
def edit_vehicle(request, id):
    vehicle = get_object_or_404(Vehicle, id=id, owner=request.user)

    if request.method == 'POST':
        vehicle.name          = request.POST.get('name')
        vehicle.vehicle_type  = request.POST.get('vehicle_type')
        vehicle.year          = request.POST.get('year')
        vehicle.price_per_day = request.POST.get('price_per_day')
        vehicle.description   = request.POST.get('description')
        vehicle.latitude      = request.POST.get('latitude')
        vehicle.longitude     = request.POST.get('longitude')
        vehicle.location_name = request.POST.get('location_name')
        vehicle.save()

        for image in request.FILES.getlist('images'):
            VehicleImage.objects.create(vehicle=vehicle, image=image)

        return redirect('vehicle_detail', id=vehicle.id)

    return render(request, 'core/edit_vehicle.html', {'vehicle': vehicle})


@login_required
def delete_vehicle(request, id):
    vehicle = get_object_or_404(Vehicle, id=id, owner=request.user)
    vehicle.delete()
    return redirect('vehicle_list')


def vehicle_detail(request, id):
    vehicle = get_object_or_404(Vehicle, id=id)
    images  = vehicle.images.all()
    reviews = vehicle.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    avg_rating = round(avg_rating, 1)

    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()

    # Handle review submission
    if request.method == 'POST' and 'submit_review' in request.POST:
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to leave a review.')
            return redirect('login')

        if user_review:
            messages.error(request, 'You have already reviewed this vehicle.')
        else:
            rating  = request.POST.get('rating')
            comment = request.POST.get('comment', '').strip()

            if rating and rating.isdigit() and 1 <= int(rating) <= 5:
                Review.objects.create(
                    vehicle = vehicle,
                    user    = request.user,
                    rating  = int(rating),
                    comment = comment,
                )
                messages.success(request, 'Review submitted successfully!')
                return redirect('vehicle_detail', id=id)
            else:
                messages.error(request, 'Please select a star rating.')

    return render(request, 'core/vehicle_detail.html', {
        'vehicle':      vehicle,
        'images':       images,
        'reviews':      reviews,
        'avg_rating':   avg_rating,
        'review_count': reviews.count(),
        'user_review':  user_review,
    })


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    vehicle_id = review.vehicle.id
    review.delete()
    messages.success(request, 'Review deleted.')
    return redirect('vehicle_detail', id=vehicle_id)


def my_bookings(request):
    return render(request, 'core/my_bookings.html')