from rest_framework import serializers
from mainapp.models import ReviewRating, Player


class PlayerSerializer(serializers.ModelSerializer):
    """ Serializer for models.Player """
    class Meta:
        model = Player
        fields = '__all__'


class ReviewRatingSerializer(serializers.ModelSerializer):
    """ Serializer for models.ReviewRating """
    # For getting player from models.Players.
    player = serializers.CharField(max_length=40)

    class Meta:
        model = ReviewRating
        fields = ('player', 'health', 'speed', 'body_strength', 'strength_environment', 'talent')

    def to_representation(self, instance):
        my_fields = {'health', 'speed', 'body_strength', 'strength_environment', 'talent'}
        data = super().to_representation(instance)
        # Check if any field in 'fields' returns 'None' --> show that player does not have data yet.
        for field in my_fields:
            if not data[field]:
                #  Return empty data if no votes yet.
                return {
                    'player': data['player'],
                    'data': {}
                }
            else:
                # Data filled with average rating by metrics.
                return ({'player': data['player'],
                         'data': {
                             'health': data['health'],
                             'speed': data['speed'],
                             'body_strength': data['body_strength'],
                             'strength_environment': data['strength_environment'],
                             'talent': data['talent'],
                         }})
        return data
