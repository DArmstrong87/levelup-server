SELECT * FROM levelupapi_gametype;

SELECT * FROM auth_user;
SELECT * FROM authtoken_token;
SELECT * FROM levelupapi_gamer;
SELECT * FROM levelupapi_game;
SELECT * FROM levelupapi_event;
SELECT * FROM levelupapi_eventgamer;

DELETE FROM levelupapi_gametype
WHERE id > 3;