var helpers = {};
helpers.view = function(ctrl) {};
helpers.controller = function() {};

helpers.inputValidation = function() {
    var me = {};
    me.isAlpha = function(inputToValidate) {
        return (inputToValidate.search(/[^\w*^\d*]/) == -1);
    };
    me.isEmail = function(inputToValidate) {
        return (inputToValidate.search(/[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/) !== -1);
    };
    me.replaceSpacesWithUnderscores = function(inputToValidate) {
        if(inputToValidate != undefined) {
            return inputToValidate.replace(/ /g, "_");
        } else {
            return "";
        }
    };
    return me;
};


helpers.cookies = function() {
    var me = {};
    me.getCookie = function(cname) {
        var name = cname + "=";
        var ca = document.cookie.split(';');
        for(var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' '){
                c = c.substring(1);
            }
            if (c.indexOf(name) != -1){
                return c.substring(name.length,c.length);
            }
        }
        return false;
    };
    me.deleteCookie = function(cname) {
        if(me.getCookie(cname)) {
            document.cookie = cname + "= ;expires=Thu, 01-Jan-1970 00:00:01 GMT";
        }
    };
    me.checkSession = function(responseFunction) {
        if(me.getCookie("session")) {
            m.request({
                method: "POST",
                url: "/account",
                data: {"session":JSON.stringify(me.getCookie("session"))}
            }).then(function(response) {
                responseFunction(response);
            })
        } else {
            console.log("No Session");
            return "No Session"
        }
    };
    return me;
};

helpers.sort = function() {
    var me = {};

    me.sortByProperty = function(property) {
        'use strict';
        if(property == "gameplays") {
            return function (a, b) {
                var sortStatus = 0;
                if (parseInt(a[property]) < parseInt(b[property])) {
                    sortStatus = 1;
                } else if (parseInt(a[property]) > parseInt(b[property])) {
                    sortStatus = -1;
                }
                return sortStatus;
            };
        } else {
            return function (a, b) {
                var sortStatus = 0;
                if (a[property] < b[property]) {
                    sortStatus = -1;
                } else if (a[property] > b[property]) {
                    sortStatus = 1;
                }
                return sortStatus;
            };
        }
    };
    return me;
};

helpers.colors = function() {
    var me = {};
    me.goodColor = "#62BF65";
    me.badColor = "#E67373";
    me.greyColor = "#808080";
    return me;
};

helpers.routing = function() {
    var me = {};
    me.reroute = function() {
        m.route("#/page/1");
    };
    return me;
};