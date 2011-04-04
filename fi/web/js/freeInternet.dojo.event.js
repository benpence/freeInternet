freeInternet.dojo.event = {
    addTab: function(item, content, title){
        // Already open?
        if(!!ui.tabs[item.id]){
            ui.tabs[item.id].setContent(content);

        } else {
            // Create tab object
            ui.tabs[item.id] = new dijit.layout.ContentPane({
                content: content,
                title: title,
                closable: true,
            });

            // Add to DOM
            ui.tab_container.addChild(ui.tabs[item.id]);
        }

        ui.tab_container.selectChild(ui.tabs[item.id]);
    },
    
    assignmentTab: function(item, grid, title, evt){
        var assignment_id = grid._getItemAttr(evt.rowIndex, 'id');
        
        freeInternet.ajaxCallback(
            this,
            'output-' + item.job_id + '-' + item.instance_id + '-' + assignment_id + '.json',
            function(self, data){
                self.addTab(
                    {id: item.id + ' ' + assignment_id},
                    data.output,
                    title + ' ' + assignment_id
                );
            }
        );
    },

    table_columns: [
        {
            field: 'id',
            name: 'ID',
            width: '40px'
        },
        {
            field: 'ip',
            name: 'Client IP',
            width: 'auto'
        },
        {
            field: 'time_issued',
            name: 'Time Issued',
            width: '200px'
        },
        {
            field: 'time_returned',
            name: 'Time Returned',
            width: '200px'
        },
        {
            field: 'verified',
            name: 'Verified',
            width: 'auto',
            formatter: function(value){
                var color = "";
                if(value == "Correct"){
                    color = "393";
                } else {
                    color = "933"
                }
                        
                return "<span style='color: #" + color + "'>" + value + "</span>";
            }
        }
    ],

    instanceTab: function(item){
        /*
        FORMAT:
            {
                'id' : ass.id,
                'ip': ass.client.ip,
                'time_issued': ass.time_issued,
                'time_returned': ass.time_returned,
                'output': ass.output,
                'verified': ass.verified
            }
        */
        dojo.require("dojox.grid.DataGrid");
        dojo.require("dojo.data.ItemFileWriteStore");
        
        var self = this;
        var title = item.job + " " + item.instance_id;
        dojo.addOnLoad(function(){
            var table = new dojo.data.ItemFileWriteStore({
                url: 'assignments-' + item.job_id + '-' + item.instance_id + '.json',
            });

            // Get number of rows from table
            table.fetch({
                query: {},
                onBegin: function(size, request) {
                    // If no finished assignments, break
                    if(!size){
                        return;
                    }
                    
                    // create a new grid
                    var grid = new dojox.grid.DataGrid({
                        query: {
                            id: '*'
                        },
                        store: table,
                        clientSort: true,
                        //rowSelector: '20px',
                        structure: self.table_columns,
                        onRowDblClick: function(evt){
                            self.assignmentTab(item, grid, title, evt);
                        },
                        selectionMode: 'none',
                    });
                    
                    // Add to tab container
                    self.addTab(item, grid.domNode, title);
                    
                    // Render
                    grid.startup();
                },
                start: 0,
                count: 0
            });
        });
    },    

    jobTab: function(item){
        var output = "";
    
        output += "<b>" + item.name + "</b><br />";
        output += "<u>Description</u><br />" + item.description + "<br /><br />";
        output += "<u>Input</u><br />" + item.input + "<br /><br />";
        output += "<u>Output</u><br />" + item.output + "<br /><br />";
    
        this.addTab(item, output, item.name);
    },

    onNodeClick: function(item){
        // Job
        if(item.type == "job"){
            this.jobTab(item);
            
        // Instance
        } else {
            this.instanceTab(item);
        }
    },
};