$(function(){
    function init_lines(){
        var lines = {
            bandwidth: [],
            proportion: [],
        };
        
        for(var i = 1; i < 7; i++){
            lines.bandwidth.push({
                label: "192.168.1." + i,
                data: [],
            });
            
            lines.proportion.push({
                label: "192.168.1." + i,
                data: [],
            });
        }
            
        return lines;
    }
    
    function append_to_lines(map, bandwidth_lines, proportion_lines){
        /* Expected map {"ip": bandwidth} */
        
        // Find total bandwidth
        var total_bandwidth = 0;
        for(var key in map){
            total_bandwidth += map[key];
        }

        // Add next point to each line
        var now = new Date().getTime();
        for(var i = 0; i < bandwidth_lines.length; i++){
            var ip = bandwidth_lines[i].label;
            // (time, bandwidth)
            bandwidth_lines[i].data.push([
                now,// - then,
                map[ip]
            ]);
            
            //  (time, bandwidth / total)
            proportion_lines[i].data.push([
                now,//- then,
                map[ip] / total_bandwidth * 100
            ]);
            
            if(bandwidth_lines[i].data.length > max_points){
                bandwidth_lines[i].data.shift();
                proportion_lines[i].data.shift();
            }
        }
    }
    
    function onDataReceived(new_data){
        append_to_lines(
            new_data,
            lines.bandwidth,
            lines.proportion
        );
        
        plots.bandwidth = $.plot($("#bandwidth"), lines.bandwidth, $.extend(common_options, {
            series: {
                //stack: true,
                lines: {
                    show: true,
                    fill: false
                },
                points: {
                    show: true
                }
            },
            yaxis: {
                label: "Bandwidth",
                min: 0,
            },
        }));

        plots.proportion = $.plot($("#proportion"), lines.proportion, $.extend(common_options, {
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
                label: "Percent of Bandwidth",            
                min: 0,
                max: 100,
            },
        }));
    }
    
    function update(){
        $.ajax({
            url: "flot/test" + (count++ % 6) + ".json",
            method: 'GET',
            dataType: 'json',
            success: onDataReceived
        });

        //setTimeout(update, timestep * 1000);
    }
    
    var then = new Date().getTime();
    var count = 0;
    var lines = init_lines();
    var plots = [];
    
    var timestep = 4;
    var max_points = 15;
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
            label: "Time",
            ticks: max_points / 3,
            mode: "time",
        },
    }

    update();
});