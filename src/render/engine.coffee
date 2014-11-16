$ ()->
	ws = new WebSocket("ws://127.0.0.1:8888/socket");

	ws.onopen = ()->
	   ws.send("Hello, world");

	ws.onmessage = (evt) ->
	   alert(evt.data);