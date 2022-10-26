from django.contrib import admin
from .models import *


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'position', 'team')
    list_display_links = ('name',)
    search_fields = ('name',)


class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'player', 'user', 'health', 'speed',
        'body_strength', 'strength_environment', 'talent', 'created_on'
    )
    list_display_links = ('player',)


admin.site.register(Player, PlayerAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)
