from otree.api import *

author = "Arpit Kaur"

doc = """
Simple Trust Game
"""


class Constants(BaseConstants):
    name_in_url = 'my_trust'
    players_per_group = 2
    num_rounds = 1

    endowment = cu(10)
    multiplication_factor = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    sent_amount = models.CurrencyField(
        label="How much do you want to send to participant B?",
        min=cu(0),
        max=Constants.endowment
    )
    sent_back_amount = models.CurrencyField(
        label="How much do you want to send back?"
    )

    def sent_back_amount_choices(group):
        return currency_range(
            cu(0),
            group.sent_amount * Constants.multiplication_factor,
            cu(1)
        )


def set_payoffs(group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = Constants.endowment - group.sent_amount + group.sent_back_amount
    p2.payoff = group.sent_amount * Constants.multiplication_factor - group.sent_back_amount


class Player(BasePlayer):
    pass


# PAGES
class Send(Page):
    form_model = 'group'
    form_fields = ['sent_amount']

    # only player 1 sees this page
    def is_displayed(player):
        return player.id_in_group == 1


class WaitForP1(WaitPage):
    pass


class Sendback(Page):
    form_model = 'group'
    form_fields = ['sent_back_amount']

    def is_displayed(player):
        return player.id_in_group == 2
        # only player 2 sees this page

    def vars_for_template(player):
        group = player.group

        return dict(
            tripled_amount=group.sent_amount * Constants.multiplication_factor
        )


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    pass


page_sequence = [
    Send,
    WaitForP1,
    Sendback,
    ResultsWaitPage,
    Results,
]