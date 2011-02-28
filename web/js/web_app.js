var doInspect;

$(function (){
    doInspect = function(){
        inspect = !inspect;
        
        if(inspect){
            $('.highcharts-legend').hide()
        } else {
            $('.highcharts-legend').show()
        }
        
    };

    var texts = [
        "Inspect",
        "Graph"
    ];
    var images = [
        "img/inspect.png",
        "img/graph.png"
    ];

    $("#inspect").click(function () {
        var icon = $("#inspect_icon", $(this));

        icon.attr(
            "src",
            images[Number(inspect)]
        );
    
        var text = $("#inspect_text", $(this));
        text.text(
            texts[Number(inspect)]
        );
        
        doInspect();
    });
});

function onLegendHover(legend_box){
    
}

function onLegendClick(legend_box){
    
}

