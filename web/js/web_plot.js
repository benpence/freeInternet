var charts;
var inspect = false;

$(function(){
    // Constants
    var TIMESTEP = 1;
    var MAX_POINTS = 10;
    var CHARTS_NODE = $('#charts');
    
    var CHARTS_TO_GRAPH = [
        {
            name: "Credit",
            data_name: "credit",
            proportion: false
        },
        {
            name: "Bandwidth Proportions",
            data_name: "bandwidth",
            proportion: true
        }
    ];
        
    function updateForever(data){
        /*
            data:{String:{String:int}} -> undefined

            Updates/creates initial lines with data
            Calls to plot each graph
            Sets a Timeout for itself
        */
        
        /* charts will look like this:
            {
                chart_name : {
                    options: {}
                    chart: Highcharts.Chart
                }
            }
        */
        
        var now = new Date().getTime();
        if(!inspect){
        $.each(CHARTS_TO_GRAPH, function(i, chart_to_graph){
            var chart_name = chart_to_graph.name;
            var chart = charts[chart_name];
        
            var shift = charts[chart_name].series[0].data.length == MAX_POINTS;
                        
            
            // For each ip
            var j = 0;
            $.each(data[chart_to_graph.data_name], function(ip, value){
                // Add point
                chart.series[j].addPoint(
                    [now, value],
                    false, // redraw?
                    shift  // shift points?
                );
                j++;
            });
            
            chart.redraw();
            
        });
        }
        
        setTimeout(
            function (){
                ajaxCallback(updateForever)
            },
            TIMESTEP * 1000
        );
    }
    
    function drawCharts(data){
        /*
            chart_name:String | chart:{String:{}} -> undefined

            Inserts new graph DOM divs in graph_node (if necessary) and plots them
        */
        function defaultOptions(name, id, proportion){
            var options = {
                title: {
                    text: name + " over Time"
                },
                chart: {
                    renderTo: id + '_chart',
                    animation: {
                        duration: TIMESTEP * 1000,
                        easing: 'linear'
                        
                    },
                },
                xAxis: {
                    /*title: {
                        text: 'Time'
                    },*/
                    type: 'datetime'
                },
                yAxis: {
                    
                },
                legend: {
                    enabled: false,
                    //layout: 'vertical'
                },
                series: []
            }
            
            var marker = {
                enabled: false,
                states: {
                    hover: {
                       enabled: true,
                       symbol: 'circle',
                       radius: 2,
                       lineWidth: 1
                    }
                }
            };
            
            if(proportion){
                return $.extend(true, options, {
                    chart: {
                        defaultSeriesType: 'areaspline'
                    },
                    plotOptions: {
                        areaspline: {
                            stacking: 'normal',
                            marker: marker
                        },
                    }
                });
            } 
            
            return $.extend(true, options, {
                chart: {
                    defaultSeriesType: 'spline'
                },
                plotOptions: {
                    spline: {
                        marker: marker
                    }
                }
            });
        }
        
        $.each(CHARTS_TO_GRAPH, function(i, chart_to_graph){
            var chart_name = chart_to_graph.name;
          
            // Create container node
            var id = chart_name.replace(" ", "_");
            var chart_node = $(
                '<div class="graph" id="' + id + '">' +
                    '<div class="graph_bar">' +
                        '<img src="img/minimize.png" id="graph_minimize" />' +
                        '<img src="img/maximize.png" id="graph_maximize" />' +
                    '</div>' +
                    '<div id="' + id + '_chart" style="width: 600px; height: 200px;"></div>' +
                '</div>'
            );
            CHARTS_NODE.append(chart_node);
            
            // Create chart
            var options = defaultOptions(chart_name, id, chart_to_graph.proportion);

            for(var ip in data[chart_to_graph.data_name]){
                options.series.push({
                    name: ip,
                    data: []
                });
            }
            charts[chart_name] = new Highcharts.Chart(options);
        })
                
        updateForever(data);
    }
    
    function ajaxCallback(callback){
        /*
            ajaxCallback
            callback:function -> undefined
        
            Streamlines ajax calls with data callback function
        */
        $.ajax({
            url: "test" + (count++ % 6) + ".json",
            method: 'GET',
            dataType: 'json',
            success: callback
        });
    }       
    
    var count = 0;
    charts = {};

    // Start loop
    ajaxCallback(drawCharts);
});