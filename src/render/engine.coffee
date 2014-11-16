# App State
cards = {}

# Start
$ ()->
	startUI()

	ws = new WebSocket("ws://127.0.0.1:8888/socket");
	ws.onopen = ()->
	   ws.send("Connecting to Anglerfish Central Command");

	ws.onmessage = (evt) ->
		data = JSON.parse evt.data
		if data.connected 
			$(".time").css("display","block")
		else if data.pointer
			point = data.pointer[0].split(',')
			point[0] = Math.max(Math.min(parseFloat(point[0]), 1), 0)
			point[1] = Math.max(Math.min(parseFloat(point[1]), 1), 0)
			$("#pointerDot").css("left", "#{point[0] * window.innerWidth}px")
			$("#pointerDot").css("top", "#{point[1] * window.innerHeight}px")
		else
			addCard(data.row, data.velocity, data.angle)

# Clock
startUI = () ->
	setInterval updateTime, 500
	setInterval updateBar, 100000
	updateBar()

updateTime = () ->
	h = "" + (new Date().getHours() % 12) || 12
	m = "" + new Date().getMinutes()
	if m.length is 1 then m = "0" + m

	a = if new Date().getHours() > 12 then "PM" else "AM"
	div = $ ".time"
	div.html "#{h}:#{m} #{a}"

# Bar
updateBar = () ->
	$("#bar").css('backgroundPosition', "0px 0px");
	$("#bar").transition({'backgroundPosition': "2000px 0px"}, 100000, "linear");

# Add a module
addCard = (card, velocity, angle) ->
	card.velocity = velocity
	card.angle = angle
	card.content = applyTemplate("content-#{card.type}", card, false)
	card.dom = applyTemplate("card-template", card)

	cards[card.id] = card
	$("body").append card.dom

	setTimeout (()-> centerCard(card)), 1
	setTimeout (()-> transitionInCard(card)), 2

# Center a card around a point
centerCard = (card, x = window.innerWidth/2, y = window.innerHeight/2) ->
	[cw, ch] = [card.dom.width(), card.dom.height()]
	card.dom.css "left", "#{x - cw/2}px"
	card.dom.css "top", "#{y - ch/2}px"

# Animate a card
velocityScale = 200
transitionInCard = (card) ->
	dx = velocityScale * card.velocity * Math.cos card.angle
	dy = velocityScale * card.velocity * Math.sin card.angle

	nLeft = dx + parseInt card.dom.css "left"
	nTop = dy + parseInt card.dom.css "top"

	card.dom.transition {
		"opacity": 1.0,
		"left": "#{nLeft}px"
		"top": "#{nTop}px"
	}, 1200, "easeOutExpo"

# Keaton's magical HTML templating
applyTemplate = (templateName, data, returnElement = true) ->
    html = $("#"+templateName).html()                                 # Get a copy the template html
    html = html.replace(/\$([a-zA-Z1-9\-\_]*)(\?(.*?)\:(.*?)\;)?/g,   # Regex to match variables & ternaries
        (match,vn,tern,pass,fail) ->                                  # Variable value substitution function
            if tern then return (if data[vn] then pass else fail)     # Sub in ternary operation result
            return data[vn]                                           # Sub in the variable value
    ); return if returnElement then $(html) else html       		  # Returns a jQuery object with the html
