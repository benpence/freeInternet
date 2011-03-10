freeInternet.inspect = function(){
    // Constants
    var TEXTS = [
        "Inspect",
        "Graph"
    ];
    var IMAGES = [
        "css/inspect.png",
        "css/graph.png"
    ];
        
    var icon = $("#inspect_icon", $(this));

    charts.inspect = !charts.inspect;

    icon.attr(
        "src",
        IMAGES[Number(charts.inspect)]
    );

    var text = $("#inspect_text", $(this));
    text.text(
        TEXTS[Number(charts.inspect)]
    );
};

$(function(){
    $("#inspect").click(freeInternet.inspect);
});