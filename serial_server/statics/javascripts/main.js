var PV = PV || {};

PV.Socket = {
	base: null,
	monitorAddress: null,
	socket: null,
	$outDiv: $('#monitor-data-items'),
	$inBox: $('#serial-data-input'),
	$sendButton: $('#send-data'),
	$clearButton: $('#clear-monitor'),

	init : function() {
		PV.Socket.base = window.location.host;
		PV.Socket.monitorAddress = 'ws://' + PV.Socket.base + '/serial/data-monitor';
		PV.Socket.socket = new WebSocket(PV.Socket.monitorAddress);
		PV.Socket.attachButtonEvents();
		PV.Socket.attachSocketEvents();
	},

	attachButtonEvents : function() {
		PV.Socket.$sendButton.on('click', function() {
			var data = PV.Socket.$inBox.val();
			console.log(data);
			PV.Socket.sendMessage(data);
		});

		PV.Socket.$clearButton.on('click', function() {
			PV.Socket.$outDiv.empty();
		});
	},
	
	attachSocketEvents : function() {
		PV.Socket.socket.onopen = function() {
			console.log('Connected!');
		};
		
		PV.Socket.socket.onmessage = function(msg) {
			console.log('Received: ' + msg.data);
			PV.Socket.$outDiv.append('<li class="data-received">' + msg.data + '</li>');
		};
		
		PV.Socket.socket.onclose = function() {
			console.log('Disconnected');
		};
	},
	
	sendMessage : function(msg) {
		console.log('Sending: ' + msg);
		PV.Socket.socket.send(msg);
		
		PV.Socket.$outDiv.append('<li class="data-sent">' + msg + '</li>');
	}
};

PV.AutoScroll = {
	$inBox: $('#serial-data-input'),
	$sendButton: $('#send-data'),
	$divToScroll: $('#data-monitor'),
	
	init : function() {
		PV.AutoScroll.attachEvents();
	},
	
	attachEvents : function() {
		this.$sendButton.on('click', function(evt) {
			PV.AutoScroll.$divToScroll[0].scrollTop = PV.AutoScroll.$divToScroll[0].scrollHeight;
			PV.AutoScroll.$divToScroll.val('');
		}).focus();
		
		this.$inBox.on('keyup', function(evt) {
			if (evt.keyCode == 13) {
				var data = PV.AutoScroll.$inBox.val();
				PV.Socket.sendMessage(data);
				PV.AutoScroll.$divToScroll[0].scrollTop = PV.AutoScroll.$divToScroll[0].scrollHeight;
				PV.AutoScroll.$divToScroll.val('');
			}
		}).focus();
	}
};

$(document).on('ready', function() {
	PV.Socket.init();
	PV.AutoScroll.init();
});