$(function(){
    function onUpdate(callback)
        $.ajax({
            url: "flot/test" + (count++ % 6) + ".json",
            method: 'GET',
            dataType: 'json',
            success: callback
        });
    }
    
    function draw(graphs_node, graph_name, graph_data){
        var graph_node = $('#' + graph_name, graphs_node);
        
        // Create node if it doesn't exist
        if(!graph_node){
            /* FILL THIS IN */
        }
        
        $.plot(graph_node, graph_data.lines, graph_data.options);
    }
    
    function updateForever(data){
        function nextData(graph_name, ip, proportions, data){
            if(name.indexOf("proportions") != -1){
                return proportions[ip];
            }
            
            return data[graph_name][ip];
        }
        
        function calculateProportions(ipsToValues){
            var proportions = {};
        
            var total = 0;
            
            for(var ip in ipsToValues){
                total += ipsToValues[ip];
            }
            
            for(var ip in ipsToValues){
                proportions[ip] = ipsToValues[ip] / total * 100;
            }
            
            return proportions;
        }
    
        var graphs_node = $('graphs');
        var now = new Date().getTime();
        for(var name in data){
            var proportions = calculateProportions(data[name]);

            // For the values and the value proportions
            for(var graph_name in [name, name + "_proportion"]){
                // Create graph if it doesn't exist
                if(!graphs[graph_name]){
                    graphs[graph_name] = {
                        options: (name == graph_name ? value_options : proportion_option),
                        lines: []
                    };
                }
                
                // For each ip
                for(var ip in data[name]){
                    // Create line if it doesn't exist
                    if(!graphs[graph_name].lines.length < 1){
                        graphs[graph_name].lines.push({
                            label: ip,
                            data: [[
                                now - then,
                                // Value or proportion
                                firstData(graph_name, ip, proportions, data)
                            ]],
                        });
                        
                    // Add to line
                    } else {
                        /*graphs[graph_name].lines*/
                    }
                }
                
                // Draw graph
                draw(graphs_node, graph_name, graphs[graph_name]);
            }
        }
        
        setTimeout(
            function (){
                onUpdate(draw)
            },
            TIMESTEP * 1000
        );
    }        
    
    // Constants
    var TIMESTEP = 2;
    var MAX_POINTS = 20;
    
    // Options
    var common_options = {
        grid: {
            color: "#898989",
            borderWidth: 1,
        },
        legend: {
            container: $("#legend")
        },
        crosshair: {
            mode: "x",
        },
        xaxis: {
            ticks: MAX_POINTS / 4,
            mode: "time",
            show: false,
        },
    }
    var value_options = $.extend(common_options, {
        series: {
            lines: {
                show: true,
                fill: false
            },
            points: {
                show: true
            }
        },
        yaxis: {
            min: 0,
        },
    });
    var proportion_options = $.extend(common_options, {
        series: {
            stack: true,
            lines: {
                show: true,
                fill: true
            },
            points: {
                show: false
            }
        },
        yaxis: {
            min: 0,
            max: 100,
        },
    })
    
    
    // Start time
    var then = new Date().getTime();
    var count = 0;

    // Init lines
    var graphs = {};

    // Start loop
    onUpdate(updateForever);
});