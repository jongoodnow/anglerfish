# Welcome to Angler Fish
# You will be assimilated

$ ()->

	setInterval loadStack, 1000
	loadStack()
	setupHandlers()

# Data handling
globalData = []

loadStack = () ->
	$.get "../stack", (data) ->
		data = JSON.parse(data)
		for dRow in data

			alreadyExists = false
			for gRow in globalData
				if dRow.id == gRow.id then alreadyExists = true

			if !alreadyExists
				globalData.push dRow
				createRow(dRow)

createRow = (rowData, container = $("article")) ->

	rowDiv = $ "<div card-row data-stack-id=#{rowData.id}></div>"
	if rowData.type == "picture"
		rowDiv.append $ "<img src=#{rowData.src}/>"

	rowDiv.append $ "<h3>#{rowData.name}</h3>"

	if rowData.message
		rowDiv.append $ "<p>#{rowData.message}</p>"

	if rowData.sender
		rowDiv.append $ "<p>-#{rowData.sender}</p>"

	container.append rowDiv

# Gesture control
escapeVelocity = 0.25
minDist = 33

setupHandlers = () ->

	# Touch start
	$("body").delegate "[card-row]", "touchstart", (evt) ->
		target = $(evt.target)
		if target.parent('[card-row]').length > 0 then return true

		target.attr "data-touch-x", evt.originalEvent.touches[0].pageX
		target.attr "data-start-time", new Date().getTime()
		return true

	# Touch move
	$("body").delegate "[card-row]", "touchmove", (evt) ->
		target = $(evt.target)
		if target.parent('[card-row]').length > 0 then return true

		startX = parseInt target.attr "data-touch-x"
		delta = evt.originalEvent.touches[0].pageX - startX
		$(evt.target).css "left", "#{delta}px"

		target.attr "data-last-x", evt.originalEvent.touches[0].pageX
		return true

	# Touch done, continue velocity
	$("body").delegate "[card-row]", "touchend", (evt) ->
		target = $(evt.target)
		if target.parent('[card-row]').length > 0 then return true

		startX = parseInt target.attr "data-touch-x"
		startT = parseInt target.attr "data-start-time"
		lastX = parseInt target.attr "data-last-x"

		deltaX = Math.abs(lastX - startX)
		deltaT = (new Date().getTime()) - startT
		velocity = deltaX / deltaT

		if deltaX > minDist and velocity > escapeVelocity
			width = $("body").width()
			targetLeft = if lastX > startX then width else -width
			remainingDistance = width - deltaX
			time = 0.66 * (1 / (velocity / remainingDistance))
			target.animate {left: "#{targetLeft}px"}, time, () ->

				# On complete
				rowId = target.attr "data-stack-id"
				row = r for r in globalData when r.id == rowId
				sendCard(row, velocity, lastX > startX)
				target.animate {height: "0px"}, 200, () ->
					target.remove()

		else
			target.animate {left: "0px"}, 200

# Accelerometer control
accY = 0
accX = 0
window.ondevicemotion = (event) ->
	accX = event.accelerationIncludingGravity.x
	accY = event.accelerationIncludingGravity.y

# API back to the server
sendCard = (card, velocity, isRight) ->
	postData = {}
	postData['row'] = card
	postData['velocity'] = velocity

	pureAngle = Math.atan2(accX, accY)
	offset = Math.PI / 4
	postData['angle'] = pureAngle + (if isRight then offset else -offset)

	$.post "../push", postData, (data)->
		console.log data
