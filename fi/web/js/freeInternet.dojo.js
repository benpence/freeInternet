freeInternet.Dojo = Class.$extend({
    onNodeClick: function(self, message){
        $.log(message);
        
        var item = message.item
        
        // Clicked job name
        if(item.type == "job"){
            
        }
            
        // Clicked instance input -> Get all output for relevant assignments
        function gotData(self, data){
            /*
            FORMAT:
                ass.id : {
                    'ip': ass.client.ip,
                    'date_issued': ass.date_issued,
                    'date_returned': ass.date_returned,
                    'output': ass.output,
                    'verified': ass.verified
                }
            */
            // Format tab content
            var output = "";
            $.each(data, function(ass_id, values){
                output += "<u>Assignment " + ass_id + ":</u><br/>"
                output += "<b>" + values.ip + "</b> client<br />";
                output += "<b>" + values.date_issued + "</b> issued<br />";
                output += "<b>" + values.date_returned + "</b> output returned<br />"
                output += "<b>" + values.verified + "ly</b> performed:<br />";
                output += "<span style='color: "
                
                if(values.verified == "Correct"){
                    output += "#393;'>"
                } else {
                    output += "#933;'>"
                }
                
                output += values.output + "</span><br /><br />";
            });
            
            // Create tab object
            self.tabs[item.id] = new dijit.layout.ContentPane({
                title: item.job + " " + item.instance_id,
                content: output,
                closable: true,
            });
            
            // Add to DOM
            self.tab_container.addChild(self.tabs[item.id]);
        }
        
        // Already open?
        if(!!self.tabs[item.id]){
            self.tab_container.selectChild(self.tabs[item.id]);
            return
        }
        
        // Create new tab for assignments of relevant job-instance
        freeInternet.ajaxCallback(
            self,
            'assignments-' + item.job_id + '-' + item.instance_id + '.json',
            {},
            gotData
        );
    },
    
    createJobs: function(self){
        dojo.require("dojo.data.ItemFileReadStore");
        dojo.require("dijit.Tree");
        dojo.require("dijit.TooltipDialog");

        dojo.addOnLoad(function() {
            var store = new dojo.data.ItemFileReadStore({
                url: "jobs.json"
            });

            var treeModel = new dijit.tree.ForestStoreModel({
                store: store,
                query: {
                    "type": "job"
                },
                childrenAttrs: ["children"],
            });

            /*var dialog = new dijit.TooltipDialog({
                content: "item.description"
            });*/
            
            new dijit.Tree(
                {
                    model: treeModel,
                    showRoot: false,
                    openOnClick: false,
                },
                'jobs_node'
            );
        });
        
        // For click events
        dojo.subscribe("jobs_node", dojo.hitch(this, function(message){
            self.onNodeClick(self, message);
        }));
        
        // For close events
        dojo.subscribe("interface-removeChild", function(child){
            $.each(self.tabs, function(key, tab){
                if(tab == child){
                    delete self.tabs[key];
                    return;
                }
            })
        });
    },
    
    createLayout: function(self, node_id){
        dojo.require("dijit.layout.TabContainer");
        dojo.require("dijit.layout.ContentPane");
        
        dojo.addOnLoad(function() {
            self.tab_container = new dijit.layout.TabContainer({
                style: "height: 100%; width: 100%;"
            },
            node_id);

            var cp1 = new dijit.layout.ContentPane({
                title: "Graphs",
                content: $('#graphs_node')
            });
            self.tab_container.addChild(cp1);

            var cp2 = new dijit.layout.ContentPane({
                title: "Jobs",
                content: $('#jobs_node')
            });
            self.tab_container.addChild(cp2);

            self.tab_container.startup();
        });
    },

    __init__ : function(node_id){
        this.node = $('#' + node_id);
        this.tabs = {}
                
        this.createLayout(this, node_id);
        this.createJobs(this)
        this.graphs_node = $('#graphs_node');
    },
});
    
var ui;
dojo.ready(function(){
    ui = new freeInternet.Dojo('interface');
    
    ui.charts = new freeInternet.Charts(ui.graphs_node);
    freeInternet.ajaxCallback(
        ui.charts,
        'creditbandwidth.json',
        '',
        ui.charts.drawCharts
    );
});