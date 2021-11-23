SELECT * FROM levelupapi_gametype;

SELECT * FROM auth_user;
SELECT * FROM authtoken_token;
SELECT * FROM levelupapi_gamer;
SELECT * FROM levelupapi_game;
SELECT * FROM levelupapi_event;
SELECT * FROM levelupapi_eventgamer;

DELETE FROM levelupapi_gametype
WHERE id > 3;

SELECT
e.date,
e.time,
u.first_name || " " || u.last_name as full_name,
ga.title
FROM levelupapi_event e
JOIN levelupapi_eventgamer eg on e.id = eg.event_id
JOIN levelupapi_gamer g on eg.gamer_id = g.id
JOIN auth_user u on u.id = g.user_id
JOIN levelupapi_game ga on e.game_id = ga.id