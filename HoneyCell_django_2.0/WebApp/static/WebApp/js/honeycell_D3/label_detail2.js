var margin = {top: 20, right: 20, bottom: 30, left: 100},
    width_detail = 700 - margin.left - margin.right,
    height_detail = 350 - margin.top - margin.bottom;

var y0_detail = d3.scale.ordinal()
    .rangeRoundBands([height_detail, 0], .1);

var y1_detail = d3.scale.ordinal();


var x_detail = d3.scale.linear()
    .range([0, width_detail-100]);

var color = d3.scale.ordinal()
    .range(["rgb(239, 142, 173)", "rgb(213, 161, 102)", "rgb(122, 186, 127)", "rgb(0, 189, 213)", "#DDD"]);

var yAxis_detail = d3.svg.axis()
    .scale(y0_detail)
    .orient("left")
    .tickSize(0,0);


var xAxis_detail = d3.svg.axis()
    .scale(x_detail)
    .orient("bottom")
    .tickSize(height_detail)
    //.tickFormat(d3.format(".2f"));


var tip_detail = d3.tip()
      .attr('class', 'd3_tip_detail')
      .direction('e')
      .offset([0, 2])
      .html(function(d) {
        return "<strong>" + d.name +":</strong> <span style='color:red'>" + 
                d.value + "</span>";
    });
  

var svg_detail = d3.select("#label_detail")
    .append("svg")
    .attr("width", width_detail + margin.left + margin.right)
    .attr("height", height_detail + margin.top + margin.bottom)
    .attr("id", "label_detail_D3")
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

svg_detail.call(tip_detail);




var data = [];
var task_id = document.getElementById("task_id").value;

d3.json("/get_json_result/" + task_id, function(error, apidata) {

 apidata = JSON.parse(apidata);

 var object = {};
  for(var i = apidata.LabelNum-1; i >= 0; i--) {
    object["labels"+i] = {
      "F1Measure" : apidata.Labels[i].F1Measure,
      "Recall" : apidata.Labels[i].Recall,
      "Precision" : apidata.Labels[i].Precision
    }
  }
  var data = Object.keys(object).map(function(key){
    return {
      name : key,
      categories: Object.keys(object[key]).map(function(cat_name){
        return {
          name: cat_name,
          value: object[key][cat_name] 
        }
      })
    }
  });

  // data = new Array(data);
  console.log(data);
  var categories =['F1Measure','Recall','Precision'];
  y0_detail.domain(data.map(function(d){ return d.name; }));
  y1_detail.domain(categories).rangeRoundBands([0, y0_detail.rangeBand()], 0.15);
  x_detail.domain([0, d3.max(data, function(city) {
    return d3.sum(city.categories, function(d) { return d.value; });
  })]);
  svg_detail.append("g")
      .attr("class", "y axis_label_detail")
      .call(yAxis_detail);

  svg_detail.append("g")
      .attr("class", "x axis_label_detail")
      .call(xAxis_detail)
      .append("text")
      .attr("x", width_detail)
      .attr("y", height_detail+5)
      .attr("dy", ".71em")
      .style("text-anchor", "end")


  var totals = svg_detail.selectAll(".total_bar")
      .data(data, function(d){ return d.name; })
      .enter()
      .append("rect")
      .attr("class", "total_bar")
      .attr("height", y0_detail.rangeBand())
      .attr("x", 2) 
      .attr("y", function(d) { return y0_detail(d.name); })
      .attr("width", 0);

  totals.transition()
    .duration(600)
    .ease("linear")
    .attr("width", function(city) {
          return x_detail(d3.sum(city.categories, function(d) { return d.value; }));
    });

  var zero=d3.format(".4s");

  totals.append("title")
    .text(function(city){
      return "Total: " + zero(d3.sum(city.categories, function(d) { return d.value; }))
    })

  var cities = svg_detail.selectAll(".city")
      .data(data, function(d){ return d.name; })
      .enter().append("g")
      .attr("class", "city")
      .attr("transform", function(d) { return "translate(0," + y0_detail(d.name) + ")"; });
  
  var detail_bar = cities.selectAll(".detail_bar")
      .data(function(city) { return city.categories; }, function(d){ return d.name; })
      .enter()
      .append("rect")
      .attr("class", "detail_bar")
      .attr("height", y1_detail.rangeBand())
      .attr("x", 2) 
      .attr("y", function(d) { return y1_detail(d.name); })
      .attr("width", 0)
      .style("fill", function(d) { return color(d.name); })
      .on('mouseover', tip_detail.show)
      .on('mouseout', tip_detail.hide)
      ;
      
  detail_bar.transition()
      .duration(600)
      .ease("linear")
      .attr("width", function(d) { return x_detail(d.value)});


 
  var legend = svg_detail.selectAll(".legend")
      .data(categories.concat(["total"]))
      .enter()
      .append("g")
      .attr("class", "legend")
      .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

  legend.append("rect")
      .attr("x", width_detail-100)
      .attr("width", 18)
      .attr("height", 18)
      .style("fill", color);

  legend.append("text")
      .attr("x", width_detail - 70)
      .attr("y", 9)
      .attr("dy", ".35em")
      .style("text-anchor", "start")
      .text(function(d) { return d; });



})