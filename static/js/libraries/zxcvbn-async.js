(function () {
    var a;
    a = function () {
        var a, b;
        b = document.createElement("script");
        b.src = "/static/js/libraries/zxcvbn.js";
        b.type = "text/javascript";
        b.async = !0;
        a = document.getElementsByTagName("script")[0];
        return a.parentNode.insertBefore(b, a)
    };
    null != window.attachEvent ? window.attachEvent("onload", a) : window.addEventListener("load", a, !1)
}).call(this);
