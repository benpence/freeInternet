freeInternet.dojo.Static = Class.$extend({
    createJobs: function(self){
        dojo.require("dojo.data.ItemFileReadStore");
        dojo.require("dijit.Tree");

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
            freeInternet.dojo.event.onNodeClick(message.item);
        }));
    },
    
    createLayout: function(self, node_id){
        dojo.require("dijit.layout.TabContainer");
        dojo.require("dijit.layout.ContentPane");
        
        dojo.addOnLoad(function() {
            self.tab_container = new dijit.layout.TabContainer({
                style: "height: 100%; width: 100%;",
                tabPosition: "left-h",
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
    ui = new freeInternet.dojo.Static('interface');
    
    ui.charts = new freeInternet.Charts(ui.graphs_node);
    freeInternet.ajaxCallback(
        ui.charts,
        'creditbandwidth.json',
        ui.charts.drawCharts
    );
});