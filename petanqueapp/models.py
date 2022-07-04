from django.db import models

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=256, unique=True, default='NoName')
    match_points = models.IntegerField(default=0)
    matches_played = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    opp_score = models.IntegerField(default=0)
    byes = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Tournament(models.Model):
    players = models.ManyToManyField(Player)

    def get_player_list(self):
        return self.players.all()

    def get_leaderboard(self):
        leaderboard = []
        for p in self.get_player_list():
            leaderboard.append([p, p.match_points, p.total_points, p.opp_score])
        leaderboard.sort(key=lambda x:x[3], reverse=True)
        leaderboard.sort(key=lambda x:x[2], reverse=True)
        leaderboard.sort(key=lambda x:x[1], reverse=True)
        leaderboard = [leaderboard[i][0] for i in range(len(leaderboard))]
        return leaderboard

    def pair_round(self):
        round = Round(tournament = self)
        round.save()
        leaderboard = self.get_leaderboard()
        while len(leaderboard)%3 != 0:
            p = leaderboard.pop()
            p.match_points +=1
            p.matches_played +=1
            p.byes +=1
            p.save()
        while len(leaderboard) > 0:
            p1 = leaderboard.pop(0)
            p2 = leaderboard.pop(0)
            p3 = leaderboard.pop(0)
            m = Match(player1 = p1, player2 = p2, player3 = p3, round = round)
            m.save()


class Round(models.Model):
    status = models.CharField(max_length=256, default='In Progress')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

class Match(models.Model):
    status = models.CharField(max_length=256, default='Scheduled')
    player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name = 'player1')
    player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name = 'player2')
    player3 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name = 'player3')
    player1score = models.IntegerField(default=0)
    player2score = models.IntegerField(default=0)
    player3score = models.IntegerField(default=0)
    round = models.ForeignKey(Round, on_delete = models.CASCADE, related_name = 'round')


    def end_match(self, score1, score2, score3):
        try:
            score1 = int(score1)
        except ValueError:
            score1 = 0

        try:
            score2 = int(score2)
        except ValueError:
            score2 = 0

        try:
            score3 = int(score3)
        except ValueError:
            score3 = 0

        self.status = 'Finished'
        self.player1score = score1
        self.player1.matches_played += 1
        self.player1.total_points += score1
        self.player1.opp_score += (score2 + score3)
        self.player2score = score2
        self.player2.matches_played += 1
        self.player2.total_points += score2
        self.player2.opp_score += (score1 + score3)
        self.player3score = score3
        self.player3.matches_played += 1
        self.player3.total_points += score3
        self.player3.opp_score += (score1 + score2)
        if score1 > max(score2, score3):
            self.player1.match_points += 1
            self.winner = self.player1.name
        elif score2 > max(score1, score3):
            self.player2.match_points += 1
            self.winner = self.player2.name
        else:
            self.player3.match_points +=1
            self.winner = self.player3.name
        self.save()
        self.player1.save()
        self.player2.save()
        self.player3.save()

    def __str__(self):
        return f'{self.player1} vs. {self.player2} vs. {self.player3}'
