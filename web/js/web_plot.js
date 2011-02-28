var charts;
$(function(){
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
        
        for(var name in data){
            var shift = charts[name].series[0].data.length == MAX_POINTS;
            // For the values and the value proportions
            $.each([name, name + "_proportion"], function(i, chart_name){
                var chart = charts[chart_name];
                
                // For each ip
                var i = 0;
                for(var ip in data[name]){
                    // Add point
                    chart.series[i].addPoint(
                        [now, data[name][ip]],
                        false, // redraw?
                        shift  // shift points?
                    );
                    i++;
                }
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
        function defaultOptions(name){
            var proportion = name.indexOf("proportion") == -1;
            
            var options = {
                title: {
                    text: name + " over Time"
                },
                chart: {
                    renderTo: name + '_chart',
                    animation: {
                        duration: TIMESTEP * 1000
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
            
            if(!proportion){
                return $.extend(true, options, {
                    chart: {
                        defaultSeriesType: 'areaspline'
                    },
                    plotOptions: {
                        areaspline: {
                            stacking: 'percent',
                            marker: {
                                enabled: false,
                                states: {
                                    hover: {
                                       enabled: true,
                                       symbol: 'circle',
                                       radius: 2,
                                       lineWidth: 1
                                    }
                                }
                            },
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
                        marker: {
                            enabled: false,
                            states: {
                                hover: {
                                   enabled: true,
                                   symbol: 'circle',
                                   radius: 2,
                                   lineWidth: 1
                                }
                            }
                        }
                    }
                }
            });
        }
        
        
        
        for(var name in data){
            $.each([name, name + "_proportion"], function(i, chart_name){
                $.log(chart_name);
                // Create container node
                var chart_node = $(
                    '<div class="graph" id="' + chart_name + '">' +
                        '<div class="graph_bar">' +
                            '<img src="img/minimize.png" id="graph_minimize" />' +
                            '<img src="img/maximize.png" id="graph_maximize" />' +
                        '</div>' +
                        '<div id="' + chart_name + '_chart" style="width: 600px; height: 200px;"></div>' +
                    '</div>'
                );
        
                charts_node.append(chart_node);
                
                // Create chart
                var options = defaultOptions(chart_name);

                for(var ip in data[name]){
                    options.series.push({
                        name: ip,
                        data: []
                    })
                }
                
                charts[chart_name] = new Highcharts.Chart(options);
            });
        }
        
        
        updateForever();
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
    
    // Constants
    var TIMESTEP = 2;
    var MAX_POINTS = 10;
    
    // Start time
    var charts_node;
    var count = 0;

    charts = {};
    charts_node = $('#charts');

    // Start loop
    ajaxCallback(drawCharts);
});