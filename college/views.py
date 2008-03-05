from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.syndication.feeds import Feed
from operator import itemgetter
from fumblerooski.recruits.models import SchoolType, City, School, Player, Outcome, Signing, Year
from fumblerooski.college.models import Coach, College, CollegeCoach, Position, State, Game, Conference

def conference_index(request):
    conference_list = Conference.objects.all().order_by('name')
    return render_to_response('college/conferences.html', {'conference_list': conference_list})

def conference_detail(request, conf):
    c = get_object_or_404(Conference, abbrev=conf)
    team_list = College.objects.filter(conference=c).order_by('name')
    recent_games = Game.objects.filter(team1__conference=c, team2__conference=c).order_by('-date')[:10]
    return render_to_response('college/conference_detail.html', {'conference': c, 'team_list': team_list, 'recent_games':recent_games })

def team_index(request):
    team_list = College.objects.all().order_by('name')
    return render_to_response('college/teams.html', {'team_list': team_list})

def team_vs(request, team1, team2):
    team_1 = get_object_or_404(College, slug=team1)
    try:
        team_2 = College.objects.get(slug=team2)
        if team_1 == team_2:
            team_2 = None
    except:
        team_2 = None
    games = Game.objects.filter(team1=team_1, team2=team_2).order_by('-date')
    try:
        last_home_loss = games.filter(t1_game_type='H', t1_result='L')[0]
    except:
        last_home_loss = None
    try:
        last_road_win = games.filter(t1_game_type='A', t1_result='W')[0]
    except:
        last_road_win = None
    return render_to_response('college/team_vs.html', {'team_1': team_1, 'team_2': team_2, 'games': games, 'last_home_loss': last_home_loss, 'last_road_win': last_road_win })

def game(request, team1, team2, year):
    team_1 = get_object_or_404(College, slug=team1)
    try:
        team_2 = College.objects.get(slug=team2)
        if team_1 == team_2:
            team_2 = None
    except:
        team_2 = None
    game = Game.objects.get(team1=team_1, team2=team_2, season=year)
    if game.season > 2002:
        game.drivechart = True
    return render_to_response('college/game.html', {'team_1': team_1, 'team_2': team_2, 'game': game })

def game_index(request):
    pass # do calendar-based view here