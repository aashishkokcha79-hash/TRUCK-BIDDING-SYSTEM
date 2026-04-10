from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegistrationForm, RequirementForm, BidForm
from .models import UserProfile, TransporterProfile, Requirement, Bid
import random

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/home.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            user_type = form.cleaned_data['user_type']
            contact_number = form.cleaned_data.get('contact_number', '')
            
            UserProfile.objects.create(user=user, user_type=user_type, contact_number=contact_number)
            
            if user_type == 'Transporter':
                TransporterProfile.objects.create(
                    user=user,
                    transporter_name=form.cleaned_data.get('transporter_name'),
                    vehicle_number=form.cleaned_data.get('vehicle_number'),
                    current_latitude=20.5937 + random.uniform(-1.0, 1.0),
                    current_longitude=78.9629 + random.uniform(-1.0, 1.0)
                )
            messages.success(request, f"Account created for {user.username}!")
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()
    return render(request, 'core/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    user_type = getattr(request.user, 'profile', None)
    if not user_type:
        return redirect('home')
        
    if user_type.user_type == 'Customer':
        return redirect('customer_dashboard')
    elif user_type.user_type == 'Transporter':
        return redirect('transporter_dashboard')
    return redirect('home')

def customer_dashboard(request):
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'Customer':
        return redirect('home')

    if request.method == 'POST':
        form = RequirementForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.customer = request.user
            req.save()
            messages.success(request, "Requirement posted successfully.")
            return redirect('customer_dashboard')
    else:
        form = RequirementForm()

    requirements = request.user.requirements.all().order_by('-created_at')
    
    return render(request, 'core/customer_dashboard.html', {
        'form': form,
        'requirements': requirements
    })

def requirement_detail(request, req_id):
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'Customer':
        return redirect('home')
    
    requirement = get_object_or_404(Requirement, id=req_id, customer=request.user)
    bids = requirement.bids.all().order_by('amount')
    
    lowest_bid = bids.first() if bids.exists() else None

    # Logic to auto-select winner if manually triggered
    if request.method == 'POST':
        if 'accept_bid' in request.POST:
            bid_id = request.POST.get('accept_bid')
            bid_to_accept = get_object_or_404(Bid, id=bid_id)
            requirement.winning_bid = bid_to_accept
            requirement.status = 'Closed'
            requirement.save()
            messages.success(request, f"Accepted bid of {bid_to_accept.amount} from {bid_to_accept.transporter.username}!")
            return redirect('requirement_detail', req_id=requirement.id)

    return render(request, 'core/requirement_detail.html', {
        'requirement': requirement,
        'bids': bids,
        'lowest_bid': lowest_bid
    })

def transporter_dashboard(request):
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'Transporter':
        return redirect('home')

    if request.method == 'POST' and 'place_bid' in request.POST:
        form = BidForm(request.POST)
        req_id = request.POST.get('requirement_id')
        req = get_object_or_404(Requirement, id=req_id, status='Open')
        
        if form.is_valid():
            # Check if transporter already placed a bid
            existing_bid = Bid.objects.filter(requirement=req, transporter=request.user).first()
            if existing_bid:
                existing_bid.amount = form.cleaned_data['amount']
                existing_bid.save()
                messages.success(request, "Bid updated successfully.")
            else:
                bid = form.save(commit=False)
                bid.transporter = request.user
                bid.requirement = req
                bid.save()
                messages.success(request, "Bid placed successfully.")
            return redirect('transporter_dashboard')

    open_requirements = Requirement.objects.filter(status='Open').order_by('-created_at')
    # attach transporter's bid to each requirement if it exists
    my_bids = {b.requirement_id: b for b in Bid.objects.filter(transporter=request.user)}
    
    for req in open_requirements:
        req.my_bid = my_bids.get(req.id)

    won_requirements = Requirement.objects.filter(
        status='Closed', 
        winning_bid__transporter=request.user
    ).order_by('-created_at')

    bid_form = BidForm()

    return render(request, 'core/transporter_dashboard.html', {
        'open_requirements': open_requirements,
        'won_requirements': won_requirements,
        'bid_form': bid_form
    })
