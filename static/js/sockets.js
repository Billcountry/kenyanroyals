/**
 * Created by ruth on 12/23/17.
 */

var socket = io.connect('https://' + document.domain + ':' + location.port);

    socket.on('connect', function() {
        // Start sending data to the server
        socket.emit('my event', {data: 'I\'m connected!'});
    });

    socket.on('balance_update', function(message) {
        // Update the interface with the new balance
    });