from django.shortcuts import render, redirect
from .models import Heroes, DateHeroes, UserDates
from django.http import JsonResponse, HttpResponseRedirect
from django.core import serializers
from .forms import HeroForm, RegisterForm, LoginForm, ChangeForm, DeleteAllForm
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
import json
import random
from numpy.random import choice, seed
from django.db.models import Sum, Avg
from django.contrib.auth import login, authenticate
from django.contrib import messages
import csv
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
# # Create your views here.


def index(request, live=True, ranked=False):
    heroes = Heroes.objects.all()
    form = HeroForm()
    regform = RegisterForm()
    logform = LoginForm()
    context = {'heroes': heroes, 'hero_form': form}
    
    attempts = request.session.get('attempts', {})
    request.session['live'] = live
    path_info = request.META.get('PATH_INFO')

    if live:
        today = datetime.utcnow().date()
        path_date = str(today)
    else:
        path_date = path_info.split('/')[-1]
        today = datetime.strptime(path_date, '%Y-%m-%d').date()

    if request.session.get('prev_page', [None, None]) != [ranked, path_date]:
        request.session['prev_page'] = [ranked, path_date]
        request.session['attempts'] = {}
        request.session['is_guessed'] = False

    is_guessed = get_is_guessed(request, path_date, path_info)
    date_word = get_hero_by_date(today, ranked, request.user.id)
    today_hero = Heroes.objects.get(Name=date_word)
    user_stats = get_user_stats(request)
    user_ranked_stats = get_user_ranked_stats(request)

    if request.method == 'POST':
        if 'hero_field' in request.POST:
            user_input = request.POST.get('hero_field')
            _a, is_guessed = check_hero(user_input, today, ranked, request.user.id)
            attempts[len(attempts)] = _a
            request.session['attempts'] = attempts
            request.session['is_guessed'] = is_guessed
            user_data(request)
            return JsonResponse({'attempts': attempts, 'is_guessed': is_guessed})
        
        elif 'email' in request.POST:
            regform = RegisterForm(request.POST)
            if regform.is_valid():
                user = regform.save()
                messages.success(request, 'You have signed up successfully.')
                login(request, user)
                return redirect('/classic')
            return JsonResponse({'success': False, 'message': 'Invalid username or password'})

    context.update({
        'attempts': attempts,
        'today_hero': today_hero,
        'regform': regform,
        'logform': logform,
        'user': request.user,
        'userdates': User.objects.all(),
        'is_guessed': is_guessed,
        'user_stats': user_stats,
        'ranked': ranked,
        'user_ranked_stats': user_ranked_stats,
    })
    return render(request, 'app/index.html', context)


def get_hero_by_date(date, ranked, uid):
    if ranked:
        return ranked_roll(date, uid)
    else:
        try:
            return DateHeroes.objects.get(Date=date).Hero
        except DateHeroes.DoesNotExist:
            populate_table(table=DateHeroes)
            return DateHeroes.objects.get(Date=date).Hero


def login_ajax(request):
    if request.method == 'POST' and 'logusername' in request.POST:
        username = request.POST['logusername']
        password = request.POST['logpassword']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Cannot find a user with these credentials'})


@login_required
def ranked(request):
    return index(request, ranked=True)


def ranked_roll(target_date, userid):
    heroes = [x.Name for x in Heroes.objects.all()]
    weights = [1/len(heroes) for x in heroes]
    seed(userid)
    first_date = datetime.strptime("2023-09-01", '%Y-%m-%d').date()
    days_needed_to_fill = (target_date - first_date).days +1
    for i in range(days_needed_to_fill):
        hero, weights = weighted_roll(heroes, weights)
    return hero


def reroll_hero(request):
    heroes = [x.Name for x in Heroes.objects.all()]
    
    hero = unweighted_roll(heroes)
    last_hero_entry = DateHeroes.objects.last()

    last_hero_entry.Hero = hero
    last_hero_entry.save()

    request.session['attempts'] = {}
    request.session['is_guessed'] = False
    context = {'reload_needed': True}
    return JsonResponse(context)


def unweighted_roll(heroes):
    random.seed(random.random())
    return random.choice(heroes)


def generate_hero(request):
    if 'ranked' in request.META.get('HTTP_REFERER'):
        reload_needed = False
    else:
        reload_needed = populate_table(table=DateHeroes)

    if reload_needed:
        request.session['attempts'] = {}
        request.session['is_guessed'] = False
    context = {'reload_needed':reload_needed}

    return JsonResponse(context)


def populate_table(table=DateHeroes, s=1693515600):
    heroes = [x.Name for x in Heroes.objects.all()]
    # s = int(time.mktime(datetime.strptime("2023-09-01", '%Y-%m-%d').date().timetuple()))
    # == 2023-09-01 in ms
    seed(s)

    weights, target_index = prepare_weights(heroes)

    # website birth date
    first_date = datetime.strptime("2023-09-01", '%Y-%m-%d').date()
    
    target_date = first_date + timedelta(days=target_index-1)

    today = datetime.utcnow().date()
    days_needed_to_fill = (today - target_date).days +1
    for i in range(days_needed_to_fill):

        hero, weights = weighted_roll(heroes, weights)

        print(f'Adding {hero} - {target_date} - {target_index}')
        new_hero_entry = table(
            id = target_index,
            Date = target_date,
            Hero = hero,
        )
        new_hero_entry.save()

        target_index += 1
        target_date += timedelta(days=1)

    return bool(days_needed_to_fill)


def prepare_weights(heroes):
    weights = [1/len(heroes) for x in heroes]
    target_index = 1
    for i in DateHeroes.objects.all():
        last_hero = i.Hero
        last_date = i.Date
        last_index = i.id
        target_index = last_index + 1
        _w = weights[heroes.index(last_hero)]
        weights = [x+_w/(len(heroes)-1) for x in weights]
        weights[heroes.index(last_hero)] = 0
        
        print(f'Used - {last_hero} - {last_date} - {last_index}')
    
    return [weights, target_index]


def weighted_roll(heroes, weights):
    hero = choice(heroes, 1, p=weights)[0]
    _w = weights[heroes.index(hero)]
    weights = [x+_w/(len(heroes)-1) for x in weights]
    weights[heroes.index(hero)] = 0

    return hero, weights


def get_heroes(request):
    heroesser = Heroes.objects.all()
    serialized_heroes = serializers.serialize('json', heroesser)
    dateheroesser = Heroes.objects.all()
    serialized_dateheroes = serializers.serialize('json', dateheroesser)
    return JsonResponse({'heroesser': serialized_heroes, 'dateheroesser': serialized_dateheroes})


def check_hero(user_input, today, ranked=False, uid=None):
    if not ranked:
        date_word = DateHeroes.objects.get(Date=today).Hero
    else:
        date_word = ranked_roll(today, uid)
    today_hero = Heroes.objects.get(Name=date_word)
    guessed_hero = Heroes.objects.get(Name=user_input)
    guessed_attributes = {}


    guessed_attributes['Name'] = guessed_hero.Name

    guessed_attributes['CodeName'] = guessed_hero.CodeName.replace('npc_dota_hero_', '')


    guessed_roles = guessed_hero.Role.split(',')
    guessed_levels = guessed_hero.Rolelevels.split(',')
    guessed_roles_group = {guessed_roles[i]: guessed_levels[i] for i in range(len(guessed_roles))}
    guessed_roles = today_hero.Role.split(',')
    guessed_levels = today_hero.Rolelevels.split(',')
    tray = {guessed_roles[i]: guessed_levels[i] for i in range(len(guessed_roles))}
    guessed_attributes['Role'] = {}
    for k,v in guessed_roles_group.items():
        if k in tray.keys():
            if v == tray[k]:
                res = 'cor'
            else:
                res = 'partial'
        else:
            res = 'incor'
        templevels = [x for x in range(int(v))]
        guessed_attributes['Role'][k] = {'Name': k, 'Rolelevels': templevels, 'style': res}
    

    if guessed_hero.Team == today_hero.Team:
        res = 'cor'
    else:
        res = 'incor'
    tempname = str(guessed_hero.Team)
    guessed_attributes['Team'] = {'Name': tempname, 'style': res}


    if guessed_hero.AttackType == today_hero.AttackType:
        res = 'cor'
    else:
        res = 'incor'
    tempname = str(guessed_hero.AttackType)
    guessed_attributes['AttackType'] = {'Name': tempname, 'style': res}


    guessed_attributes['SimilarHeroes'] = {}
    for i in guessed_hero.SimilarHeroesID.split(','):
        if i in today_hero.SimilarHeroesID.split(',') \
            or int(i) == today_hero.HeroID:
            res = 'cor'
        else:
            res = 'incor'
        if i == '0':
            tempname = 'No Information'
            _code = 'No Information'
            guessed_attributes['SimilarHeroes'][i] = {'Name': tempname, 'CodeName': _code, 'style': res} 
            break
        tempname = str(Heroes.objects.get(HeroID=i).Name)
        _code = str(Heroes.objects.get(HeroID=i).CodeName).replace('npc_dota_hero_', '')
        _position_for_js = guessed_hero.SimilarHeroesID.split(',').index(i)
        guessed_attributes['SimilarHeroes'][_position_for_js] = {'ID': i, 'Name': tempname, 'CodeName': _code, 'style': res}

    _ga = json.loads(guessed_hero.Adjectives)
    _ta = json.loads(today_hero.Adjectives)
    guessed_attributes['Adjectives'] = {}
    for k,v in _ga.items():
        if k in _ta.keys():
            if k == 'Legs' and v != _ta['Legs']:
                res = 'partial'
            else:
                res = 'cor'
        else:
            res = 'incor'

        if v == '0' and k in ['Legs', 'Nose']:
            tempname = f'No {k}'
        elif k == 'Legs':
            tempname = f'{v} {k}'
        else:
            tempname = f'{k}'
        guessed_attributes['Adjectives'][k] = {'Name': tempname, 'style': res}



    guessed_attributes['AttributePrimary'] = {}
    if today_hero.AttributePrimary == guessed_hero.AttributePrimary:
        res = 'cor'
    else:
        res = 'incor'
    tempname = guessed_hero.AttributePrimary.replace('DOTA_ATTRIBUTE_', '').replace('ALL', 'UNIVERSAL').replace('INTELLECT', 'INTELLIGENCE').capitalize() 
    guessed_attributes['AttributePrimary'] = {'Name': tempname, 'style': res}
    

    csv_file_path = 'attempts.csv'
    header = ['id', 'target', 'attempt'] 

    with open(csv_file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        lines = list(reader)
        if len(lines) > 0:
            last_line = lines[-1]
            first_value = int(last_line[0])
            if last_line[1] != today_hero.Name \
                or last_line[1] == last_line[2]:
                first_value += 1
        else:
            first_value = 0

    with open(csv_file_path, 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if csvfile.tell() == 0:
            writer.writerow(header)

        writer.writerow([first_value, today_hero.Name, guessed_hero.Name])


    return [guessed_attributes, guessed_hero.HeroID == today_hero.HeroID]


def classic_by_date(request, date):
    try:
        requested_date = datetime.strptime(date, '%Y-%m-%d').date()
        DateHeroes.objects.get(Date=requested_date)
        if 'prev_page' not in request.session.keys() \
            or (request.session['prev_page'][1] != date) \
            or (request.session['prev_page'][0] is True):
            request.session['prev_page'] = [False, date]
            request.session['attempts'] = {}
            request.session['is_guessed'] = False
        return index(request, live = False)
    except DateHeroes.DoesNotExist:
        return HttpResponseRedirect('/classic/')


@login_required
def ranked_by_date(request, date):
    if 'prev_page' not in request.session.keys() \
        or (request.session['prev_page'][1] != date) \
        or (request.session['prev_page'][0] is False): 
        request.session['prev_page'] = [True, date]
        request.session['attempts'] = {}
        request.session['is_guessed'] = False
    return index(request, live = False, ranked = True)


def get_date_range(request):
    first = DateHeroes.objects.first().Date
    last = DateHeroes.objects.last().Date
    return JsonResponse({'first': first, 'last': last})


def get_day_mod(request):
    day = request.META.get('HTTP_REFERER').split('/')[-1]
    mod = request.META.get('HTTP_REFERER').split('/')[3]
    if day == '':
        day = str(datetime.utcnow().date())
    return [day, mod]


@login_required
def user_data(request):
    day_mod = get_day_mod(request)
    date_heroes = DateHeroes.objects.all()
    users = User.objects.all()
    date = date_heroes.get(Date=day_mod[0])
    current_user = users.get(username=request.user)
    today_hero = date_heroes.filter(Date=day_mod[0])[0].Hero
    current_data = UserDates.objects.filter(user_id=current_user.id, date=date)
    if not current_data:
        if request.session['attempts'][0]['Name'] == today_hero and day_mod[1] == 'classic':
            new_userdata = UserDates(user_id=current_user, date=date, classic_isguessed=True, classic_attempts=1, ranked_isguessed=False, ranked_attempts=0)
            new_userdata.save()
        elif request.session['attempts'][0]['Name'] == today_hero and day_mod[1] == 'ranked':
            new_userdata = UserDates(user_id=current_user, date=date, classic_isguessed=False, classic_attempts=0, ranked_isguessed=True, ranked_attempts=1)
            new_userdata.save()
        elif request.session['attempts'][0]['Name'] != today_hero and day_mod[1] == 'classic':
            new_userdata = UserDates(user_id=current_user, date=date, classic_isguessed=False, classic_attempts=1, ranked_isguessed=False, ranked_attempts=0)
            new_userdata.save()
        elif request.session['attempts'][0]['Name'] != today_hero and day_mod[1] == 'ranked':
            new_userdata = UserDates(user_id=current_user, date=date, classic_isguessed=False, classic_attempts=0, ranked_isguessed=False, ranked_attempts=1)
            new_userdata.save()
    else:
        if day_mod[1] == 'classic' and current_data[0].classic_isguessed is False:
            old_userdata = current_data
            user_data = old_userdata[0]
            print(user_data.classic_attempts)
            user_data.classic_attempts += 1
            if(request.session['attempts'][list(request.session['attempts'].keys())[-1]]['Name'] == today_hero):
                user_data.classic_isguessed = True
            user_data.save()

        elif day_mod[1] == 'ranked' and current_data[0].ranked_isguessed is False:
            old_userdata = UserDates.objects.filter(user_id=current_user.id, date=date)
            old_userdata[0].ranked_attempts+=1
            if(request.session['attempts'][list(request.session['attempts'].keys())[-1]]['Name'] == today_hero):
                old_userdata[0].ranked_isguessed = True
            old_userdata[0].save()


@login_required
def get_is_guessed(request, path_date, path_info):
    mod = path_info.split('/')[1]
    if mod == 'classic':
        try:
            return UserDates.objects.filter(date_id=DateHeroes.objects.get(Date=path_date), user_id_id=request.user)[0].classic_isguessed
        except IndexError:
            return False
    elif mod == 'ranked':
        try:
            return UserDates.objects.filter(date_id=DateHeroes.objects.get(Date=path_date), user_id_id=request.user)[0].ranked_isguessed
        except IndexError:
            return False


@login_required
def get_user_stats(request):
    userdates = UserDates.objects.filter(user_id_id=request.user) 
    total_attempts = userdates.aggregate(Sum('classic_attempts'))['classic_attempts__sum']
    total_attempts = total_attempts if total_attempts is not None else 0
    userdates_true = UserDates.objects.filter(user_id_id=request.user, classic_isguessed=True)
    avg_attempts =  round(userdates_true.aggregate(avg_attempts=Avg('classic_attempts'))['avg_attempts'], 1) if userdates_true.aggregate(avg_attempts=Avg('classic_attempts'))['avg_attempts'] is not None else 0
    heroes_guessed = len(userdates_true)
    userdates_oneshot = UserDates.objects.filter(user_id_id=request.user, classic_isguessed=True, classic_attempts=1) 
    oneshots = len(userdates_oneshot)
    return [avg_attempts, total_attempts, heroes_guessed, oneshots]


@login_required
def get_user_ranked_stats(request):
    userdates = UserDates.objects.filter(user_id_id=request.user) 
    total_ranked_attempts = userdates.aggregate(Sum('ranked_attempts'))['ranked_attempts__sum']
    total_ranked_attempts = total_ranked_attempts if total_ranked_attempts is not None else 0
    userdates_ranked_true = UserDates.objects.filter(user_id_id=request.user, ranked_isguessed=True)
    avg_ranked_attempts =  round(userdates_ranked_true.aggregate(avg_attempts=Avg('ranked_attempts'))['avg_attempts'], 1) if userdates_ranked_true.aggregate(avg_attempts=Avg('ranked_attempts'))['avg_attempts'] is not None else 0
    heroes_ranked_guessed = len(userdates_ranked_true)
    userdates_ranked_oneshot = UserDates.objects.filter(user_id_id=request.user, ranked_isguessed=True, ranked_attempts=1) 
    oneshots = len(userdates_ranked_oneshot)
    return [avg_ranked_attempts, total_ranked_attempts, heroes_ranked_guessed, oneshots]


def leaderboard(request):
    if str(request.user) != 'AnonymousUser':
        user_stats = get_user_stats(request)
        user_ranked_stats = get_user_ranked_stats(request)
        context = {
            'user_stats':user_stats,
            'user_ranked_stats':user_ranked_stats
        }
    else:
        regform = RegisterForm()
        logform = LoginForm() 
        context = {'regform':regform, 'logform': logform}
    return render(request, 'app/leaderboard.html', context)


def profile(request):
    user = request.user
    regform = RegisterForm()
    logform = LoginForm() 
    if str(user)!= 'AnonymousUser':
        changeform = ChangeForm(initial = {'changeusername': user.username, 'changeemail':user.email})
        delform = DeleteAllForm()
        if request.method == 'POST' and 'deleteall' in request.POST:
            message = request.POST.get('deleteall')
            if message == 'I want to delete my account':
                User.objects.get(username=user.username).delete()
                return redirect('/classic')
        if request.method == 'POST' and 'changeusername' in request.POST:
            newusername = request.POST.get('changeusername') if request.POST.get('changeusername') else None
            newemail = request.POST.get('changeemail') if request.POST.get('changeemail') else None
            newpassword = request.POST.get('changenewpassword') if request.POST.get('changenewpassword') else None
            userdata = User.objects.get(username=user.username)
            if newusername:
                userdata.username = newusername
            if newemail:
                userdata.email = newemail
            if newpassword:
                userdata.password = make_password(newpassword)
            userdata.save()
        context = {
            'changeform':changeform,
            'delform':delform,
        }
    else:
        context = {'regform':regform, 'logform': logform}
    return render(request, 'app/profile.html', context)
