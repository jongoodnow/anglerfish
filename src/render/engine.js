(function() {
  $(function() {
    var ws;
    ws = new WebSocket("ws://127.0.0.1:8888/socket");
    ws.onopen = function() {
      return ws.send("Hello, world");
    };
    return ws.onmessage = function(evt) {
      return alert(evt.data);
    };
  });

}).call(this);
