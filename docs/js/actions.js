/**
 * Created by ruth on 12/23/17.
 */

$('.button-collapse').sideNav({
        menuWidth: 300, // Default is 300
        edge: 'left', // Choose the horizontal origin
        closeOnClick: true, // Closes side-nav on <a> clicks, useful for Angular/Meteor
        draggable: true, // Choose whether you can drag to open on touch screens,
        onOpen: function (el) { /* Do Stuff */
        }, // A function to be called when sideNav is opened
        onClose: function (el) { /* Do Stuff */
        }, // A function to be called when sideNav is closed
    }
);

var just_a_click = true;

var on_click = function (element, settings) {
    function setDefaultVal(value, defaultValue) {
        return (value === undefined) ? defaultValue : value;
    }

    settings = {
        click: setDefaultVal(settings.click, function (evt) {
            console.log(evt)
        }),
        dblclick: setDefaultVal(settings.dblclick, function (evt) {
            console.log(evt)
        })
    };

    element.addEventListener('dblclick', function (evt) {
        just_a_click = false;
        setTimeout("just_a_click = true;", 500);
        settings.dblclick(evt);
    });

    element.addEventListener('click', function (evt) {
        setTimeout(function () {
            if (just_a_click) {
                settings.click(evt)
            }
        }, 400);
    });
};

var success_disp = document.querySelector('#disp_success');
on_click(success_disp, {
    click: function () {
        toast("Double click to view successful members.");
    },
    dblclick: function () {
        toast("Loading success cases");
    }
});

var fail_disp = document.querySelector('#disp_failed');
on_click(fail_disp, {
    click: function () {
        toast("Double click to view members who fell back to homelessness");
    },
    dblclick: function () {
        toast("Loading failed cases");
    }
});

var pending_disp = document.querySelector('#disp_pending');
on_click(pending_disp, {
    click: function () {
        toast("Double click to display members who we hope to help");
    },
    dblclick: function () {
        toast("Loading pending cases");
    }
});

var toast = function (message) {
    Materialize.toast(message, 6000)
};

var ajax = function (options) {
    function setDefaultVal(value, defaultValue) {
        return (value === undefined) ? defaultValue : value;
    }

    var settings = {
        url: setDefaultVal(options.url, ""),
        type: setDefaultVal(options.type, "GET"),
        headers: setDefaultVal(options.headers, {}),
        data: setDefaultVal(options.data, {}),
        dataType: setDefaultVal(options.dataType, "text"),
        success: setDefaultVal(options.success, function (response) {
            console.log(response);
        }),
        error: setDefaultVal(options.error, function (error) {
            console.log(error)
        })
    };
    // Can implement multiple methods of Ajax
    if (Window.fetch) {
        var data = new FormData();
        if (settings.data !== undefined) {
            Object.keys(settings.data).forEach(function (key) {
                data.append(key, settings.data[key]);
            });
        }

        function checkStatus(response) {
            if (response.status >= 200 && response.status < 300) {
                return response
            } else {
                var error = new Error(response.statusText);
                error.response = response;
                throw error;
            }
        }

        function parseData(response) {
            var type = response.headers.get('Content-Type');
            if (settings.dataType === "json" || type.index("json") >= 0) {
                return response.json();
            } else {
                return response.text()
            }
        }

        fetch(settings.url, {
            method: settings.type,
            body: data
        }).then(checkStatus).then(parseData).then(settings.success).catch(settings.error)
    } else {
        $.ajax(settings);
    }
};
