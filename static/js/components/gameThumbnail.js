var gameThumbnail = {};

gameThumbnail.view = function(ctrl, args) {
    if(args.gameInfo != undefined) {
        if(args.gameInfo.title.length > 15) {
            args.gameInfo.title = args.gameInfo.title.substring(0, 15) + "...";
        }
        return m(".col-sm-3",[
            m(".well.well-sm", {style: "border-radius: 0; border-style: solid; border-width: 1px; border-color: gray; background-color: #eee; width: " + (document.getElementById("getWidth").offsetWidth / 4)}, [
                m("center", [
                    m("p", args.gameInfo.title),
                    m("a", {href: "#/game/" + inputValidation.replaceSpacesWithUnderscores(args.gameInfo.title)}, [
                        m("img.img-rounded.img-responsive", {src: args.gameInfo.thumbnail, alt: args.gameInfo.title})
                    ]),
                    m("br")
                ])
            ])
        ])
    } else {
        //fallback for first render
        return m("#placeholder");
    }
};

gameThumbnail.controller = function(args) {
    var me = {};
    return me;
};

//global array of games objects
//game object attributes:
//category
//description
//developer_name
//featured_image
//flash_file
//gameplays
//height
//id
//instructions
//launch_date
//rating
//screenshot
//thumbnail
//title
//url
//width