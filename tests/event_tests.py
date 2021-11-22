import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import GameType, Game, Gamer, Event


class EventTests(APITestCase):
    def setUp(self):
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }
        # Initiate request and capture response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Store the auth token
        self.token = json_response["token"]

        # Assert that a user was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        game_type = GameType()
        game_type.label = "Board game"
        game_type.save()

        self.game = Game.objects.create(
            game_type=game_type,
            title="Monopoly",
            maker="Hasbro",
            gamer_id=1,
            number_of_players=5,
            skill_level=2
        )

        gamer = Gamer.objects.get(user=1)
        self.gamer = gamer

    def test_retrieve_event(self):

        event = Event.objects.create(
            date="2021-11-11",
            time="12:00:00",
            description="Describe",
            game_id=1,
            organizer_id=1
        )

        url = f"/events/{event.id}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], event.id)
        self.assertEqual(response.data['date'], event.date)
        self.assertEqual(response.data['time'], event.time)
        self.assertEqual(response.data['description'], event.description)
        self.assertEqual(response.data['organizer']['id'], event.organizer.id)

    def test_create_event(self):

        data = {
            "date": "2021-12-23",
            "time": "12:00:00",
            "description": "Xmas Eve Eve",
            "gameId": self.game.id
        }

        url = "/events"
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response['date'], data['date'])
        self.assertEqual(json_response['time'], data['time'])
        self.assertEqual(json_response['description'], data['description'])
        self.assertEqual(json_response['game']['id'], data['gameId'])

    def test_delete_event(self):
        event = Event.objects.create(
            date="2021-11-11",
            time="12:00:00",
            description="Describe",
            game_id=1,
            organizer_id=1
        )

        url = f"/events/{event.id}"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_event(self):
        event = Event.objects.create(
            date="2021-11-11",
            time="12:00:00",
            description="Describe",
            game_id=1,
            organizer_id=1
        )

        data = {
            "date": "2021-11-11",
            "time": "12:00:00",
            "description": "Description",
            "game_id": 1,
            "organizer_id": 1
        }
        url = f"/events/{event.id}"
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        response = self.client.get(f'/events/{event.id}')
        json_response = json.loads(response.content)
        self.assertEqual(json_response['date'], data['date'])
        self.assertEqual(json_response['time'], data['time'])
        self.assertEqual(json_response['description'], data['description'])

    def test_join_event(self):
        # TODO: Test joining an event method
        event = Event.objects.create(
            organizer_id=1,
            game=self.game,
            time="12:30:00",
            date="2021-12-23",
            description="Game night"
        )
        # Assert that no one is in the event list, the length should be 0
        self.assertEqual(len(event.attendees.all()), 0)

        response = self.client.post(f'/events/{event.id}/signup')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # After the post runs assert that the attendees length is 1
        self.assertEqual(len(event.attendees.all()), 1)
        
    def test_leave_events(self):
        event = Event.objects.create(
            organizer_id=1,
            game=self.game,
            time="12:30:00",
            date="2021-12-23",
            description="Game night"
        )
        # Add a gamer to the attendees
        gamer = Gamer.objects.get(pk=1)
        event.attendees.add(gamer)

        response = self.client.delete(f'/events/{event.id}/signup')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(event.attendees.all()), 0)