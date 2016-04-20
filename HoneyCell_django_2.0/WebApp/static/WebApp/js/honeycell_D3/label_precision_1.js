
var margin = {top: 20, right: 20, bottom: 30, left: 80},
    width_precision = 700 - margin.left - margin.right,
    height_precision = 350 - margin.top - margin.bottom;

var formatPercent = d3.format(".0%");

var x_precision = d3.scale.ordinal()
    .rangeRoundBands([0, width_precision], .1, 1);

var y_precision = d3.scale.linear()
    .range([height_precision, 0]);

var xAxis_precision = d3.svg.axis()
    .scale(x_precision)
    .orient("bottom");

var yAxis_precision = d3.svg.axis()
    .scale(y_precision)
    .orient("left")
    .tickFormat(formatPercent);

var tip_precision = d3.tip()
      .attr('class', 'd3_tip_precision')
      .direction('n')
      .offset([-10, 2])
      .html(function(d) {
        return "<strong>Precision:</strong> <span style='color:red'>" + 
                d.Precision + "</span>";
    });

var svg_precision = d3.select("#label_precision")
	  .append("svg")
    .attr("width", width_precision + margin.left + margin.right)
    .attr("height", height_precision + margin.top + margin.bottom)
    .attr("id", "label_precision_D3")
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

svg_precision.call(tip_precision);






var task_id = document.getElementById("task_id").value;

d3.json("/get_json_result/" + task_id, function(error, json_data) {

  // console.log(json_data);
  json_data = JSON.parse(json_data);

  var label_num = json_data.LabelNum;
  var data = [];

  for (var i = 0; i < label_num; i++) {
      data[i] = {Labels: i, Precision: json_data.Labels[i].Precision};
    console.log(data[i]);
  }

  // console.log(data);

  data.forEach(function(d) {
    // console.log(d.Precision);
    d.Precision = +d.Precision;
  });

  x_precision.domain(data.map(function(d) { return d.Labels; }));
  y_precision.domain([0, d3.max(data, function(d) { return d.Precision; })]);

  svg_precision
      .append("g")
      .attr("class", "x axis_label_precision")
      .attr("transform", "translate(0," + height_precision + ")")
      .call(xAxis_precision);

  svg_precision
      .append("g")
      .attr("class", "y axis_label_precision")
      .call(yAxis_precision)
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Precision");

  svg_precision
      .selectAll(".precision_bar")
      .data(data)
      .enter()
      .append("rect")
      .attr("class", "precision_bar")
      .attr("x", function(d) { return x_precision(d.Labels); })
      .attr("width", x_precision.rangeBand())
      .attr("y", function(d) { return y_precision(d.Precision); })
      .attr("height", function(d) { return height_precision - y_precision(d.Precision); })
      .on('mouseover', tip_precision.show)
      .on('mouseout', tip_precision.hide)
      ;

  d3.select("#precison_sort").on("change", change);

  var sortTimeout = setTimeout(function() {
    d3.select("#precison_sort").property("checked", true).each(change);
  }, 2000);

  function change() {
    clearTimeout(sortTimeout);

    // Copy-on-write since tweens are evaluated after a delay.
    var x0_precision = x_precision.domain(data.sort(this.checked
        ? function(a, b) { return b.Precision - a.Precision; }
        : function(a, b) { return d3.ascending(a.Labels, b.Labels); })
        .map(function(d) { return d.Labels; }))
        .copy();

    svg_precision
        .selectAll(".precision_bar")
        .sort(function(a, b) { return x0_precision(a.Labels) - x0_precision(b.Labels); });

    var transition = svg_precision
        .transition().duration(750),
        delay = function(d, i) { return i * 50; };

    transition.selectAll(".precision_bar")
        .delay(delay)
        .attr("x", function(d) { return x0_precision(d.Labels); });

    transition.select(".x.axis_label_precision")
        .call(xAxis_precision)
      .selectAll("g")
        .delay(delay);
  }
});
