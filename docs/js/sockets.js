/**
 * Created by ruth on 12/23/17.
 */

var socket = io('/realtime');

socket.on('connect', function() {
    socket.emit('json',{
        'action': 'connection',
        'status': true,
        data: null
    })
});

socket.on('message', function(message) {
    console.log(message);
});

socket.on('json', function (json) {
    console.log("Json both ways")
    console.log(json);
})

socket.on('balance_update', function(message) {
    // Update the interface with the new balance
});