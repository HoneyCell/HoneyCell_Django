/**
 * Created by jianheluo on 4/18/16.
 */



var trueData = [
    {label: "Label1", color: "#3366CC", value: 50},
    {label: "Label2", color: "#DC3912", value: 50},
    {label: "Label3", color: "#FF9900", value: 50},
];

var predictData = [
    {label: "Label1", color: "#3366CC", value: 59},
    {label: "Label2", color: "#DC3912", value: 49},
    {label: "Label3", color: "#FF9900", value: 42},
];


var svg = d3.select("body").append("svg").attr("width", 700).attr("height", 300);

svg.append("g").attr("id", "salesDonut");
svg.append("g").attr("id", "quotesDonut");

Donut3D.draw("salesDonut", randomData(), 150, 150, 130, 100, 30, 0.4);
Donut3D.draw("quotesDonut", randomData2(), 450, 150, 130, 100, 30, 0);


function randomData() {

    var result = trueData.map(function (d) {
        return {label: d.label, value: d.value, color: d.color};
    });

    console.log(result);

    return result;
}

function randomData2() {

    var result = predictData.map(function (d) {
        return {label: d.label, value: d.value, color: d.color};
    });

    console.log(result);

    return result;
}
