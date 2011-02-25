$(function(){
    function updateLegend() {
        updateLegendTimeout = null;

        
        var pos = latestPosition;
        var axes = plot.getAxes();

        // Outside of graph
        if(pos.x < axes.xaxis.min || pos.x > axes.xaxis.max || pos.y < axes.yaxis.min || pos.y > axes.yaxis.max)
            return;

        var i, j, dataset = plot.getData();
        for (i = 0; i < dataset.length; ++i){
            var series = dataset[i];

            // find the nearest points, x-wise
            for (j = 0; j < series.data.length; ++j)
                if (series.data[j][0] > pos.x)
                    break;

            // now interpolate
            var y, p1 = series.data[j - 1], p2 = series.data[j];
            if (p1 == null)
                y = p2[1];
            else if (p2 == null)
                y = p1[1];
            else
                y = p1[1] + (p2[1] - p1[1]) * (pos.x - p1[0]) / (p2[0] - p1[0]);

            legends.eq(i).text(series.label.replace(/=.*/, "= " + y.toFixed(2)));
        }
    }

    var legends = $("#legend");
    legends.each(function () {
        // fix the widths so they don't jump around
        $(this).css('width', 98);
    });

    var updateLegendTimeout = null;
    var latestPosition = null;

    $("#proportion").bind("plothover", function (event, pos, item) {
        latestPosition = pos;
        if(!updateLegendTimeout)
            updateLegendTimeout = setTimeout(updateLegend, 50);
    });
    
    $("#bandwidth").bind("plothover", function (event, pos, item) {
        latestPosition = pos;
        if(!updateLegendTimeout)
            updateLegendTimeout = setTimeout(updateLegend, 50);
    });

    /*function getMultiple(ob){
        var selected = [];
        while(ob.selectedIndex != -1){
            if(ob.selectedIndex != 0){
                selected.push(ob.options[ob.selectedIndex].value);
            }
        }
    }*/
});