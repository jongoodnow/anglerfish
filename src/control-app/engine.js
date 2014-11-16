(function() {
  var accX, accY, beta, createRow, escapeVelocity, globalData, initialBeta, loadStack, minDist, sendCard, setupHandlers;

  $(function() {
    setInterval(loadStack, 1000);
    loadStack();
    return setupHandlers();
  });

  globalData = [];

  loadStack = function() {
    return $.get("../stack", function(data) {
      var alreadyExists, dRow, gRow, _i, _j, _len, _len1, _results;
      data = JSON.parse(data);
      _results = [];
      for (_i = 0, _len = data.length; _i < _len; _i++) {
        dRow = data[_i];
        alreadyExists = false;
        for (_j = 0, _len1 = globalData.length; _j < _len1; _j++) {
          gRow = globalData[_j];
          if (dRow.id === gRow.id) {
            alreadyExists = true;
          }
        }
        if (!alreadyExists) {
          globalData.push(dRow);
          _results.push(createRow(dRow));
        } else {
          _results.push(void 0);
        }
      }
      return _results;
    });
  };

  createRow = function(rowData, container) {
    var rowDiv;
    if (container == null) {
      container = $("article");
    }
    rowDiv = $("<div card-row data-stack-id=" + rowData.id + "></div>");
    if (rowData.type === "picture") {
      rowDiv.append($("<img src=" + rowData.src + "/>"));
    }
    rowDiv.append($("<h3>" + rowData.name + "</h3>"));
    if (rowData.message) {
      rowDiv.append($("<p>" + rowData.message + "</p>"));
    }
    if (rowData.sender) {
      rowDiv.append($("<p>-" + rowData.sender + "</p>"));
    }
    return container.append(rowDiv);
  };

  escapeVelocity = 0.25;

  minDist = 33;

  setupHandlers = function() {
    $("body").delegate("[card-row]", "touchstart", function(evt) {
      var target;
      target = $(evt.target);
      if (target.parent('[card-row]').length > 0) {
        return true;
      }
      target.attr("data-touch-x", evt.originalEvent.touches[0].pageX);
      target.attr("data-start-time", new Date().getTime());
      return true;
    });
    $("body").delegate("[card-row]", "touchmove", function(evt) {
      var delta, startX, target;
      target = $(evt.target);
      if (target.parent('[card-row]').length > 0) {
        return true;
      }
      startX = parseInt(target.attr("data-touch-x"));
      delta = evt.originalEvent.touches[0].pageX - startX;
      $(evt.target).css("left", "" + delta + "px");
      target.attr("data-last-x", evt.originalEvent.touches[0].pageX);
      return true;
    });
    return $("body").delegate("[card-row]", "touchend", function(evt) {
      var deltaT, deltaX, lastX, remainingDistance, startT, startX, target, targetLeft, time, velocity, width;
      target = $(evt.target);
      if (target.parent('[card-row]').length > 0) {
        return true;
      }
      startX = parseInt(target.attr("data-touch-x"));
      startT = parseInt(target.attr("data-start-time"));
      lastX = parseInt(target.attr("data-last-x"));
      deltaX = Math.abs(lastX - startX);
      deltaT = (new Date().getTime()) - startT;
      velocity = deltaX / deltaT;
      if (deltaX > minDist && velocity > escapeVelocity) {
        width = $("body").width();
        targetLeft = lastX > startX ? width : -width;
        remainingDistance = width - deltaX;
        time = 0.66 * (1 / (velocity / remainingDistance));
        return target.animate({
          left: "" + targetLeft + "px"
        }, time, function() {
          var r, row, rowId, _i, _len;
          rowId = target.attr("data-stack-id");
          for (_i = 0, _len = globalData.length; _i < _len; _i++) {
            r = globalData[_i];
            if (r.id === rowId) {
              row = r;
            }
          }
          sendCard(row, (lastX - startX) / deltaT, lastX > startX);
          return target.animate({
            height: "0px"
          }, 200, function() {
            return target.remove();
          });
        });
      } else {
        return target.animate({
          left: "0px"
        }, 200);
      }
    });
  };

  accY = 0;

  accX = 0;

  window.ondevicemotion = function(event) {
    accX = event.accelerationIncludingGravity.x;
    return accY = event.accelerationIncludingGravity.y;
  };

  initialBeta = void 0;

  beta = 0;

  window.addEventListener('deviceorientation', function(event) {
    if (initialBeta === void 0) {
      initialBeta = event.gamma + 180;
    }
    return beta = event.gamma + 180;
  });

  sendCard = function(card, velocity, isRight) {
    var postData, pureAngle, reverse;
    postData = {};
    postData['row'] = card;
    reverse = Math.abs(initialBeta - beta) < 90 || Math.abs(initialBeta + 360 - beta) < 90;
    postData['velocity'] = reverse ? velocity : -velocity;
    pureAngle = Math.atan2(accX, accY);
    postData['angle'] = -pureAngle;
    return $.post("../push", JSON.stringify(postData), function(data) {
      return console.log(data);
    });
  };

}).call(this);
