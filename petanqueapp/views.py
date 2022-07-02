from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from petanqueapp.models import Player, Match, Round, Tournament
from petanqueapp.forms import MatchForm

# Create your views here.
def index(request):
    print('connected!')
    tournament = Tournament.objects.latest('id')
    players = tournament.get_leaderboard()
    leaderboard = tournament.get_leaderboard()
    round = Round.objects.filter(tournament = tournament).last()
    matches = Match.objects.filter(round = round)
    scheduled_matches = []
    finished_matches = []
    for m in matches:
        if m.status == 'Scheduled':
            scheduled_matches.append(m)
        else:
            finished_matches.append(m)

    context = {
        'tournament':tournament,
        'players':players,
        'scheduled_matches':scheduled_matches,
        'finished_matches':finished_matches,
    }

    if len(scheduled_matches) == 0:
        context['end_of_round'] = 1

    if request.method == "POST":
        if "Næste Runde" in request.POST:
            print('næste runde')
            tournament.pair_round()
        else:
            print('submit match')
            player1score = request.POST.get('player1score')
            player2score = request.POST.get('player2score')
            player3score = request.POST.get('player3score')
            match_id = request.POST.get('submit-button')
            winner = Match.objects.get(id=match_id)
            winner.end_match(player1score, player2score, player3score)
        return redirect("/")

    return render(request, 'petanqueapp/index.html', context)
