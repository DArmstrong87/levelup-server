from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from levelupapi.models import Game, Event, Gamer
from django.contrib.auth import get_user_model

@api_view(['GET'])
def user_profile(request):
    """Handle GET requests to profile resource

    Returns:
        Response -- JSON representation of user info and events
    """
    gamer = Gamer.objects.get(user=request.auth.user)
    # events = Event.objects.all()
    
    # TODO: Use the django orm to filter events if the gamer is attending the event
    # attending = 
    attending = gamer.attending.all()
    hosting = gamer.event_set.all()

    # TODO: Use the orm to filter events if the gamer is hosting the event

    attending = EventSerializer(
        attending, many=True, context={'request': request})
    hosting = EventSerializer(
        hosting, many=True, context={'request': request})
    gamer = GamerSerializer(
        gamer, many=False, context={'request': request})

    # Manually construct the JSON structure you want in the response
    profile = {
        "gamer": gamer.data,
        "attending": attending.data,
        "hosting": hosting.data
    }

    return Response(profile)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for gamer's related Django user"""
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username')


class GamerSerializer(serializers.ModelSerializer):
    """JSON serializer for gamers"""
    user = UserSerializer(many=False)

    class Meta:
        model = Gamer
        fields = ('user', 'bio')


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    class Meta:
        model = Game
        fields = ('title',)


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""
    game = GameSerializer(many=False)

    class Meta:
        model = Event
        fields = ('id', 'game', 'description', 'date', 'time')