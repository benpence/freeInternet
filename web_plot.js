$(function(){
    function ajaxCallback(callback){
        /*
            ajaxCallback
            callback:function -> undefined
        
            Streamlines ajax calls with data callback function
        */
        
        $.ajax({
            url: "flot/test" + (count++ % 6) + ".json",
            method: 'GET',
            dataType: 'json',
            success: callback
        });
    }
    
    function draw(graphs_node, graph_name, graph_data){
        /*
            graphs_node:div | graph_name:String | graph_data:{String:{}} -> undefined

            Inserts new graph DOM divs in graph_node (if necessary) and plots them
        */
        
        // Create node if it doesn't exist
        if(!graph_data.node){
            graph_data.node = $(
                '<div class="graph" id="' + graph_name + '">' +
                    '<div class="graph_bar">' +
                        '<img src="img/minimize.png" id="graph_minimize" />' +
                        '<img src="img/maximize.png" id="graph_maximize" />' +
                    '</div>' +
                    '<div id="graph_plot" style="width:600px;height:200px;"></div>' +
                '</div>'
            );
            
            graphs_node.append(graph_data.node);
        }
    
        $.plot(
            $('#graph_plot', graph_data.node)
                .width(300)
                .height(300),
            graph_data.lines,
            graph_data.options
        );
    }
    
    function updateForever(data){
        /*
            data:{String:{String:int}} -> undefined

            Updates/creates initial lines with data
            Calls to plot each graph
            Sets a Timeout for itself
        */
        function calculateProportions(ipsToValues){
            /* Take values and turn them into an a-array of proportions to each other */
            var proportions = {};
        
            var total = 0;
            
            // Count total
            for(var ip in ipsToValues){
                total += ipsToValues[ip];
            }
            
            // Create proportions a-array
            for(var ip in ipsToValues){
                proportions[ip] = ipsToValues[ip] / total * 100;
            }
            
            return proportions;
        }
        function nextData(graph_name, ip, proportions, ipsToValues){
            /* Depending on context, return value or proportion value */
            if(graph_name.indexOf("proportions") != -1){
                return proportions[ip];
            }
            
            return ipsToValues[ip];
        }
        
        /* graphs will look like this:
            {
                graph_name : {
                    options: {}
                    lines: []
                    node: DOM div (not plot DOM div)
                }
            }
        */
        var graphs_node = $('graphs');
        var now = new Date().getTime();

        for(var name in data){
            var proportions = calculateProportions(data[name]);

            // For the values and the value proportions
            for(var graph_name in [name, name + "_proportion"]){
                var graph_data = graphs[graph_name];
                
                // Create graph if it doesn't exist
                if(!graph_data){
                    graph_data = graphs[graph_name] = {
                        // Value or proportion graph?
                        options: (
                            name == graph_name ?
                                value_options :
                                proportion_options),
                        lines: []
                    };
                }

                // For each ip
                var i = 0;
                for(var ip in data[name]){
                    var new_point = [
                        now - then,
                        // Value or proportion
                        nextData(graph_name, ip, proportions, data[name]),
                    ];
                    
                    // Create line if it doesn't exist
                    if(!graph_data.lines[i]){
                        graph_data.lines.push({
                            label: ip,
                            data: [new_point]
                        });
                        
                    // Add to line
                    } else {
                        graph_data.lines[i].data.push(new_point);
                    }
                    i++;
                }
                
                // Draw graph
                draw(graphs_node, graph_name, graph_data);
            }
        }
        
        /*setTimeout(
            function (){
                ajaxCallback(updateForever)
            },
            TIMESTEP * 1000
        );*/
    }        
    
    // Constants
    var TIMESTEP = 2;
    var MAX_POINTS = 20;
    
    // Options
    var COMMON_OPTIONS = {
        grid: {
            color: "#898989",
            borderWidth: 1,
        },
        legend: {
            container: $("#legend")
        },
        /*crosshair: {
            mode: "x",
        },*/
        xaxis: {
            ticks: MAX_POINTS / 4,
            mode: "time",
            show: false,
        },
    }
    var value_options = $.extend(COMMON_OPTIONS, {
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
    var proportion_options = $.extend(COMMON_OPTIONS, {
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
    ajaxCallback(updateForever);
});