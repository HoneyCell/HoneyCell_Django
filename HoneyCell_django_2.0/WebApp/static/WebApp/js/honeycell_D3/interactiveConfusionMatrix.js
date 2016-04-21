/**
 * Created by jianheluo on 4/18/16.
 */



var margin = {top: 20, right: 20, bottom: 30, left: 80},
    width = 700 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

var formatPercent = d3.format(".0%");

var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .1, 1);

var y = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .tickFormat(formatPercent);

var svg = d3.select("#confusion_matrix")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + 60 + "," + -60 + ")");


var task_id = document.getElementById("task_id").value;


d3.json("/get_json_result/" + task_id, function(error, json_data){

    //console.log(json_data);
    json_data = JSON.parse(json_data);

    var data = [];

    for (var i = 0; i < json_data.LabelNum; i++) {
        data[i] = {ConfusionMatrix: json_data.ConfusionMatrix[i]};
        console.log(data[i]);
    }



    var freqData = [
        {State: 'Label1', freq: {Label1: data[0].ConfusionMatrix[0], Label2: data[1].ConfusionMatrix[0], Label3: data[2].ConfusionMatrix[0]}}
        , {State: 'Label2', freq: {Label1: data[0].ConfusionMatrix[1], Label2: data[1].ConfusionMatrix[1], Label3: data[2].ConfusionMatrix[1]}}
        , {State: 'Label3', freq: {Label1: data[0].ConfusionMatrix[2], Label2: data[1].ConfusionMatrix[2], Label3: data[2].ConfusionMatrix[2]}}
    ];


    // call the dashboard function
    dashboard('#confusion_matrix', freqData);


    function dashboard(id, fData) {

        console.log("Hello world.")

        var barColor = 'steelblue';

        function segColor(c) {
            return {Label1: "#807dba", Label2: "#e08214", Label3: "#41ab5d"}[c];
        }

        // compute total for each state.
        fData.forEach(function (d) {
            d.total = d.freq.Label1 + d.freq.Label2 + d.freq.Label3;
        });

        // function to handle histogram.
        function histoGram(fD) {
            var hG = {}, hGDim = {t: 20, r: 0, b: 30, l: 40};
            hGDim.w = 300 - hGDim.l - hGDim.r,
            hGDim.h = 300 - hGDim.t - hGDim.b;

            //create svg for histogram.
            var hGsvg = svg
                // d3.select(id)
                .append("svg")
                .attr("width", hGDim.w + hGDim.l + hGDim.r)
                .attr("height",400)
                .append("g")
                .attr("transform", "translate(" + 0 + "," + 83 + ")");

            // create function for x-axis mapping.
            var x = d3.scale.ordinal().rangeRoundBands([0, hGDim.w], 0.1)
                .domain(fD.map(function (d) {
                    return d[0];
                }));

            // Add x-axis to the histogram svg.
            hGsvg.append("g").attr("class", "x axis")
                .attr("transform", "translate(0," + hGDim.h + ")")
                .call(d3.svg.axis().scale(x).orient("bottom"));

            // Create function for y-axis map.
            var y = d3.scale.linear().range([hGDim.h, 0])
                .domain([0, d3.max(fD, function (d) {
                    return d[1];
                })]);

            // Create bars for histogram to contain rectangles and freq labels.
            var bars = hGsvg.selectAll(".bar").data(fD).enter()
                .append("g").attr("class", "bar");

            //create the rectangles.
            bars.append("rect")
                .attr("x", function (d) {
                    return x(d[0]);
                })
                .attr("y", function (d) {
                    return y(d[1]);
                })
                .attr("width", x.rangeBand())
                .attr("height", function (d) {
                    return hGDim.h - y(d[1]);
                })
                .attr('fill', barColor)
                .on("mouseover", mouseover)// mouseover is defined below.
                .on("mouseout", mouseout);// mouseout is defined below.

            //Create the frequency labels above the rectangles.
            bars.append("text").text(function (d) {
                    return d3.format(",")(d[1])
                })
                .attr("x", function (d) {
                    return x(d[0]) + x.rangeBand() / 2;
                })
                .attr("y", function (d) {
                    return y(d[1]) - 5;
                })
                .attr("text-anchor", "middle");

            function mouseover(d) {  // utility function to be called on mouseover.
                // filter for selected state.
                var st = fData.filter(function (s) {
                        return s.State == d[0];
                    })[0],
                    nD = d3.keys(st.freq).map(function (s) {
                        return {type: s, freq: st.freq[s]};
                    });

                // call update functions of pie-chart and legend.
                pC.update(nD);
                leg.update(nD);
            }

            function mouseout(d) {    // utility function to be called on mouseout.
                // reset the pie-chart and legend.
                pC.update(tF);
                leg.update(tF);
            }

            // create function to update the bars. This will be used by pie-chart.
            hG.update = function (nD, color) {
                // update the domain of the y-axis map to reflect change in frequencies.
                y.domain([0, d3.max(nD, function (d) {
                    return d[1];
                })]);

                // Attach the new data to the bars.
                var bars = hGsvg.selectAll(".bar").data(nD);

                // transition the height and color of rectangles.
                bars.select("rect").transition().duration(500)
                    .attr("y", function (d) {
                        return y(d[1]);
                    })
                    .attr("height", function (d) {
                        return hGDim.h - y(d[1]);
                    })
                    .attr("fill", color);

                // transition the frequency labels location and change value.
                bars.select("text").transition().duration(500)
                    .text(function (d) {
                        return d3.format(",")(d[1])
                    })
                    .attr("y", function (d) {
                        return y(d[1]) - 5;
                    });
            }
            return hG;
        }

        // function to handle pieChart.
        function pieChart(pD) {
            var pC = {}, pieDim = {w: 250, h: 250};
            pieDim.r = Math.min(pieDim.w, pieDim.h) / 2;

            // create svg for pie chart.
            var piesvg = svg
                // d3.select(id).append("svg")
                // .attr("width", pieDim.w).attr("height", pieDim.h)
                // .attr("transform", "translate(" + 100 + "px ," + -300 + "px)")
                .append("g")
                // .attr("transform", "translate(" + pieDim.w / 2 + "," + pieDim.h / 2 + ")");
                .attr("transform", "translate(" + 450 + " ," + 200 + ")")

            // create function to draw the arcs of the pie slices.
            var arc = d3.svg.arc().outerRadius(pieDim.r - 10).innerRadius(0);

            // create a function to compute the pie slice angles.
            var pie = d3.layout.pie().sort(null).value(function (d) {
                return d.freq;
            });

            // Draw the pie slices.
            piesvg.selectAll("path").data(pie(pD)).enter().append("path").attr("d", arc)
                .each(function (d) {
                    this._current = d;
                })
                .style("fill", function (d) {
                    return segColor(d.data.type);
                })
                .on("mouseover", mouseover).on("mouseout", mouseout);

            // create function to update pie-chart. This will be used by histogram.
            pC.update = function (nD) {
                piesvg.selectAll("path").data(pie(nD)).transition().duration(500)
                    .attrTween("d", arcTween);
            }
            // Utility function to be called on mouseover a pie slice.
            function mouseover(d) {
                // call the update function of histogram with new data.
                hG.update(fData.map(function (v) {
                    return [v.State, v.freq[d.data.type]];
                }), segColor(d.data.type));
            }

            //Utility function to be called on mouseout a pie slice.
            function mouseout(d) {
                // call the update function of histogram with all data.
                hG.update(fData.map(function (v) {
                    return [v.State, v.total];
                }), barColor);
            }

            // Animating the pie-slice requiring a custom function which specifies
            // how the intermediate paths should be drawn.
            function arcTween(a) {
                var i = d3.interpolate(this._current, a);
                this._current = i(0);
                return function (t) {
                    return arc(i(t));
                };
            }

            return pC;
        }

        // function to handle legend.
        function legend(lD) {
            var leg = {};

            // create table for legend.
            var legend = d3.select("#dashboard")
                        .append("table")
                        .attr('class', 'legend')
                        // .append("g")
                        // .attr("transform", "translate(" + 700 + " ," + 150 + ")")
                        ;

            // create one row per segment.
            var tr = legend.append("tbody").selectAll("tr").data(lD).enter().append("tr");

            // create the first column for each segment.
            tr.append("td")
                .append("svg")
                .attr("width", '16').attr("height", '16')
                .append("rect")
                .attr("width", '16').attr("height", '16')
                .attr("fill", function (d) {
                    return segColor(d.type);
                });

            // create the second column for each segment.
            tr.append("td").text(function (d) {
                return d.type;
            });

            // create the third column for each segment.
            tr.append("td").attr("class", 'legendFreq')
                .text(function (d) {
                    return d3.format(",")(d.freq);
                });

            // create the fourth column for each segment.
            tr.append("td").attr("class", 'legendPerc')
                .text(function (d) {
                    return getLegend(d, lD);
                });

            // Utility function to be used to update the legend.
            leg.update = function (nD) {
                // update the data attached to the row elements.
                var l = legend.select("tbody").selectAll("tr").data(nD);

                // update the frequencies.
                l.select(".legendFreq").text(function (d) {
                    return d3.format(",")(d.freq);
                });

                // update the percentage column.
                l.select(".legendPerc").text(function (d) {
                    return getLegend(d, nD);
                });
            }

            function getLegend(d, aD) { // Utility function to compute percentage.
                return d3.format("%")(d.freq / d3.sum(aD.map(function (v) {
                        return v.freq;
                    })));
            }

            return leg;
        }

        // calculate total frequency by segment for all state.
        var tF = ['Label1', 'Label2', 'Label3'].map(function (d) {
            return {
                type: d, freq: d3.sum(fData.map(function (t) {
                    return t.freq[d];
                }))
            };
        });

        // calculate total frequency by state for all segment.
        var sF = fData.map(function (d) {
            return [d.State, d.total];
        });

        var hG = histoGram(sF), // create the histogram.
            pC = pieChart(tF), // create the pie-chart.
            leg = legend(tF);  // create the legend.

    }

});

