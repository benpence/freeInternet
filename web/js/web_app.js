$(function() {
    function inspect(){
    }
    
    var texts = [
        "Inspect",
        "Graph"
    ];
    var images = [
        "img/inspect.png",
        "img/graph.png"
    ];
    
    // Change image
    $("#inspect").mouseup(function() {
        // Change text
        var icon = $("#inspect_icon");
        
        if(icon.attr("src").indexOf("inspect") != -1){
            inspect();
        }
        
        icon.attr(
            "src",
            images[
                (images.indexOf(
                    icon.attr("src")
                ) + 1) % 2
            ]
        );
        
        var text = $("#inspect_text");
        text.html(
            texts[
                (texts.indexOf(
                    text.text()
                ) + 1) % 2
            ]
        );
    });
});

function onLegendHover(legend_box){
    
}

function onLegendClick(legend_box){
    legend_box.setAttribute()
}

