
//document.getElementById("PageCaption").innerText = qs["PageCaption"];
//DecisionModel = '<% =Session["CurrentDecisionModel"] %>';
//var ListOfUpdates = { "DM": DecisionModel, "Updates": [] };
//---------------------------------------------------- initialization
$(window).on('load', function () {
    $("#cover").fadeOut(200);
});
function newW() {
    $(window).load();
}
setTimeout(newW, 1000);




//----------------------------------------------------Stack
class Stack {

    constructor() {
        this.items = [];
    }

    push(element) {
        this.items.push(element);
    }

    pop() {
        if (this.items.length === 0)
            return "Underflow";
        return this.items.pop();
    }

    peek() {
        return this.items[this.items.length - 1];
    }

    isEmpty() {
        return this.items.length === 0;
    }

    printStack() {
        var str = "";
        for (var i = 0; i < this.items.length; i++)
            str += this.items[i] + " ";
        return str;
    }

    restStack() {
        for (var i = 0; i < this.items.length; i++)
            this.pop();
    }
}
//---------------------------------------------------- Query Strings
var qs = (function (a) {
    if (a === "") return {};
    var b = {};
    for (var i = 0; i < a.length; ++i) {
        var p = a[i].split('=', 2);
        if (p.length === 1)
            b[p[0]] = "";
        else
            b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
    }
    return b;
})(window.location.search.substr(1).split('&'));
var CurrentStep = 0;
var ReqChanged = false;
var PrevPage = "MainPage";
var stackOfBackButton = new Stack();
stackOfBackButton.push("MainPage");
//----------------------------------------------------
function reset(item) {

    ReloadScriptFile('XML_DB/Profiles/' + UID + '/JS/FeatureRequirements.js');
    ReloadScriptFile('XML_DB/Profiles/' + UID + '/JS/CherryPickIncSolutions.js');

    document.getElementById("BtnNext").style.display = "none";
    document.getElementById("btnResetSelection").style.display = "block";
    document.getElementById("BtnBack").style.display = "inline-block";

    //.........................................
    if (item !== 8) {
        if (document.getElementById("DivLocation").style.display === "block") {
            PrevPage = "DivLocation";
        }
        else if (document.getElementById("DivSuitability").style.display === "block") {
            PrevPage = "DivSuitability";
        }
        else if (document.getElementById("DivTransportation").style.display === "block") {
            PrevPage = "DivTransportation";
        }
        else if (document.getElementById("DivBudget").style.display === "block") {
            PrevPage = "DivBudget";
        }
        else if (document.getElementById("DivResults").style.display === "block") {
            PrevPage = "DivResults";
        }
        else if (document.getElementById("AdvancedFeatureDefinition").style.display === "block") {
            PrevPage = "AdvancedFeatureDefinition";
        }
        else if (document.getElementById("MainPage").style.display === "block") {
            PrevPage = "MainPage";
        }
        else if (document.getElementById("MainItem").style.display === "block") {
            PrevPage = "MainItem";
        }

        stackOfBackButton.push(PrevPage);
    }
    //.........................................

    document.getElementById("DivLocation").style.display = "none";
    document.getElementById("DivSuitability").style.display = "none";
    document.getElementById("DivTransportation").style.display = "none";
    document.getElementById("DivBudget").style.display = "none";
    document.getElementById("DivResults").style.display = "none";
    document.getElementById("AdvancedFeatureDefinition").style.display = "none";
    document.getElementById("MainPage").style.display = "none";
    document.getElementById("MainItem").style.display = "none";
}
function Step(step) {

    if (CurrentStep === 0 && step === -1) {
        return;
    }
    else if (CurrentStep === 3 && step === 1) {
        return;
    }


    if (step > 0)
        CurrentStep++;
    else
        CurrentStep--;

    selectItem(CurrentStep);
}
function selectItem(item) {

    reset(item);

    if (item === 0) {
        document.getElementById("BtnNext").style.display = "inline-block";
        document.getElementById("DivLocation").style.display = "block";
        map.resize();
        map.invalidateSize();
    }
    else if (item === 1) {
        document.getElementById("BtnNext").style.display = "inline-block";
        document.getElementById("DivSuitability").style.display = "block";
    }
    else if (item === 2) {
        document.getElementById("BtnNext").style.display = "inline-block";
        document.getElementById("DivTransportation").style.display = "block";
    }
    else if (item === 3) {
        document.getElementById("BtnNext").style.display = "inline-block";
        document.getElementById("DivBudget").style.display = "block";
    }
    else if (item === 4) {

        if (ReqChanged) {

            ReqChanged = false;
            document.location = "Default.aspx?query=ShowMeTheResults";
        }
        else {
            document.getElementById("BtnNext").style.display = "inline-block";
            document.getElementById("lstFeasibleSolutions").innerHTML = lstSolutions;
            document.getElementById("DivResults").style.display = "block";
        }
    }
    else if (item === 5) {

        if (ReqChanged) {

            ReqChanged = false;
            document.location = "Default.aspx?query=ShowAdvancedFeatures";
        }
        else {
            document.getElementById("AdvancedFeatureDefinition").style.display = "block";
        }
    }
    else if (item === 6) {
       
        document.getElementById("MainItem").style.display = "block";
        if (sessionStorage.getItem("where") === null) {
            document.getElementById("txtWhere").innerText = "N/A";
        }
        else {       

            document.getElementById("txtWhere").innerText = sessionStorage.getItem("where");
            document.getElementById("btnWehere_items").style.backgroundColor = "pink";
        }

        if (sessionStorage.getItem("who") === null) {
            document.getElementById("txtWho").innerText = "N/A";
        }
        else {
            document.getElementById("txtWho").innerText = sessionStorage.getItem("who");
            document.getElementById("btnWho_items").style.backgroundColor = "pink";

            if (sessionStorage.getItem("who") === "single") {
                update_quick_selection_criteria("single", 0);
            }
            else if (sessionStorage.getItem("who") === "couple") {
                update_quick_selection_criteria("couple", 0);
            }
            else if (sessionStorage.getItem("who") === "family") {
                update_quick_selection_criteria("family", 0);
            }      
        }

        if (sessionStorage.getItem("transport") === null) {
            document.getElementById("txtTransport").innerText = "N/A";
        }
        else {
            document.getElementById("txtTransport").innerText = sessionStorage.getItem("transport");
            document.getElementById("btnTransport_items").style.backgroundColor = "pink";

            if (sessionStorage.getItem("transport") === "by car") {
                update_quick_selection_criteria("car", 0);
            }
            else if (sessionStorage.getItem("transport") === "by public transportation") {
                update_quick_selection_criteria("public", 0);
            }
            else if (sessionStorage.getItem("transport") === "by bike") {
                update_quick_selection_criteria("bike", 0);
            }
        }

        if (sessionStorage.getItem("cost") === null) {
            document.getElementById("txtCost").innerText = "N/A";
        }
        else {
            document.getElementById("txtCost").innerText = sessionStorage.getItem("cost");
            document.getElementById("btnCost_items").style.backgroundColor = "pink";

            if (sessionStorage.getItem("cost") === "low") {
                update_quick_selection_criteria("low", 0);
            }
            else if (sessionStorage.getItem("cost") === "medium") {
                update_quick_selection_criteria("medium", 0);
            }
            else if (sessionStorage.getItem("cost") === "high") {
                update_quick_selection_criteria("high", 0);
            }
        }
    }
    else if (item === 7) {// reset button
        stackOfBackButton.restStack();
        document.getElementById("MainPage").style.display = "block";
        document.getElementById("btnResetSelection").style.display = "none";
        document.getElementById("BtnBack").style.display = "none";
        document.getElementById("BtnNext").style.display = "none";

        sessionStorage.removeItem('where');
        sessionStorage.removeItem('who');
        sessionStorage.removeItem('transport');
        sessionStorage.removeItem('cost');

        UpdateCherryPickInc_Housing_Req("reset");
        ReqChanged = true;

    }
    else if (item === 8) { //back button

        curBtn = "";

        if (!stackOfBackButton.isEmpty()) {
            curBtn = stackOfBackButton.pop();
            document.getElementById(curBtn).style.display = "block";
        }
        else {
            document.getElementById("MainPage").style.display = "block";
            stackOfBackButton.push("MainPage");
            curBtn = "MainPage";
        }

        if (curBtn === "MainPage") {
            document.getElementById("btnResetSelection").style.display = "none";
            document.getElementById("BtnBack").style.display = "none";
        }
    }
}
//---------------------------------------------------- Map settings
mapboxgl.accessToken = 'pk.eyJ1Ijoic2lhbWFrZmFyc2hpZGkiLCJhIjoiY2s3dG5zaW0wMHg4czNtb3U1dWRwc2ZlbyJ9.yYhXI7_f9gBUYBAD_wS8Ug';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v9',
    center: [4.8945, 52.3667],
    zoom: 13
});
var geocoder = new MapboxGeocoder({
    accessToken: mapboxgl.accessToken,
    mapboxgl: mapboxgl
});
map.addControl(geocoder);
$('#SelectLocation').on('shown.bs.modal', function () { // chooseLocation is the id of the modal.
    map.resize();
});
map.on('load', function () {
    draw_circle_location();
});
function draw_circle_location() {
    map.addSource('single-point', {
        "type": "geojson",
        "data": {
            "type": "FeatureCollection",
            "features": []
        }
    });

    map.addLayer({
        "id": "point",
        "source": "single-point",
        "type": "circle",
        "paint": {
            "circle-radius": 1,
            "circle-color": "#007cbf"
        }
    });

    geocoder.on('result', function (ev) {

        var strSelectedLocation = ev.result.place_name;

        sessionStorage.setItem("where", ev.result.place_name);

        map.getSource('single-point').setData(ev.result.geometry);
        console.log(ev.result.geometry);

        var center = {
            "type": "Feature",
            "properties": {
                "marker-color": "#0f0"
            },
            "geometry": {
                "type": "Point",
                "coordinates": ev.result.geometry.coordinates
            }
        };

        var radius = 5;

        var options = { steps: 100, units: 'kilometers', properties: { foo: 'bar' } };

        var circle = turf.circle(center, radius, options);


        map.addLayer({
            "id": "circle-outline",
            "type": "line",
            "source": {
                "type": "geojson",
                "data": circle
            },
            "paint": {
                "line-color": "blue",
                "line-opacity": 0.5,
                "line-width": 2,
                "line-offset": 2
            },
            "layout": {

            }
        });
    });
}
//---------------------------------------------------- Message box
function showMessageBox(title, body) {
    document.getElementById("MessageTitle").innerText = title;
    document.getElementById("MessageText").innerHTML = body;

    $(document).ready(function () {

        $('#MessageBox').modal('show');
    });
}
//---------------------------------------------------- 
// beat the heart
// 'times' (int): nr of times to beat
function beatHeart(times) {
    var interval = setInterval(function () {
        $(".heartbeat").fadeIn(500, function () {
            $(".heartbeat").fadeOut(500);
        });
    }, 1000); // beat every second

    // after n times, let's clear the interval (adding 100ms of safe gap)
    setTimeout(function () { clearInterval(interval); }, 1000 * times + 100);
}
$(function () {
    // just keeping beating 2 times, each 3 seconds
    setInterval(function () { beatHeart(2); }, 3000);

});
function setHeartbeat() {
    setTimeout("heartbeat()", 300000); // every 5 min
}
function heartbeat() {
    $.get(
        "GenericHandlers/SessionHeartbeat.ashx",
        null,
        function (data) {
            //$("#heartbeat").show().fadeOut(1000); // just a little "red flash" in the corner :)
            setHeartbeat();
        },
        "json"
    );
}
beatHeart(2);
//---------------------------------------------------- 
var DecisionModel = null;
DecisionModel = "";
//----------------------------------------------------Bar and Pie charts
function drawChart_PieChart() {
    var data = google.visualization.arrayToDataTable(QualityAttributesRatio);

    var options = {
        title: 'Impacts of the selected feature requirements on quality attributes:',
        is3D: true,
        legend: { position: 'left', textStyle: { color: 'white' } },
        backgroundColor: 'transparent',
        chartArea: { left: 0, top: 50, width: "100%", height: "100%" },
        titleTextStyle: {
            color: 'white',
            fontSize: 14,
            bold: true
        }
    };

    var chart = new google.visualization.PieChart(document.getElementById('piechart_3d'));
    chart.draw(data, options);
}
function drawChart_BarChart() {
    var data = google.visualization.arrayToDataTable(FeasibleSolutionsScores);

    var view = new google.visualization.DataView(data);
    view.setColumns([0, 1,
        {
            calc: "stringify",
            sourceColumn: 1,
            type: "string",
            role: "annotation"
        },
        2]);

    var options = {
        title: "Top-10 feasible solutions:",
        backgroundColor: 'transparent',
        chartArea: { width: 350, height: 300 },
        bar: { groupWidth: "95%" },
        legend: { position: "none" },
        titleTextStyle: {
            color: 'white',
            fontSize: 14,
            bold: true
        },
        hAxis: { minValue: 0, maxValue: 100, textStyle: { color: '#FFF' } },
        vAxis: { textStyle: { color: '#FFF' } }

    };
    var chart = new google.visualization.BarChart(document.getElementById("barchart_values"));
    chart.draw(view, options);
}
//----------------------------------------------------Decision Structure
function init() {
    if (window.goSamples) goSamples();  // init for these samples -- you don't need to call this
    var $ = go.GraphObject.make;  // for conciseness in defining templates
    myDiagram =
        $(go.Diagram, "DecisionStructure",  // must be the ID or reference to div
            {
                initialAutoScale: go.Diagram.UniformToFill,
                layout: $(go.LayeredDigraphLayout)
                // other Layout properties are set by the layout function, defined below
            });
    // define the Node template
    myDiagram.nodeTemplate =
        $(go.Node, "Spot",
            { locationSpot: go.Spot.Center },
            $(go.Shape, "Rectangle",
                {
                    fill: "lightyellow",  // the initial value, but data-binding may provide different value
                    stroke: null,
                    desiredSize: new go.Size(148, 15)
                },
                new go.Binding("stroke", "fill")),
            $(go.TextBlock,
                new go.Binding("text", "text"), { font: "9px sans-serif" })
        );
    // define the Link template to be minimal
    myDiagram.linkTemplate =
        $(go.Link,
            { selectable: false },
            $(go.Shape,
                { strokeWidth: 1, stroke: "white" }));
    // generate a tree with the default values
    rebuildGraph();
}
//---------------------------------------------------- DropDown Infeasible Solution
function autoComplete() {
    //document.getElementById("spnInfeasibleList").remove();
    //$("#DD_Placeholder").append("<span class='autocomplete-select' id='spnInfeasibleList'></span>");

    //document.getElementById("DecisionStructure").remove();
    //$("#PlnDecisionStructure").append("<div id='DecisionStructure' style='width: 100%; font-size: xx-small; height: 630px; background-color: #435C70; border: 2px solid #435C70;'></div >");

    //var autocomplete = new SelectPure(".autocomplete-select", {

    //    options: ListOfInfeasibleSolutions,
    //    value: [],
    //    multiple: true,
    //    autocomplete: true,
    //    icon: "fa fa-times",
    //    onChange: value => { ListOfSelectedInfeasibleSolutionsChanges(value); }
    //});

    //google.charts.load("current", { packages: ["corechart"] });
    //google.charts.setOnLoadCallback(drawChart_PieChart);
    //google.charts.setOnLoadCallback(drawChart_BarChart);

    //init();
}
var CurrentListOfInfeasibleSolutions = [];
function ListOfSelectedInfeasibleSolutionsChanges(value) {

    if (CurrentListOfInfeasibleSolutions.length < value.length) {
        CurrentListOfInfeasibleSolutions.push(value[value.length - 1]);
        Add_InfeasibleSolution_DecisionMatrix(CurrentListOfInfeasibleSolutions[CurrentListOfInfeasibleSolutions.length - 1]);
    }
    else if (CurrentListOfInfeasibleSolutions.length > value.length) {
        Index = getRemovedItemIndex(value);
        Remove_InfeasibleSolution_DecisionMatrix(CurrentListOfInfeasibleSolutions[Index]);
        CurrentListOfInfeasibleSolutions.splice(Index, 1);
    }
}
var getRemovedItemIndex = function (value) {

    var found = false;

    for (i = 0; i < CurrentListOfInfeasibleSolutions.length; i++) {
        found = false;
        for (j = 0; j < value.length; j++) {
            if (CurrentListOfInfeasibleSolutions[i] === value[j]) {
                found = true;
                break;
            }
        }
        if (!found)
            return i;
    }
    return -1;
};
var getNameByID = function (ID) {

    for (i = 0; i < ListOfInfeasibleSolutions.length; i++)
        if (ListOfInfeasibleSolutions[i].value === ID)
            return ListOfInfeasibleSolutions[i].label;

    return "";
};
function Add_InfeasibleSolution_DecisionMatrix(ID) {
    Name = getNameByID(ID);

    if (!table_decision_matrix.getColumn("A" + ID))
        table_decision_matrix.addColumn({ title: Trim(Name, 15), field: "A" + ID, align: "center", formatter: "tickCross", headerSort: true, headerVertical: true, headerTooltip: Name }, false, "MoSCoW");
    GetInfeasibleSolution({ "Name": Name, "ID": ID });
}
function Trim(str, length) {
    appendix = "...";
    delim = " ";

    if (str.length <= length) return str;

    var trimmedStr = str.substr(0, length + delim.length);

    var lastDelimIndex = trimmedStr.lastIndexOf(delim);
    if (lastDelimIndex >= 0) trimmedStr = trimmedStr.substr(0, lastDelimIndex);

    if (trimmedStr) trimmedStr += appendix;
    return trimmedStr;
}
function Remove_InfeasibleSolution_DecisionMatrix(ID) {

    if (table_decision_matrix.getColumn("A" + ID))
        table_decision_matrix.deleteColumn("A" + ID);
}
//----------------------------------------------------Feature Requirement
var InfoIcon = function (cell) {
    var row = cell.getRow();
    if (row.getData().FeatureDataType !== "Category") {
        return '<i style="color:#A11664;font-size:20px;" class="fas fa-info-circle"></i>';
    }
};
var DotsIcon = function (cell) {
    var row = cell.getRow();
    quickSelectionValueCheck_CherryPiuckIncHousing(row);

    if (row.getData().FeatureDataType !== "Category") {
        return getDotsByMoSCoW(row.getData().MoSCoW);
    }
};



function quickSelectionValueCheck_CherryPiuckIncHousing(row) {

    if (row.getData().Feature === "Bike parking" && row.getData().MoSCoW === "S") {
        sessionStorage.setItem("transport", "by bike");
    }
    else if (row.getData().Feature === "Near to a public bus station" && row.getData().MoSCoW === "S") {
        sessionStorage.setItem("transport", "by public transportation");
    }
    else if (row.getData().Feature === "Has a parking" && row.getData().MoSCoW === "S") {
        sessionStorage.setItem("transport", "by car");
    }
    else if (row.getData().Feature === "Suitable only for one person" && row.getData().MoSCoW === "S") {
        sessionStorage.setItem("who", "single");
    }
    else if (row.getData().Feature === "Suitable only for a couple" && row.getData().MoSCoW === "S") {
        sessionStorage.setItem("who", "couple");
    }
    else if (row.getData().Feature === "Suitable only for a a family" && row.getData().MoSCoW === "S") {
        sessionStorage.setItem("who", "family");
    }
    else if (row.getData().Feature === "Less than 500 EUR" && row.getData().MoSCoW === "S") {
        sessionStorage.setItem("cost", "low");
    }
    else if (row.getData().Feature === "Less than 1000 EUR" && row.getData().MoSCoW === "S") {
        sessionStorage.setItem("cost", "medium");
    }
    else if (row.getData().Feature === "Less than 2000 EUR" && row.getData().MoSCoW === "S") {
        sessionStorage.setItem("cost", "high");

    }
}

function getDotsByMoSCoW(MoSCoW) {
    if (MoSCoW === "N")
        return '<i style="color:#A11664;font-size:15px;" class="far fa-circle"></i><i style="color:#A11664;font-size:15px;" class="far fa-circle"></i><i style="color:#A11664;font-size:15px;" class="far fa-circle"></i>';
    else if (MoSCoW === "C")
        return '<i style="color:#A11664;font-size:15px;" class="fas fa-circle"></i><i style="color:#A11664;font-size:15px;" class="far fa-circle"></i><i style="color:#A11664;font-size:15px;" class="far fa-circle"></i>';
    else if (MoSCoW === "S")
        return '<i style="color:#A11664;font-size:15px;" class="fas fa-circle"></i><i style="color:#A11664;font-size:15px;" class="fas fa-circle"></i><i style="color:#A11664;font-size:15px;" class="far fa-circle"></i>';
    else if (MoSCoW === "M")
        return '<i style="color:#A11664;font-size:15px;" class="fas fa-circle"></i><i style="color:#A11664;font-size:15px;" class="fas fa-circle"></i><i style="color:#A11664;font-size:15px;" class="fas fa-circle"></i>';
}
var CurrentColor = "";
var table_feature_requirements = new Tabulator("#Table_DomainFeatureRequirement", {
    height: "500px",
    data: FeatureRequirement_datatable, //assign data to table
    layout: "fitColumns",
    headerFilterPlaceholder: "Find Features...",
    selectable: 1, //make rows selectable
    dataTree: true,
    dataTreeBranchElement: true,
    dataTreeStartExpanded: false,
    dataTreeElementColumn: "Feature",
    tooltipsHeader: false,
    columns: [
        { title: "FeatureID", field: "FeatureID", sorter: "string", width: 250, visible: false },
        { title: "Feature Requirement", field: "Feature", sorter: "string", width: "60%" },
        {
            title: "MoSCoW", field: "MoSCoW", sorter: "string", visible: false, editor: "select",
            editorParams: function (cell) {
                var row = cell.getRow();
                if (row.getData().FeatureDataType !== "Category") {
                    return { "N": "N", "M": "M", "S": "S", "C": "C", "W": "W" };
                }
                return {};
            },
            width: 98,
            cellEdited: function (cell) {

                var row = cell.getRow();
                if (row.getData().FeatureDataType !== "Category") {
                    ID = row.getData().FeatureID;
                    if (cell.getValue() === "None")
                        Req = "N";
                    else
                        Req = getMoSCoW(cell.getValue());
                    UpdateFeatureRequirements_MoSCoW(ID, Req);
                }
            }
        },
        { title: "Importance", field: "Importance", formatter: DotsIcon, align: "center", width: "20%" },
        {
            title: "Info", field: "Info", formatter: InfoIcon, align: "center", width: "20%", cellClick: function (e, cell) {
                var row = cell.getRow();
                if (row.getData().FeatureDataType !== "Category") {
                    showMessageBox(row.getData().Feature, row.getData().Description);
                }
                e.stopPropagation();
            }
        },
        {
            title: "Description", field: "Description", sorter: "string", visible: false,
            formatter: function (cell, formatterParams, onRendered) {
                var row = cell.getRow();
                if (row.getData().FeatureDataType === "Category") {
                    row.getElement().style.backgroundColor = "#fff";
                    row.getElement().style.color = "black";
                    row.getElement().style.fontWeight = "bold";
                }
                else {
                    CurMoSCoW = row.getData().MoSCoW;
                    row.getElement().style.backgroundColor = getRowBackgroundColor(CurMoSCoW);
                }
            }
        }, //hide this column first
        { title: "FeatureDataType", field: "FeatureDataType", sorter: "string", visible: false }, //hide this column first
        { title: "FeatureCategory", field: "FeatureCategory", sorter: "string", visible: false }, //hide this column first
        { title: "FeatureParent", field: "FeatureParent", sorter: "string", visible: false }, //hide this column first
        { title: "FeatureSupportedAlternatives", field: "FeatureSupportedAlternatives", sorter: "string", visible: false } //hide this column first
    ],
    rowClick: function (e, row) {
        if (row.getData().FeatureDataType !== "Category") {

            CurMoSCoW = getNextPriority(row.getData().MoSCoW);
            CurrentColor = getRowBackgroundColor(CurMoSCoW);
            row.getElement().style.backgroundColor = CurrentColor;

            ID = row.getData().FeatureID;
            Req = CurMoSCoW;
            UpdateFeatureRequirements_MoSCoW(ID, Req);
            ReqChanged = true;

            row.update({ "MoSCoW": CurMoSCoW })
                .then(function () {
                    //run code after data has been updated
                })
                .catch(function (error) {
                    //handle error updating data
                });


            row.update({ "Importance": getDotsByMoSCoW(CurMoSCoW) })
                .then(function () {
                    //run code after data has been updated
                })
                .catch(function (error) {
                    //handle error updating data
                });


        }
    },
    rowMouseOver: function (e, row) {
        CurrentColor = row.getElement().style.backgroundColor;
        row.getElement().style.backgroundColor = "orange";
        row.getElement().style.fontWeight = "bold";
    },
    rowMouseOut: function (e, row) {
        row.getElement().style.backgroundColor = CurrentColor;
        if (row.getData().FeatureDataType !== "Category")
            row.getElement().style.fontWeight = "200";
    }
});
document.getElementById("AdvancedFeatureDefinition").style.display = "none";
function getRowBackgroundColor(MoSCoW) {
    if (MoSCoW === "C")
        return "#ffa0bd";
    else if (MoSCoW === "S")
        return "#ff7ea7";
    else if (MoSCoW === "M")
        return "#ff5593";
    else if (MoSCoW === "N")
        return "#fff";
}
function getNextPriority(MoSCoW) {
    if (MoSCoW === "N")
        return "C";
    else if (MoSCoW === "C")
        return "S";
    else if (MoSCoW === "S")
        return "M";
    else if (MoSCoW === "M")
        return "N";
}
var UpdateJasonElementByID = function (JasonDataset, FeatureID, Key, Value) {
    var i = null;
    for (i = 0; JasonDataset.length > i; i += 1) {
        if (JasonDataset[i].id === FeatureID) {
            JasonDataset[i][Key] = Value;
            return JasonDataset;
        }
        if ('_children' in JasonDataset[i]) {

            var j = null;
            for (j = 0; j < JasonDataset[i]._children.length; j++) {
                if (JasonDataset[i]._children[j].id === FeatureID) {
                    JasonDataset[i]._children[j][Key] = Value;
                    return JasonDataset;
                }
                if ('_children' in JasonDataset[i]._children[j]) {
                    for (k = 0; k < JasonDataset[i]._children[j]._children.length; k++) {
                        if (JasonDataset[i]._children[j]._children[k].id === FeatureID) {
                            JasonDataset[i]._children[j]._children[k][Key] = Value;
                            return JasonDataset;
                        }
                    }
                }
            }
        }
    }
    return null;
};
var FlattenDataSet = function (DataSet) {
    var txtDataSet = JSON.stringify(DataSet);
    var i = null;
    for (i = 0; i < txtDataSet.split('{').length; i++) {
        txtDataSet = txtDataSet.replace(',"_children":[', '},');
        txtDataSet = txtDataSet.replace(']}', '');
    }
    return JSON.parse(txtDataSet);
};
var SerachFeatures = function (MainDataSet, searchTerm) {

    searchTerm = searchTerm.toLowerCase();
    DataSet = FlattenDataSet(MainDataSet);
    DataSet = DataSet.filter(e => RegExp(searchTerm, 'i').test(e.Feature) || RegExp(searchTerm, 'i').test(e.Description));

    return DataSet;
};
function Synchronization(FlatDataSet, OriginalDataSet) {
    for (i = 0; i < FlatDataSet.length; i++) {
        OriginalDataSet = UpdateJasonElementByID(OriginalDataSet, FlatDataSet[i].id, 'MoSCoW', FlatDataSet[i].MoSCoW);
        OriginalDataSet = UpdateJasonElementByID(OriginalDataSet, FlatDataSet[i].id, 'FeatureCriterionValue', FlatDataSet[i].FeatureCriterionValue);
    }

    return OriginalDataSet;
}
//---------------------------------------------------- Ajax
function UpdateCase() {
    JsonCase = { "title": document.getElementById("txttitle").value, "explanation": document.getElementById("txtdescription").value };
    var postdata = JSON.stringify(JsonCase);

    try {
        $.ajax({
            type: "POST",
            url: "GenericHandlers/UpdateCase.ashx",
            cache: false,
            data: postdata,
            success: getSuccess,
            error: getFail
        });
    } catch (e) {
        alert(e);
    }
    function getSuccess(data, textStatus, jqXHR) {

        showMessageBox("Update", "The case was successfully updated!");
    }

    function getFail(jqXHR, textStatus, errorThrown) {
        alert(jqXHR.status);
    }
}
var _URL = window.URL || window.webkitURL;
$("#f_UploadImage").on('change', function () {

    var file = this.files[0], img;
    if (file) {
        img = new Image();
        img.onload = function () {
            sendImage(file);
        };
        img.onerror = function () {
            alert("Not a valid file:" + file.type);
        };
        img.src = _URL.createObjectURL(file);
    }
});
function sendImage(file) {

    var formData = new FormData();
    formData.append('file', $('#f_UploadImage')[0].files[0]);
    $.ajax({
        type: 'post',
        url: 'GenericHandlers/fileUploader.ashx',
        data: formData,
        success: function (status) {
            if (status !== 'error') {
                var my_path = "Image/Cases/" + status;
                $("#myUploadedImg").attr("src", my_path);
            }
        },
        processData: false,
        contentType: false,
        error: function () {
            alert("Uploading failed!");
        }
    });
}
$("#f_DecisionModel").on('change', function () {

    var file = this.files[0], img;
    if (file) {
        if (file.type === "text/xml") {
            sendFile(file);
        }
        else {
            alert("Not a valid file:" + file.type);
        }
    }
});
function sendFile(file) {

    var formData = new FormData();
    formData.append('file', $('#f_DecisionModel')[0].files[0]);
    $.ajax({
        type: 'post',
        url: 'GenericHandlers/DecisionModelUploader.ashx',
        data: formData,
        success: function (status) {
            if (status !== 'error') {

                result = status.split(";");
                window.location = "CaseDefinition.aspx?OpenDecisionModel=" + result[0] + "&PageCaption=" + result[1];
            }
        },
        processData: false,
        contentType: false,
        error: function () {
            alert("Uploading failed!");
        }
    });
}
function UpdateFeatureRequirements_MoSCoW(ID, Req) {
    var postdata = JSON.stringify({ "ID": ID, "Req": Req });
    $.ajax({
        type: 'post',
        url: 'GenericHandlers/UpdateFeatureRequirements_MoSCoW.ashx',
        cache: false,
        data: postdata,
        success: function (status) {
            // alert(status);
        },
        error: function () {
            alert("Updating MoSCoW priorities failed!");
        }
    });
}

function UpdateCherryPickInc_Housing_Req(criterion) {
    var postdata = JSON.stringify({ "criterion": criterion });
    $.ajax({
        type: 'post',
        url: 'GenericHandlers/CherryPickInc_Housing_Req.ashx',
        cache: false,
        data: postdata,
        success: function (status) {
            // alert(status);
        },
        error: function () {
            alert("Updating CherryPickInc criteria failed!");
        }
    });
}



function UpdateFeatureRequirements_Criterion(ID, Val) {
    var postdata = JSON.stringify({ "ID": ID, "Val": Val });
    $.ajax({
        type: 'post',
        url: 'GenericHandlers/UpdateFeatureRequirements_Criterion.ashx',
        cache: false,
        data: postdata,
        success: function (status) {
            //  alert(status);
        },
        error: function () {
            alert("Updating criteria failed!");
        }
    });
}
function MakeDecision() {
    $.ajax({
        url: 'GenericHandlers/MakeDecision.ashx',
        timeout: 60000,
        error: function (jqXHR, textStatus) {
            location.reload(true);
        },
        success: function (status) {
            if (status < 1)
                showMessageBox("Feasible solutions", "<div style='margin:15px;'> No feasible solution found! <br /> Please revise your feature requirements.</div>");

            ReloadScriptFile('XML_DB/Profiles/' + UID + '/JS/DecisionMatrix.js');
            ReloadScriptFile('XML_DB/Profiles/' + UID + '/JS/ListOfInfeasibleSolutions.js');
            ReloadScriptFile('XML_DB/Profiles/' + UID + '/JS/PieChartData.js');
            ReloadScriptFile('XML_DB/Profiles/' + UID + '/JS/BarGraphData.js');
            ReloadScriptFile('XML_DB/Profiles/' + UID + '/JS/DecisionStructure.js');

            table_decision_matrix.clearData();
            table_decision_matrix.setColumns(DecisionMatrix_Columns);
            table_decision_matrix.setData(DecisionMatrix_datatable);
        }
    });
}
function ReloadScriptFile(JSFile) {
    $("script").each(function () {
        var oldScript = this.getAttribute("src");
        if (oldScript === JSFile) {
            $(this).remove();
            var newScript;
            newScript = document.createElement('script');
            newScript.type = 'text/javascript';
            newScript.src = oldScript;
            document.getElementsByTagName("head")[0].appendChild(newScript);
        }
    });
}
function GetInfeasibleSolution(InfeasibleSolutionData) {
    var postdata = JSON.stringify(InfeasibleSolutionData);
    try {
        $.ajax({
            type: "POST",
            url: "GenericHandlers/UpdateInfeasibleList.ashx",
            cache: false,
            data: postdata,
            success: getSuccess,
            error: getFail
        });
    } catch (e) {
        alert(e);
    }
    function getSuccess(data, textStatus, jqXHR) {
        UpdateDecisionMatrix(data, InfeasibleSolutionData);
    }
    function getFail(jqXHR, textStatus, errorThrown) {
        alert(jqXHR.status);
    }
}
//----------------------------------------------------Update Decision Matrix
function UpdateDecisionMatrix(FeatureRequirements, InfeasibleSolutionData) {
    var Features = FeatureRequirements.split(';');
    for (i = 0; i < Features.length; i++) {
        Feature = Features[i].split(',');
        for (j = 0; j < DecisionMatrix_datatable.length; j++) {
            if (Feature[0] === DecisionMatrix_datatable[j].FeatureID) {
                DecisionMatrix_datatable[j]["A" + InfeasibleSolutionData.ID] = Feature[1] === "true" ? true : false;

            }
        }
    }

    table_decision_matrix.setData(DecisionMatrix_datatable);
}
//---------------------------------------------------- Update the list of updates in the knowledge base
function AddUpdate(NewUpdate) {

    isDuplicate = 0;

    for (i = 0; i < ListOfUpdates["Updates"].length; i++) {
        if (ListOfUpdates["Updates"][i].ID === NewUpdate.ID && ListOfUpdates["Updates"][i].UF === NewUpdate.UF) {
            ListOfUpdates["Updates"][i].Val = NewUpdate.Val;
            isDuplicate = 1;
            break;
        }
    }

    if (isDuplicate === 0)
        ListOfUpdates["Updates"].push(NewUpdate);
}
//---------------------------------------------------- Event Handlers
SearchCriteria_OnBlur();
$("#UpdateFeatures").click(function () {
    selectItem(4);
    //if (ListOfUpdates["Updates"].length > 0)
    //    UpdateKnowledgeBase();
});
$("#updateDefinition").click(function () {
    UpdateCase();
});
$("#ExtractFeatures").click(function () {

    showMessageBox('title', 'body');
});
$("#btnShow_Report").click(function () {
    window.open('ExtraPage/PrintableReport.aspx', '_blank');
});
function ClearSearchCriteria() {
    document.getElementById("SearchCriteria").value = "Find features...";
    document.getElementById("SearchCriteria").style.fontStyle = "italic";
    document.getElementById("SearchCriteria").style.fontSize = "small";
    document.getElementById("SearchCriteria").style.color = "#D0D3D4";
}
function SearchCriteria_OnBlur() {
    if (document.getElementById("SearchCriteria").value === "") {
        ClearSearchCriteria();
    }
}
function SearchCriteria_OnFocus() {
    if (document.getElementById("SearchCriteria").value === "Find features...") {
        document.getElementById("SearchCriteria").value = "";
        document.getElementById("SearchCriteria").style.fontStyle = "normal";
        document.getElementById("SearchCriteria").style.fontSize = "medium";
        document.getElementById("SearchCriteria").style.color = "black";
    }
}
$("#btn_SearchForFeatures").click(function () {
    if (document.getElementById("SearchCriteria").value !== "Find features...") {
        FeatureRequirement_datatable = Synchronization(FeatureRequirement_datatable, DuplicateDataset);
        FeatureRequirement_datatable = SerachFeatures(FeatureRequirement_datatable, document.getElementById("SearchCriteria").value);
        table_feature_requirements.setData(FeatureRequirement_datatable);
    }
});
$("#btnDownload").click(function () {
    window.location = "ExtraPage/DownloadFile.aspx";
});
$("#btn_AllFeatures").click(function () {
    FeatureRequirement_datatable = Synchronization(FeatureRequirement_datatable, DuplicateDataset);
    table_feature_requirements.setData(FeatureRequirement_datatable);
    ClearSearchCriteria();
});
$("#SearchCriteria").keyup(function (event) {
    if (document.getElementById("SearchCriteria").value === "") {
        FeatureRequirement_datatable = Synchronization(FeatureRequirement_datatable, DuplicateDataset);
        table_feature_requirements.setData(FeatureRequirement_datatable);
    }
    else
        $("#btn_SearchForFeatures").click();
});
var getMoSCoW = function (Priority) {

    switch (Priority) {
        case "Must-Have": return "M";
        case "Should-Have": return "S";
        case "Could-Have": return "C";
        case "Won't-Have": return "W";
    }
};
//----------------------------------------------------
if (qs["query"] === "ShowMeTheResults") {
    selectItem(4);
    window.history.replaceState(null, null, "Default");
}
else if (qs["query"] === "ShowAdvancedFeatures") {

    ReloadScriptFile('XML_DB/Profiles/' + UID + '/JS/FeatureRequirements.js');
    table_feature_requirements.clearData();
    table_feature_requirements.setData(FeatureRequirement_datatable);

    selectItem(5);
    window.history.replaceState(null, null, "Default");
}

//----------------------------------------------------

function reset_Transportation_panel() {
    document.getElementById("plnParking").style.borderColor = "#A11664";
    document.getElementById("plnParking").style.color = "#A11664";

    document.getElementById("plnPublic").style.borderColor = "#A11664";
    document.getElementById("plnPublic").style.color = "#A11664";

    document.getElementById("plnBike").style.borderColor = "#A11664";
    document.getElementById("plnBike").style.color = "#A11664";

    document.getElementById("plnsingle").style.borderColor = "#A11664";
    document.getElementById("plnsingle").style.color = "#A11664";

    document.getElementById("plncouple").style.borderColor = "#A11664";
    document.getElementById("plncouple").style.color = "#A11664";

    document.getElementById("plnfamily").style.borderColor = "#A11664";
    document.getElementById("plnfamily").style.color = "#A11664";

    document.getElementById("plnlow").style.borderColor = "#A11664";
    document.getElementById("plnlow").style.color = "#A11664";

    document.getElementById("plnmedium").style.borderColor = "#A11664";
    document.getElementById("plnmedium").style.color = "#A11664";

    document.getElementById("plnhigh").style.borderColor = "#A11664";
    document.getElementById("plnhigh").style.color = "#A11664";
}

function update_quick_selection_criteria(criterion, action) {

    ReqChanged = true;
    reset_Transportation_panel();

    if (criterion === "parking") {
        document.getElementById("plnParking").style.borderColor = "darkorange";
        document.getElementById("plnParking").style.color = "darkorange";

        if (action === 1)
            UpdateCherryPickInc_Housing_Req("car");

        sessionStorage.setItem("transport", "by car");
    }
    else if (criterion === "public") {
        document.getElementById("plnPublic").style.borderColor = "darkorange";
        document.getElementById("plnPublic").style.color = "darkorange";

        if (action === 1)
            UpdateCherryPickInc_Housing_Req("public");

        sessionStorage.setItem("transport", "by public transportation");
    }
    else if (criterion === "bike") {
        document.getElementById("plnBike").style.borderColor = "darkorange";
        document.getElementById("plnBike").style.color = "darkorange";

        if (action === 1)
            UpdateCherryPickInc_Housing_Req("bike");

        sessionStorage.setItem("transport", "by bike");
    }

    else if (criterion === "single") {
        document.getElementById("plnsingle").style.borderColor = "darkorange";
        document.getElementById("plnsingle").style.color = "darkorange";

        if (action === 1)
            UpdateCherryPickInc_Housing_Req("single");


        sessionStorage.setItem("who", "single");
    }

    else if (criterion === "couple") {
        document.getElementById("plncouple").style.borderColor = "darkorange";
        document.getElementById("plncouple").style.color = "darkorange";

        if (action === 1)
            UpdateCherryPickInc_Housing_Req("couple");


        sessionStorage.setItem("who", "couple");
    }

    else if (criterion === "family") {
        document.getElementById("plnfamily").style.borderColor = "darkorange";
        document.getElementById("plnfamily").style.color = "darkorange";

        if (action === 1)
            UpdateCherryPickInc_Housing_Req("family");


        sessionStorage.setItem("who", "family");
    }

    else if (criterion === "low") {
        document.getElementById("plnlow").style.borderColor = "darkorange";
        document.getElementById("plnlow").style.color = "darkorange";

        if (action === 1)
            UpdateCherryPickInc_Housing_Req("low");

        sessionStorage.setItem("cost", "low");
    }
    else if (criterion === "medium") {
        document.getElementById("plnmedium").style.borderColor = "darkorange";
        document.getElementById("plnmedium").style.color = "darkorange";

        if (action === 1)
            UpdateCherryPickInc_Housing_Req("medium");

        sessionStorage.setItem("cost", "medium");
    }
    else if (criterion === "high") {
        document.getElementById("plnhigh").style.borderColor = "darkorange";
        document.getElementById("plnhigh").style.color = "darkorange";

        if (action === 1)
            UpdateCherryPickInc_Housing_Req("high");

        sessionStorage.setItem("cost", "high");
    }
}
//----------------------------------------------------
