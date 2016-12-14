from collections import defaultdict
from decimal import Decimal
from app.ladder.models import Player, MatchPlayer
from dal import autocomplete
from django.db.models import Max, Count, Prefetch, Case, When, F, ExpressionWrapper, FloatField
from django.views.generic import ListView, DetailView


class PlayerList(ListView):
    # those who played at least 1 game
    # TODO make active players manager
    queryset = Player.objects.exclude(name__in=['hoxieloxie'])\
        .filter(matchplayer__isnull=False).distinct()

    def get_context_data(self, **kwargs):
        context = super(PlayerList, self).get_context_data(**kwargs)
        players = context['player_list']

        players = players or Player.objects.all()

        players = players.prefetch_related(Prefetch(
            'matchplayer_set',
            queryset=MatchPlayer.objects.select_related('match'),
            to_attr='matches'
        )).annotate(
            match_count=Count('matchplayer'),
            wins=Count(Case(
                When(
                    matchplayer__team=F('matchplayer__match__winner'), then=1)
                )
            ),
            winrate=ExpressionWrapper(
                F('wins') * Decimal('100') / F('match_count'),
                output_field=FloatField()
            )
        )

        max_vals = players.aggregate(Max('mmr'), Max('score'), Max('ladder_mmr'))
        score_max = max_vals['score__max']
        mmr_max = max_vals['mmr__max']
        ladder_mmr_max = max_vals['ladder_mmr__max']

        matches_max = max(player.match_count for player in players)
        matches_max = max(matches_max, 1)

        for player in players:
            player.score_percent = float(player.score) / score_max * 100
            player.mmr_percent = float(player.mmr) / mmr_max * 100
            player.ladder_mmr_percent = float(player.ladder_mmr) / ladder_mmr_max * 100
            player.matches_percent = float(player.match_count) / matches_max * 100

        context.update({
            'player_list': players,
        })

        return context


class PlayerOverview(DetailView):
    model = Player
    context_object_name = 'player'
    slug_field = 'slug__iexact'

    def get_context_data(self, **kwargs):
        context = super(PlayerOverview, self).get_context_data(**kwargs)

        player = self.object

        matches = player.matchplayer_set.all()
        wins = sum(1 if m.match.winner == m.team else 0 for m in matches)
        losses = len(matches) - wins

        win_percent = 0
        if matches:
            win_percent = float(wins) / len(matches) * 100

        score_changes = player.scorechange_set.all()

        # calc score history
        score = mmr = 0
        for scoreChange in reversed(score_changes):
            score += scoreChange.amount
            mmr += scoreChange.mmr_change

            scoreChange.score = score
            scoreChange.mmr = mmr

        context.update({
            'wins': wins,
            'losses': losses,
            'winrate': win_percent,
            'match_list': matches,
            'score_changes': score_changes,
        })

        return context


class PlayerAutocomplete(autocomplete.Select2QuerySetView):
    queryset = Player.objects.order_by('name')