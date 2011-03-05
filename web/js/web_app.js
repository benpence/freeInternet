var doInspect;

$(function (){
    doInspect = function(){
        charts.inspect = !charts.inspect;
        
        /*if(inspect){
            $('.highcharts-legend').show()
        } else {
            $('.highcharts-legend').hide()
        }*/
        
        /*$.each(charts, function(key, chart){
            chart.setSize(400, 200);
        });*/
        
        $('.highcarts-grid')
            .width(400)
            .height(400);
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

        doInspect();
        
        icon.attr(
            "src",
            images[Number(charts.inspect)]
        );
    
        var text = $("#inspect_text", $(this));
        text.text(
            texts[Number(charts.inspect)]
        );
    });
});

function onLegendHover(legend_box){
    
}

function onLegendClick(legend_box){
    
}

