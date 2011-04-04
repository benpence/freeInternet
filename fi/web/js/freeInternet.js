var freeInternet = new Object();

freeInternet.ajaxCallback = function(caller, url, callback){
    /*
        ajaxCallback
        
        Streamlines ajax calls with data callback function
    */
    $.ajax({
        url: url,
        //url: 'test/test' + (this.count++ % 6) + '.json',
        type: 'GET',
        dataType: 'json',
        success: function (data){ callback(caller, data) },
    });
};

freeInternet.dojo = {};