from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from .models import user, CustomUser, Transaction
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib import auth
import random
from .forms import EditProfileForm
from django.contrib.auth.decorators import login_required


def generate_account_number():
    return random.randint(100000000000, 999999999999)


def register_form(request):
    return render(request, 'register.html')


def registerView(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        account_no = generate_account_number()

        image = request.FILES.get('image', None)

        address = request.POST.get('address')
        username = request.POST.get('username')
        email = request.POST.get('email')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        adharcard = request.POST.get('adharcard')
        pancard = request.POST.get('pancard')
        initial_amount = request.POST.get('initial_amount')

        password = request.POST.get('password')
        password = make_password(password)

        while user.objects.filter(account_no=account_no).exists():
            account_number = generate_account_number()
        custom_user = CustomUser.objects.create(username=username, email=email, password=password)

        user_profile = user.objects.create(user_id=custom_user, name=name, account_no=account_no, image=image,
                                           address=address, age=age, phone=phone, dob=dob, adharcard=adharcard,
                                           pancard=pancard, initial_amount=initial_amount)
        user_profile.save()
        messages.success(request, "account created successfully")
        return redirect('home')
    else:
        messages.error(request, "registration failed. try again")
        return redirect('regform')


def login_form(request):
    return render(request, 'login.html')


def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_admin or user.is_superuser:
                return redirect('dashboard')
            elif user.is_banker:
                return redirect('banker')
            else:
                return redirect('customer')
        else:
            messages.info(request, "invalid username and password")
            return redirect('home')


# ---------------------------------------------------------------------------------------------------#
@login_required
def customer_view(request):
    try:
        customer_details = user.objects.get(user_id=request.user)
        transactions = Transaction.objects.filter(custom_id=customer_details)
        latest_balance = transactions.latest('dateandtime').balance if transactions.exists() else 0

    except user.DoesNotExist:
        customer_details = None
        transactions = None
        latest_balance = 0

    context = {
        'customer': customer_details,
        'transactions': transactions,
        'latest_balance': latest_balance,
    }

    return render(request, 'customer.html', context)


def deposit_view(request):
    user1 = user.objects.get(user_id=request.user)
    if request.method == 'POST':
        account_no = request.POST.get('accountnumber')
        branch = request.POST.get('branch')
        amount = int(request.POST.get('amount'))

        try:
            matched_user = user.objects.get(account_no=account_no)
        except user.DoesNotExist:
            return render(request, 'deposit.html', {'error': 'Account number does not exist', 'data': user1})

        if amount < 100:
            return render(request, 'deposit.html', {'error': 'Amount must be greater than 100', 'data': user1})
        else:
            matched_user.initial_amount += amount
            matched_user.save()

            transaction = Transaction.objects.create(custom_id=matched_user, amount=amount, details='credit',
                                                     branch=branch, bank_name='SBI', ifsc_code="SBICO156789",
                                                     balance=matched_user.initial_amount)
            transaction.save()
            return redirect('history')
    else:
        return render(request, 'deposit.html', {'data': user1})


def withdraw_view(request):
    user1 = user.objects.get(user_id=request.user)
    if request.method == 'POST':
        account_no = request.POST.get('accountnumber')
        branch = request.POST.get('branch')
        amount = int(request.POST.get('amount'))

        try:
            matched_user = user.objects.get(account_no=account_no)
        except user.DoesNotExist:
            return render(request, 'withdraw.html', {'error': 'Account number does not exist', 'data': user1})

        if amount < 100:
            return render(request, 'withdraw.html', {'error': 'Amount must be greater than 100', 'data': user1})
        else:
            matched_user.initial_amount -= amount
            matched_user.save()

            transaction = Transaction.objects.create(custom_id=matched_user, amount=amount, branch=branch,
                                                     details='debit', balance=matched_user.initial_amount)
            transaction.save()
            return redirect('history')
    else:
        return render(request, 'withdraw.html', {'data': user1})


def history(request):
    customer_details = user.objects.get(user_id=request.user)
    user_transactions = Transaction.objects.filter(custom_id=customer_details)
    return render(request, 'history.html', {'transactions': user_transactions})


def profile(request, pk):
    pro = get_object_or_404(user, id=pk)  # Fetch the specific user by their ID
    context = {
        'pro': pro
    }
    return render(request, 'profile.html', context)


def moreinfo(request):
    try:
        customer_details = user.objects.get(user_id=request.user)
        transactions = Transaction.objects.filter(custom_id=customer_details)
        latest_balance = transactions.latest('dateandtime').balance if transactions.exists() else 0

    except user.DoesNotExist:
        customer_details = None
        transactions = None
        latest_balance = 0

    context = {
        'customer': customer_details,
        'transactions': transactions,
        'latest_balance': latest_balance,
    }
    return render(request, 'moreinfo.html', context)


def edit_profile(request, pk):
    pro = get_object_or_404(user, id=pk)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES,
                               instance=pro)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=pro.id)
    else:
        form = EditProfileForm(instance=pro)

    context = {
        'form': form,
        'pro': pro,
    }
    return render(request, 'edit_profile.html', context)


# ----------------------------------------------------------------------------------------------------------------#
def logoutView(request):
    logout(request)
    return redirect('home')


def banker_view(request):
    custom = CustomUser.objects.all().count()
    context = {"custom": custom}
    return render(request, 'banker.html', context)


def view_user(request):
    custom = user.objects.all()
    context = {"custom": custom}
    return render(request, 'view_user.html', context)


