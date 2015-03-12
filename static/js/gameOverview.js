var gameOverview = {};

gameOverview.view = function(ctrl) {
    return m("#homePageGridContainer.container", [
        m("select.form-control", {style: "width: 15em;"}, [
            m("option", "Alphabetical"),
            m("option", "Most Played"),
            m("option", "Newest"),
            m("option", "Featured")
        ]),
        m(".container", [
            m(".row", {style: "margin-top: 10px;"}, _.times(4, gameThumbnail.view)),
            m(".row", {style: "margin-top: 10px;"}, _.times(4, gameThumbnail.view)),
            m(".row", {style: "margin-top: 10px;"}, _.times(4, gameThumbnail.view)),
            m("center", [
                m(".row", [
                    m("nav", [
                        m("ul.pagination", [
                            m("li", [
                                m("a", {href: "#", "aria-label": "Previous"}, [
                                    m("span", {"aria-hidden": "true"}, "«")
                                ])
                            ]),
                            m("li", [m("a", {href: "#", config: m.route}, "1")]),
                            m("li", [m("a", {href: "#", config: m.route}, "2")]),
                            m("li", [m("a", {href: "#", config: m.route}, "3")]),
                            m("li", [m("a", {href: "#", config: m.route}, "4")]),
                            m("li", [m("a", {href: "#", config: m.route}, "5")]),
                            m("li", [
                                m("a", {href: "#", "aria-label": "Next"}, [
                                    m("span", {"aria-hidden": "true"}, "»")
                                ])
                            ])
                        ])
                    ])
                ])
            ])
        ])
    ]);
};

gameOverview.controller = function() {
    var me = {};
    return me;
};
