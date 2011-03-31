var freeInternet = new Object();

freeInternet.ajaxCallback = function(caller, url, send_data, callback){
    /*
        ajaxCallback
        
        Streamlines ajax calls with data callback function
    */
    $.ajax({
        url: url,
        //url: 'test/test' + (this.count++ % 6) + '.json',
        type: 'GET',
        dataType: 'json',
        data: send_data,
        success: function (data){ callback(caller, data) }
    });
};