from multiprocessing import context
from django.shortcuts import render, redirect
# models
from .models import *
# forms
from .forms import *
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
# filter
from .filters import *
# messages
from django.contrib import messages
# groups
from django.contrib.auth.models import Group
# login 
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
# decorators
from .decorators import unauthenticated_user, allowed_user, admin_only

# Create your views here.

@unauthenticated_user
def register_page(request):
    form = CustomUserRegistrationForm()
    
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            name = first_name + last_name
            # user gets added to user group
            group = Group.objects.get(name='user')
            user.groups.add(group)
            messages.success(request, 'Account was created for ' + name)
            return redirect('user:login_page')
    
    context = {'form': form}
    return render(request, 'user/register.html', context)

@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        group =CustomUser.objects.filter(groups=1,) 
            

        if user is not None:
            auth_login(request, user)

            dateTimeObj = datetime.now()
            today = dateTimeObj.strftime("%Y-%m-%d")   
            user = request.user.id
            if user in group:
                try:
                    orgs = Profile.objects.filter(user__id=user, birth_date=today)
                    orgs2 = Profile.objects.filter( birth_date=today, weight=None, phone_number=None, shoe_size=None) 
                    if not orgs:
                        Profile.objects.create(user_id=user)
                        print('Need to profile register')
                        return redirect('user:profile_create')
                    if orgs2:
                        print('Profile is empty')
                        return redirect('user:profile_create')
                except:
                    print('Dont need to profile register')

                messages.success(request,  'Successfully logged in.')
                return redirect('user:home_page')
            elif user not in group:
                messages.success(request,  'Successfully logged in.')
                return redirect('user:home_page')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'user/login.html', context)

@login_required(login_url='user:login_page')
def profile_create_page(request):
    user = Profile.objects.get(user_id=request.user.id)
    form = ProfileRegisteForm(instance=user)
    birthday = request.POST.get('birth_date')
    
    if request.method == 'POST':
        form = ProfileRegisteForm(request.POST, instance=user)
        if form.is_valid() and birthday!=today:
            form.save()
            print(form.cleaned_data)
            return redirect('user:home_page')
        
    context = {'form': form, 'birthday':birthday}
    return render(request, 'user/profile_registration.html', context)

@login_required(login_url='user:login_page')
def home_page(request):
    user =CustomUser.objects.filter(groups=2) 
    permission = False
    if request.user in user:
        permission = True
    context = {'user': user, 'permission': permission,}
    return render(request, 'user/home.html', context)

def logoutUser(request):
    logout(request)
    return redirect('user:login_page')

@login_required(login_url='user:login_page')
@allowed_user(allowed_roles=['admin'])
def profile_page(request):
    profiles = Profile.objects.all()
    users = CustomUser.objects.all()

    profileFilter = ProfileFilter(request.GET, queryset=profiles)
    profiles = profileFilter.qs 

    context = {'profiles': profiles, 'users': users,'profileFilter':profileFilter}
    return render(request, 'user/profile.html',context)

@login_required(login_url='user:login_page')
def profile_update_page(request, pk):
    user = Profile.objects.get(user_id=pk)
    form = ProfileRegisteForm(instance=user)
    
    
    if request.method == 'POST':
        form = ProfileRegisteForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            print(form.cleaned_data)
            return redirect('user:profile_detail', pk)
        
    context = {'form': form}
    return render(request, 'user/profile_registration.html', context)

@login_required(login_url='user:login_page')
def profile_detail(request,pk):
    profile = Profile.objects.get(user_id=pk)
    profileform = ProfileRegisteForm(instance=request.user)

    context = {'form': profileform, 'profile':profile}

    return render(request, 'user/profile_detail.html', context)

@login_required(login_url='user:login_page')
def account_page(request):
    user = request.user.id
    user = CustomUser.objects.get(pk=user)
    context = {'user': user}
    return render(request, 'user/account.html', context)

@login_required(login_url='user:login_page')
def account_update(request):
    form = CustomUserChangeForm(instance=request.user)
    if request.method == 'POST':
        form = CustomUserChangeForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Info Updated.')
            return redirect('user:account_page')
    context = {'form': form}
    return render(request, 'user/account_update.html', context)

@login_required(login_url='user:login_page')
def change_password(request):
    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password changed successfully.')
            return redirect('user:account_page')

    context = {'form': form, }

    return render(request, 'user/change_password.html', context)

def device_page(request):
    form = DataBaseForm(request.POST)
    if request.method == 'POST':
        form = DataBaseForm(request.POST, )
        if form.is_valid():
            form.save()
            messages.success(request, 'Entry Submitted successfully.')
    datas = DeviceData.objects.filter(user_id=request.user.id).order_by('-time')
    count =DeviceData.objects.filter(user_id=request.user.id).count()
    context = {'form': form, 'datas': datas, 'count': count}
    return render(request, 'user/device.html', context)

def data_page(request):
    datas = DeviceData.objects.filter(date=today, user_id=request.user.id)
    print()
    datafilter = DeviceDataFilter(request.GET, queryset=datas)
    datas = datafilter.qs
    a0000 = DeviceData.objects.filter(time__range=['00:00:00', '01:00:00']).count()
    a0100 = DeviceData.objects.filter(time__range=['01:00:00', '02:00:00']).count()
    a0200 = DeviceData.objects.filter(time__range=['02:00:00', '03:00:00']).count()
    a0300 = DeviceData.objects.filter(time__range=['03:00:00', '03:00:00']).count()
    a0400 = DeviceData.objects.filter(time__range=['04:00:00', '05:00:00']).count()
    a0500 = DeviceData.objects.filter(time__range=['05:00:00', '05:00:00']).count()
    a0600 = DeviceData.objects.filter(time__range=['06:00:00', '07:00:00']).count()
    a0700 = DeviceData.objects.filter(time__range=['07:00:00', '08:00:00']).count()
    a0800 = DeviceData.objects.filter(time__range=['08:00:00', '09:00:00']).count()
    a0800 = DeviceData.objects.filter(time__range=['08:00:00', '09:00:00']).count()
    a0900 = DeviceData.objects.filter(time__range=['09:00:00', '10:00:00']).count()
    a1000 = DeviceData.objects.filter(time__range=['10:00:00', '11:00:00']).count()
    a1100 = DeviceData.objects.filter(time__range=['11:00:00', '12:00:00']).count()
    a1200 = DeviceData.objects.filter(time__range=['12:00:00', '13:00:00']).count()
    a1300 = DeviceData.objects.filter(time__range=['13:00:00', '14:00:00']).count()
    a1400 = DeviceData.objects.filter(time__range=['14:00:00', '15:00:00']).count()
    a1500 = DeviceData.objects.filter(time__range=['15:00:00', '16:00:00']).count()
    a1600 = DeviceData.objects.filter(time__range=['16:00:00', '17:00:00']).count()
    a1700 = DeviceData.objects.filter(time__range=['17:00:00', '18:00:00']).count()
    a1800 = DeviceData.objects.filter(time__range=['18:00:00', '19:00:00']).count()
    a1900 = DeviceData.objects.filter(time__range=['19:00:00', '20:00:00']).count()
    a2000 = DeviceData.objects.filter(time__range=['20:00:00', '21:00:00']).count()
    a2100 = DeviceData.objects.filter(time__range=['21:00:00', '22:00:00']).count()
    a2200 = DeviceData.objects.filter(time__range=['22:00:00', '23:00:00']).count()
    a2300 = DeviceData.objects.filter(time__range=['23:00:00', '00:00:00']).count()

    context = { 'datas': datas, 
                'a0000': a0000, 
                'a0100': a0100, 
                'a0200':a0200, 
                'a0300':a0300,
                'a0400':a0400,
                'a0500':a0500,
                'a0600':a0600,
                'a0700':a0700,
                'a0800':a0800,
                'a0900':a0900,
                'a1000':a1000,
                'a1100':a1100,
                'a1200':a1200,
                'a1300':a1300,
                'a1400':a1400,
                'a1500':a1500,
                'a1600':a1600,
                'a1700':a1700,
                'a1800':a1800,
                'a1900':a1900,
                'a2000':a2000,
                'a2100':a2100,
                'a2200':a2200,
                'a2300':a2300,
                'datafilter':datafilter
                }
    return render(request, 'user/data.html', context)

def data_delete(request, pk):
    pass

def admin_data(request):
    datas = DeviceData.objects.all()
    datafilter = AdminDataFilter(request.GET, queryset=datas)
    datas = datafilter.qs
    a0000 = datas.filter(time__range=['00:00:00', '01:00:00']).count()
    a0100 = datas.filter(time__range=['01:00:00', '02:00:00']).count()
    a0200 = datas.filter(time__range=['02:00:00', '03:00:00']).count()
    a0300 = datas.filter(time__range=['03:00:00', '03:00:00']).count()
    a0400 = datas.filter(time__range=['04:00:00', '05:00:00']).count()
    a0500 = datas.filter(time__range=['05:00:00', '05:00:00']).count()
    a0600 = datas.filter(time__range=['06:00:00', '07:00:00']).count()
    a0700 = datas.filter(time__range=['07:00:00', '08:00:00']).count()
    a0800 = datas.filter(time__range=['08:00:00', '09:00:00']).count()
    a0800 = datas.filter(time__range=['08:00:00', '09:00:00']).count()
    a0900 = datas.filter(time__range=['09:00:00', '10:00:00']).count()
    a1000 = datas.filter(time__range=['10:00:00', '11:00:00']).count()
    a1100 = datas.filter(time__range=['11:00:00', '12:00:00']).count()
    a1200 = datas.filter(time__range=['12:00:00', '13:00:00']).count()
    a1300 = datas.filter(time__range=['13:00:00', '14:00:00']).count()
    a1400 = datas.filter(time__range=['14:00:00', '15:00:00']).count()
    a1500 = datas.filter(time__range=['15:00:00', '16:00:00']).count()
    a1600 = datas.filter(time__range=['16:00:00', '17:00:00']).count()
    a1700 = datas.filter(time__range=['17:00:00', '18:00:00']).count()
    a1800 = datas.filter(time__range=['18:00:00', '19:00:00']).count()
    a1900 = datas.filter(time__range=['19:00:00', '20:00:00']).count()
    a2000 = datas.filter(time__range=['20:00:00', '21:00:00']).count()
    a2100 = datas.filter(time__range=['21:00:00', '22:00:00']).count()
    a2200 = datas.filter(time__range=['22:00:00', '23:00:00']).count()
    a2300 = datas.filter(time__range=['23:00:00', '00:00:00']).count()

    context = { 'datas': datas, 
                'a0000': a0000, 
                'a0100': a0100, 
                'a0200':a0200, 
                'a0300':a0300,
                'a0400':a0400,
                'a0500':a0500,
                'a0600':a0600,
                'a0700':a0700,
                'a0800':a0800,
                'a0900':a0900,
                'a1000':a1000,
                'a1100':a1100,
                'a1200':a1200,
                'a1300':a1300,
                'a1400':a1400,
                'a1500':a1500,
                'a1600':a1600,
                'a1700':a1700,
                'a1800':a1800,
                'a1900':a1900,
                'a2000':a2000,
                'a2100':a2100,
                'a2200':a2200,
                'a2300':a2300,
                'datafilter':datafilter
                }
    return render(request, 'user/admin_data.html', context)