from django.db.models import F
from django.contrib.auth.views import LoginView
from django.db.models import Avg
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from mainapp.forms import RegisterUserForm, LoginUserForm, ReviewForm
from django.views.generic import ListView
from mainapp.models import Player, ReviewRating
import random
from django.forms import formset_factory
from django.template.defaulttags import register
from datetime import timedelta, date
from django.contrib import messages


MENU = [
    {'title': 'Главная', 'url_name': '/'},
    {'title': 'O сайте', 'url_name': 'about'},
    {'title': 'Контакты', 'url_name': 'contact'},
]
#test comment

MESSAGE_TAGS = {
    messages.INFO: '',
    messages.SUCCESS: '',
}


class PlayerColumn(ListView):
    paginate_by = 13
    model = Player
    template_name = 'index.html'
    context_object_name = 'player'

    @register.filter
    def get_item(dictionary, key):
        return dictionary.get(key)

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = MENU
        context['title'] = 'Главная страница'
        context['cat_selected'] = 0
        context['avg_rating'] = self.avg_rating()
        if self.request.user.is_anonymous is False:
            context['in_four_days'] = self.in_four_days(self.request)
            context['in_seven_days'] = self.in_seven_days(self.request)
            context['now'] = date.today()
            context['position'] = self.request.GET.get("sort")
            context['count_players'] = range(0, len(Player.objects.all()))
        return context

    def get_queryset(self):
        queryset = Player.objects.all()
        sort_by = self.request.GET.get("sort")
        if sort_by is not None:
            queryset = Player.objects.filter(position=sort_by)
        return queryset

    def in_four_days(self, request):
        in_four_days = {}
        for player in Player.objects.all():
            x = ReviewRating.objects.filter(user=request.user, player=player, is_random_choice=False).last()
            if x is not None:
                in_four_days[player.id] = x.created_on + timedelta(4)
            else:
                in_four_days[player.id] = None
        return in_four_days

    def in_seven_days(self, request):
        any_record = ReviewRating.objects.filter(user_id=self.request.user, is_random_choice=True).exists()
        if any_record is True:
            user = request.user
            last_random = ReviewRating.objects.filter(user_id=user, is_random_choice=True).last()
            seven_days = timedelta(7)
            in_seven_days = last_random.created_on + seven_days
            return in_seven_days
        else:
            return None

    def avg_rating(self):
        avg_rating = {}
        for player in Player.objects.all():
            total = ReviewRating.objects.filter(player=player).aggregate(
                avg=Avg((F('health') + F('speed') + F('body_strength') + F('strength_environment') + F('talent')) / 5)
            )
            if total.get('avg') is not None:
                avg_rating[player.id] = round(total.get('avg'), 1)
            else:
                avg_rating[player.id] = 0
        return avg_rating


class SignUp(CreateView):
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class Login(LoginView):
    form_class = LoginUserForm
    template_name = 'registration/login.html'


def create_choice(request, player_id):
    user = request.user
    player = Player.objects.get(id=player_id)
    if request.method == "POST":
        x = ReviewRating.objects.filter(user_id=user, player_id=player_id, is_random_choice=False).last()
        if x is None or date.today() >= x.created_on + timedelta(4):
            form = ReviewForm(request.POST)
            fs = form.save(commit=False)
            fs.user = user
            fs.player = player
            fs.save()
            messages.add_message(request, messages.SUCCESS, 'Спасибо за Ваш голос!')
            return redirect('/')
        else:
            messages.add_message(request, messages.INFO, 'Вы уже голосовали за этого игрока.')
            return redirect('/')
    else:
        form = ReviewForm()
        return render(request, "makechoice.html", {
            'form': form, 'player': player, 'menu': MENU, 'title': 'Голосование'
        })


def random_choice(request):
    user = request.user
    players_list = list(Player.objects.all())
    random_players = random.sample(players_list, 3)
    review_form_set = formset_factory(ReviewForm, extra=0)
    formset = review_form_set(request.POST, initial=[{'player': x.id} for x in random_players])
    if request.method == 'POST':
        last_date = ReviewRating.objects.filter(user_id=request.user, is_random_choice=True).last()
        now = date.today()
        if last_date is None or now >= last_date.created_on + timedelta(7):
            for form in formset.forms:
                fs = form.save(commit=False)
                fs.user = user
                fs.player = form.cleaned_data.get('player')
                fs.is_random_choice = True
                fs.save()
            messages.add_message(request, messages.SUCCESS, 'Спасибо за Ваш голос!')
            return redirect('/')
        else:
            messages.add_message(request, messages.INFO, 'Вы не можете повторно голосовать за'
                                                         ' рандомных игроков в течении одной недели')
            return redirect('/')
    else:
        formset = review_form_set(initial=[{'player': x.id} for x in random_players])
        return render(request, 'randomchoice.html', context={
            'formset': formset,
            'menu': MENU,
            'random_players': random_players,
            'packed': zip(formset, random_players),
            'title': 'Рандомный выбор'
        })
