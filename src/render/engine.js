(function() {
  var addCard, applyTemplate, cards, centerCard, startUI, transitionInCard, updateBar, updateTime, velocityScale;

  cards = {};

  $(function() {
    var ws;
    startUI();
    ws = new WebSocket("ws://127.0.0.1:8888/socket");
    ws.onopen = function() {
      return ws.send("Connecting to Anglerfish Central Command");
    };
    return ws.onmessage = function(evt) {
      var data, point;
      data = JSON.parse(evt.data);
      if (data.connected) {
        return $(".time").css("display", "block");
      } else if (data.pointer) {
        point = data.pointer[0].split(',');
        $("#pointerDot").css("right", "" + (parseFloat(point[0]) * window.innerWidth) + "px");
        return $("#pointerDot").css("top", "" + (parseFloat(point[1]) * window.innerHeight) + "px");
      } else {
        return addCard(data.row, data.velocity, data.angle);
      }
    };
  });

  startUI = function() {
    setInterval(updateTime, 500);
    setInterval(updateBar, 100000);
    return updateBar();
  };

  updateTime = function() {
    var a, div, h, m;
    h = "" + (new Date().getHours() % 12) || 12;
    m = "" + new Date().getMinutes();
    if (m.length === 1) {
      m = "0" + m;
    }
    a = new Date().getHours() > 12 ? "PM" : "AM";
    div = $(".time");
    return div.html("" + h + ":" + m + " " + a);
  };

  updateBar = function() {
    $("#bar").css('backgroundPosition', "0px 0px");
    return $("#bar").transition({
      'backgroundPosition': "2000px 0px"
    }, 100000, "linear");
  };

  addCard = function(card, velocity, angle) {
    card.velocity = velocity;
    card.angle = angle;
    card.content = applyTemplate("content-" + card.type, card, false);
    card.dom = applyTemplate("card-template", card);
    cards[card.id] = card;
    $("body").append(card.dom);
    setTimeout((function() {
      return centerCard(card);
    }), 1);
    return setTimeout((function() {
      return transitionInCard(card);
    }), 2);
  };

  centerCard = function(card, x, y) {
    var ch, cw, _ref;
    if (x == null) {
      x = window.innerWidth / 2;
    }
    if (y == null) {
      y = window.innerHeight / 2;
    }
    _ref = [card.dom.width(), card.dom.height()], cw = _ref[0], ch = _ref[1];
    card.dom.css("left", "" + (x - cw / 2) + "px");
    return card.dom.css("top", "" + (y - ch / 2) + "px");
  };

  velocityScale = 200;

  transitionInCard = function(card) {
    var dx, dy, nLeft, nTop;
    dx = velocityScale * card.velocity * Math.cos(card.angle);
    dy = velocityScale * card.velocity * Math.sin(card.angle);
    nLeft = dx + parseInt(card.dom.css("left"));
    nTop = dy + parseInt(card.dom.css("top"));
    return card.dom.transition({
      "opacity": 1.0,
      "left": "" + nLeft + "px",
      "top": "" + nTop + "px"
    }, 1200, "easeOutExpo");
  };

  applyTemplate = function(templateName, data, returnElement) {
    var html;
    if (returnElement == null) {
      returnElement = true;
    }
    html = $("#" + templateName).html();
    html = html.replace(/\$([a-zA-Z1-9\-\_]*)(\?(.*?)\:(.*?)\;)?/g, function(match, vn, tern, pass, fail) {
      if (tern) {
        return (data[vn] ? pass : fail);
      }
      return data[vn];
    });
    if (returnElement) {
      return $(html);
    } else {
      return html;
    }
  };

}).call(this);
