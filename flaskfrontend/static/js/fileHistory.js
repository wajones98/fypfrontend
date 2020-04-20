

function openFileHistory(fileId, projectId, modal, sessionId){
    var elem = document.getElementById(modal);
    var instance = M.Modal.getInstance(elem);
    instance.close();

    elem = document.getElementById('FileHistoryViewRow');
    elem.classList.remove("hide");

    elem = document.getElementById('ProjectViewerRow');
    elem.classList.add("hide");

    const Url = "http://127.0.0.1:8080/project/file/history";
 
    json_body = {
            "FileId":fileId,
            "ProjectId":projectId
        }
    const request={
        headers:{
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            "SessionId": sessionId
        },
        body:JSON.stringify(json_body),
        method:"POST"
    };
   
    fetch(Url, request)
    .then(data=>{return data.json()})
    .then(res=>{
        init(res);
    })
    .fetch(error=>console.log(error))    
}

function init(res){

    var $ = go.GraphObject.make;

    var myDiagram =
    $(go.Diagram, "myDiagramDiv",
    {
        "undoManager.isEnabled": true,
        layout: $(go.TreeLayout,
        { angle: 90, layerSpacing: 35 })
    });
    
    myDiagram.nodeTemplate =
        $(go.Node, "Horizontal",
        { background: "#d81b60" },

        $(go.TextBlock, "Default Text",
            { margin: 12, stroke: "white", font: "bold 16px sans-serif" },
            new go.Binding("text", "name")),
            new go.Binding("text, parent")
        );
    

    myDiagram.linkTemplate =
        $(go.Link,
        { routing: go.Link.Orthogonal, corner: 5 },
        $(go.Shape,
            { strokeWidth: 3, stroke: "#555" }));
    
    
        
            var model = $(go.TreeModel);
            for (i in res["History"]){
                var entry = res["History"][i];
                console.log(entry);
                var item = {}
                if (i === 0){
                    model.addNodeData({ key: entry["Filepath"], name: entry["Change"]});
                } else {
                    model.addNodeData({ key: entry["Filepath"], parent: entry["Previous"], name: entry["Change"]});
                }       
                
            }

    myDiagram.model = model;
}
