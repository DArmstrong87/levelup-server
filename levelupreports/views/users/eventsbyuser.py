"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from levelupreports.views.helpers import dict_fetch_all


class UserEventList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all games along with the gamer first name, last name, and id
            db_cursor.execute("""
                SELECT
                e.date,
                e.time,
                u.first_name || " " || u.last_name as full_name,
                g.id as gamer_id,
                ga.title as game_title
                FROM levelupapi_event e
                JOIN levelupapi_eventgamer eg on e.id = eg.event_id
                JOIN levelupapi_gamer g on eg.gamer_id = g.id
                JOIN auth_user u on u.id = g.user_id
                JOIN levelupapi_game ga on e.game_id = ga.id
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            events_with_gamer = []

            for row in dataset:
                event = {
                    'game_title': row['game_title'],
                    'date': row['date'],
                    'time': row['time']
                }

                # This is using a generator comprehension to find the user_dict in the games_by_user list
                # The next function grabs the dictionary at the beginning of the generator, if the generator is empty it returns None
                # This code is equivalent to:
                # user_dict = None
                # for user_game in games_by_user:
                #     if user_game['gamer_id'] == row['gamer_id']:
                #         user_dict = user_game

                user_dict = next(
                    (user_event for user_event in events_with_gamer
                     if user_event['gamer_id'] == row['gamer_id']),
                    None
                )

                if user_dict:
                    user_dict['events'].append(event)
                else:

                    events_with_gamer.append({
                        "gamer_id": row['gamer_id'],
                        "full_name": row['full_name'],
                        "events": [event]
                    })

        # The template string must match the file name of the html template
        template = 'users/events_with_gamer.html'

        # The context will be a dictionary that the template can access to show data
        context = {
            "user_events": events_with_gamer
        }

        return render(request, template, context)
