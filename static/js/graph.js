var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var parseDate = d3.time.format("%d/%m/%Y %H:%M").parse;

var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .1);

var y = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function(d) {
        var str = 'Data: <span style="color:orange">' + d.date.toLocaleString() + '</span><br>';
        str = str + 'Valor: <span style="color:orange">R$ ' + d.value + '</span>';
        return str;
    });

var svg = d3.select("#graph").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .attr('viewBox', '0 0 ' + (width+180) + ' ' + (height+20))
    .attr('preserveAspectRatio','xMinYMin meet')
    .append("g")
    .attr("transform", "translate(70, 0)");

svg.call(tip);

var url = $('#graph').data('url');
d3.json(url, function(error, data) {
    if (error) throw error;
    var custom_data = [];
    for(var i in data) {
        custom_data.push({
            'date': parseDate(data[i].timestamp),
            'value': data[i].last
        });
    }
    x.domain(custom_data.map(function(d) {
        return d.date.toLocaleString();
    }));
    y.domain([0, d3.max(custom_data, function(d) {
        return d.value;
    })]);

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
        .selectAll('text')
        .style('text-anchor', 'end')
        .attr('transform', 'rotate(-45)');

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Price ($)");

    svg.selectAll(".bar")
        .data(custom_data)
    .enter().append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return x(d.date.toLocaleString()); })
        .attr("width", x.rangeBand())
        .attr("y", function(d) { return y(d.value); })
        .attr("height", function(d) { return height - y(d.value); })
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide);

});
