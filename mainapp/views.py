from django.db.models import Avg
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from mainapp import services
from mainapp.forms import RegisterUserForm, ReviewForm
from django.views.generic import ListView
from mainapp.models import Player, ReviewRating
import random
from django.forms import formset_factory
from datetime import timedelta, date
from django.contrib import messages
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from mainapp.serializers import ReviewRatingSerializer, PlayerSerializer

MENU = [
    {'title': 'Home', 'url_name': '/'},
    {'title': 'About', 'url_name': 'about'},
    {'title': 'Contacts', 'url_name': 'contact'},
]

MESSAGE_TAGS = {
    messages.INFO: '',
    messages.SUCCESS: '',
}


class PlayerColumn(ListView):
    """ Main page of the cite. Class shows all players on the one page. """
    paginate_by = 13
    model = Player
    template_name = 'index.html'
    context_object_name = 'player'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = MENU
        context['title'] = 'Home'
        context['cat_selected'] = 0
        context['avg_rating'] = services.avg_rating()  # Gets dict from avg_rating().
        if self.request.user.is_anonymous is False:
            # Gets dict from services.in_four_days().
            context['in_four_days'] = services.in_four_days(user=self.request.user)
            # Gets date from services.in_seven_days().
            context['in_seven_days'] = services.in_seven_days(user=self.request.user)
            context['now'] = date.today()
            context['position'] = self.request.GET.get("sort")  # Gets position by sort.
            context['count_players'] = range(0, len(Player.objects.all()))  # For numbering players.
        return context

    def get_queryset(self):
        queryset = Player.objects.all()
        sort_by = self.request.GET.get("sort")
        if sort_by is not None:
            queryset = Player.objects.filter(position=sort_by)
        # Return sorted queryset of players.
        return queryset


class SignUp(CreateView):
    """ Registration. """
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def user_details_after(strategy, details, user=None, *args, **kwargs):
    """ Show message after login with Google. """
    if not user:
        messages.info(strategy.request, "You are logged in with Google.")


@receiver(user_logged_out)
def on_user_logged_out(sender, request, **kwargs):
    """ Signal --> User has been logged out. Show message. """
    messages.info(request, 'You are logged out.')


def create_choice(request, player_id):
    """ Form for making a vote for chosen player. """
    user = request.user
    player = Player.objects.get(id=player_id)
    if request.method == "POST":
        x = ReviewRating.objects.filter(user_id=user, player_id=player_id, is_random_choice=False).last()
        # Check if there is any data in X.
        # If X is not None: check if four days have passed.
        if x is None or date.today() >= x.created_on + timedelta(4):
            # Fill the form.
            form = ReviewForm(request.POST)
            fs = form.save(commit=False)
            fs.user = user
            fs.player = player
            # Save the form.
            fs.save()
            # Show message after redirect.
            messages.add_message(request, messages.SUCCESS, 'Thanks for your vote!')
            return redirect('/')
        else:
            # Show message after redirect.
            messages.add_message(request, messages.INFO, 'You have already voted for this player.')
            return redirect('/')
    else:
        form = ReviewForm()
        return render(request, "makechoice.html", {
            'form': form, 'player': player, 'menu': MENU, 'title': 'Voting'
        })


def random_choice(request):
    """ Form for making a random vote. """
    user = request.user
    players_list = list(Player.objects.all())
    random_players = random.sample(players_list, 3)
    # Making more than one form.
    review_form_set = formset_factory(ReviewForm, extra=0)  # Making more than one form.
    formset = review_form_set(request.POST, initial=[{'player': x.id} for x in random_players])
    if request.method == 'POST':
        last_date = ReviewRating.objects.filter(user_id=request.user, is_random_choice=True).last()
        now = date.today()
        # Check if there is any data in last_date.
        # If last_date is not None: check if seven days have passed.
        if last_date is None or now >= last_date.created_on + timedelta(7):
            for form in formset.forms:
                # Fill the form.
                fs = form.save(commit=False)
                fs.user = user
                fs.player = form.cleaned_data.get('player')
                fs.is_random_choice = True
                # Save the form.
                fs.save()
            # Show message after redirect.
            messages.add_message(request, messages.SUCCESS, 'Thanks for your vote!')
            return redirect('/')
        else:
            # Show message after redirect.
            messages.add_message(request, messages.INFO, 'You cannot re-vote for random players within one week.')
            return redirect('/')
    else:
        formset = review_form_set(initial=[{'player': x.id} for x in random_players])
        return render(request, 'randomchoice.html', context={
            'formset': formset,
            'menu': MENU,
            'random_players': random_players,
            'packed': zip(formset, random_players),
            'title': 'Random choice'
        })


class PlayersList(ListAPIView):
    """ Representing all players with their teams, positions and id. """
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()


class AverageRatingList(APIView):
    """ Representing all player with their current average rating. """
    permission_classes = (IsAuthenticated, )

    def get(self, request, **kwargs):
        x = []
        y = None
        # Check if is there a position in the body of the request.
        if kwargs:
            # If there is.
            y = Player.objects.filter(position=self.kwargs['position'])
        else:
            # If there is not.
            y = Player.objects.all()

        for player in y:
            health = ReviewRating.objects.filter(player=player).aggregate(avg=Avg('health'))
            speed = ReviewRating.objects.filter(player=player).aggregate(avg=Avg('speed'))
            body_strength = ReviewRating.objects.filter(player=player).aggregate(avg=Avg('body_strength'))
            strength_environment = ReviewRating.objects.filter(player=player).aggregate(avg=Avg('strength_environment'))
            talent = ReviewRating.objects.filter(player=player).aggregate(avg=Avg('talent'))

            x.append({'player': player.name,
                      'health': health.get('avg'),
                      'speed': speed.get('avg'),
                      'body_strength': body_strength.get('avg'),
                      'strength_environment': strength_environment.get('avg'),
                      'talent': talent.get('avg')
                      })

        results = ReviewRatingSerializer(x, many=True).data
        return Response(results)
