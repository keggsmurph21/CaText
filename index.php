<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Settlers of Catan</title>
    <meta charset="utf-8">
    <script src="core/includes/d3.v2.min.js"></script>
    <link href="style.css" rel="stylesheet" type="text/css" />
  </head>

  <body>

    <?php
    require_once('core/includes/funcs.php');
    init_settings('setup/standard/settings.ini'); // should eventually be able to change which style gets loaded

    var_dump(get_setting('board_shape'));

    $center = array( 'x'=>10, 'y'=>10 );
    $size = 5;
    var_dump(get_hex($center, $size));
    ?>

  	<div class="container">
      <svg id="boardContainer" width=600 height=600>
      </svg>
  	</div>

  </body>

  <script>
    /*
    // define new classes & methods
    function Hexagon (x,y) {
      this.center = [x,y];
      this.points = {p1 : [0,0], p2 : [0,0], p3 : [0,0], p4 : [0,0], p5 : [0,0], p6 : [0,0] };
    }

    Hexagon.prototype.init = function() {
      return true;
    };

    function Player () {
      this.points = 0
    }

    Player.prototype.init = function() {
      return true;
    }

    var aspectRatio = 0.707
      , width = parseInt(d3.select('.container').style('width'))
      , height = width * aspectRatio
      , nsweeps = 800
      , anchor_array = []
      , label_array = [];

    var svg = d3.select('.container').append('svg')
      .attr('width', width)
      .attr('height', height)
      .attr('xmlns', 'http://www.w3.org/2000/svg');

    svg.append('path').attr('x', 300).attr('y', 400);*/

    /*
    var width = 1440, // height = 960,
        height = 800; //height = 500
    */
    var margin = {top: 10, left: 10, bottom: 10, right: 10}
      , width = parseInt(d3.select('#map').style('width'))
      , width = width - margin.left - margin.right
      , mapRatio = .5
      , height = width * mapRatio
      , last_scale = (width/640)*100
      , offset = 8
      , radius = 8
      , nsweeps = 800
      , anchor_array= []
      , label_array = [];
    var  links, labels;

    var svg = d3.select("#map").append("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("xmlns", "http://www.w3.org/2000/svg")
        .attr("version", "1.1")
        .attr("viewBox", "0 0 "+width+" "+height)
        .call(d3.behavior.zoom()
            .translate(projection.translate())
            .scale(projection.scale())
            .on("zoom", redraw));

      var axes = svg.append("g").attr("id", "axes"),
        xAxis = axes.append("line").attr("y2", height),
    	yAxis = axes.append("line").attr("x2", width);

    svg.append("path")
        .datum(graticule.outline)
        .attr("class", "background")
        .attr("d", path);

    svg.selectAll(".graticule")
        .data(graticule.lines)
      .enter().append("path")
        .attr("class", "graticule")
        .attr("d", path);

    svg.append("path")
        .datum(graticule.outline)
        .attr("class", "foreground")
        .attr("d", path);

    /*
    //original boundaries
    d3.json("./index_map/readme-boundaries.json", function(collection) {
      svg.insert("path", ".graticule")
          .datum(collection)
          .attr("class", "boundary")
          .attr("d", path);
    });
    */

    //original land
    d3.json("./readme-land.json", function(collection) {
      svg.insert("path", ".graticule,.boundary")
          .datum(collection)
          .attr("class", "land")
          .attr("d", path);
      redraw();
    });



    d3.json("./td-locations-rev.json", function(collection) {
      var label;
      label_array.length = collection.features.length;
      anchor_array.length = collection.features.length;

      var location = svg.selectAll("svg")
        .data(collection.features, function(d) { return d.properties.label; })
      .enter().append("a")
        .attr("target", "_blank")
        .attr("xlink:href", function(d) { return d.properties.xlink; })
        .attr("class", function(d) { return "td-link "+d.properties.status; })
        .attr("id", function(d) { label = d.properties.label; return label; })
        .on("mouseover", function() { this.parentNode.appendChild(this); });
        ;
      anchors = location.append("circle")
        .attr("cx", function(d,i ) {
        	d.properties.index = i;
    		anchor_array[i] = ({x: projection(d.geometry.coordinates)[0], y: projection(d.geometry.coordinates)[1], r: 12});
        	return projection(d.geometry.coordinates)[0]; })
        .attr("cy", function(d) { return projection(d.geometry.coordinates)[1]; })
        .attr("data-latlon", function(d) { return "["+d.geometry.coordinates[1]+","+d.geometry.coordinates[0]+"]";})
        .attr("r", ".5em")
        .attr("class", function(d) { return "point "+d.properties.status; });
      labels = location.append("text", ".td-link")
        .attr("x", function(d,i) {
            label_array[i] = ( {x: projection(d.geometry.coordinates)[0], y: projection(d.geometry.coordinates)[1], width: 0, height: 0, name: d.properties.label, x_diff: 0, y_diff: 0});
        	return projection(d.geometry.coordinates)[0];
        })
        .attr("y", function(d) { return projection(d.geometry.coordinates)[1]; })
        .attr("data-latlon", function(d) { return "["+d.geometry.coordinates[1]+","+d.geometry.coordinates[0]+"]";})
        .attr("dx", ".25em")
        .attr("dy", ".35em")
        .attr("text-anchor","left")
        .attr("class", "label")
        .text( function(d) { return d.properties.label; });
      links = location.append("line")
    	.attr("class", "link")
    	.attr("x1", function(d) {
    		return projection(d.geometry.coordinates)[0];
    	})
    	.attr("y1", function(d) { return projection(d.geometry.coordinates)[1]; })
    	.attr("x2", function(d) { return projection(d.geometry.coordinates)[0]; })
    	.attr("y2", function(d) { return projection(d.geometry.coordinates)[1]; })


    	redraw();


        var index = 0;
    	labels.each(function() {
    		label_array[index].width = this.getBBox().width;
    		label_array[index].height = this.getBBox().height;
    		index += 1;
    	});

      datelabel.text( function(d){ return currentdate;})

      annealLabels(nsweeps);
      calcLabelsDiff();
      redrawLabels();

    });

    /*
    //functional insertion of single feature
    d3.json("./index_map/td-locations-rev.json", function(collection) {
    //  var coordinates = options[i].projection([93.489484,51.549743]);
      svg.insert("circle", ".point")
        .data(collection.features)
        .attr("cx", function(d) { return options[i].projection(d.geometry.coordinates)[0]; })
        .attr("cy", function(d) { return options[i].projection(d.geometry.coordinates)[1]; })
        .attr("r", "1.5em")
        .attr("class", "point");
      svg.insert("text", ".label")
        .data(collection.features)
        .attr("x", function(d) { return options[i].projection(d.geometry.coordinates)[0]; })
        .attr("y", function(d) { return options[i].projection(d.geometry.coordinates)[1]; })
        .attr("dx", ".25em")
        .attr("dy", ".35em")
        .attr("text-anchor","middle")
        .attr("class", "label")
        .text( function(d) { return d.properties.label; });
    });
    */


    var menu = d3.select("#projection-menu")
        .on("change", change);

    menu.selectAll("option")
        .data(options)
      .enter().append("option")
        .text(function(d) { return d.name; });


    var playHandler = d3.select("#play")
        .on("click", startTimer);
    var pauseHandler = d3.select("#pause")
        .on("click", pause );


    function loop() {
      var j = Math.floor(Math.random() * n);
      menu.property("selectedIndex", i = j + (j >= i));
      update(options[i]);
    }

    function change() {
    //  clearInterval(interval);
      i = this.selectedIndex;
      update(options[this.selectedIndex]);
    }

    function startTimer (){
      if (interval != 0) {
      	clearInterval(interval);
      }
      interval = setInterval(playLoop, 2000); //150000
      currentdate = startdate;
      redraw();

    }

    function playLoop() {
      if(currentdate>maxdate){
        currentdate = startdate;
      } else if (currentdate == maxdate) {
        pause();
      } else {
        currentdate ++;
      }
      redraw();
    }

    function pause() {
      clearInterval(interval);
    }

    function update(option) {
      svg.selectAll("path").transition()
          .duration(750)
          .attr("d", path.projection(option.projection));
      projection = option.projection;
      svg.selectAll("circle").transition()
         .duration(0)
    	.attr("cx", function (d) {
    		anchor_array[d.properties.index].x = projection(d.geometry.coordinates)[0];
    	    anchor_array[d.properties.index].y = projection(d.geometry.coordinates)[1];
    	    return projection(d.geometry.coordinates)[0];})
    	.attr("cy", function (d) { return projection(d.geometry.coordinates)[1];});
      svg.selectAll("text").transition()
         .duration(0)
    	.attr("x", function (d) {
    	    label_array[d.properties.index].x = projection(d.geometry.coordinates)[0];
    	    label_array[d.properties.index].y = projection(d.geometry.coordinates)[1];
    		return projection(d.geometry.coordinates)[0];})
    	.attr("y", function (d) { return projection(d.geometry.coordinates)[1];})
    	;
      svg.selectAll(".link").transition()
         .duration(0)
    	.attr("x1", function (d) { return projection(d.geometry.coordinates)[0];})
    	.attr("y1", function (d) { return projection(d.geometry.coordinates)[1];})
    	.attr("x2", function (d) { return projection(d.geometry.coordinates)[0];})
    	.attr("y2", function (d) { return projection(d.geometry.coordinates)[1];})
    	;

      annealLabels(nsweeps);
      calcLabelsDiff();
      redrawLabels();
    }

    function updateZoom(option) {
      svg.selectAll("path").transition()
          .duration(300)
          .attr("d", path.projection(option.projection));
      projection = option.projection;
      svg.selectAll("circle").transition()
         .duration(300)
    	.attr("cx", function (d) {
    	    return projection(d.geometry.coordinates)[0];})
    	.attr("cy", function (d) { return projection(d.geometry.coordinates)[1];});
      svg.selectAll("text").transition()
         .duration(300)
    	.attr("x", function (d) {
    		return projection(d.geometry.coordinates)[0] + label_array[d.properties.index].x_diff;})
    	.attr("y", function (d) { return projection(d.geometry.coordinates)[1] + label_array[d.properties.index].y_diff;})
    	;
      svg.selectAll(".link").transition()
         .duration(300)
    	.attr("x1", function (d) { return projection(d.geometry.coordinates)[0];})
    	.attr("y1", function (d) { return projection(d.geometry.coordinates)[1];})
    	.attr("x2", function (d) { return projection(d.geometry.coordinates)[0] + label_array[d.properties.index].x_diff;})
    	.attr("y2", function (d) { return projection(d.geometry.coordinates)[1] + label_array[d.properties.index].y_diff;})
    	;
    }

    function key(d) {
      return d.properties.label;
    }

    function annealLabels(nsweeps) {
      var sim_ann = d3.labeler()
    	.label(label_array)
    	.anchor(anchor_array)
    	.width(width)
    	.height(height)
      sim_ann.start(nsweeps);

      return sim_ann;
    }

    function calcLabelsDiff () {
    	for (var j in label_array) {
    		label_array[j].x_diff =  label_array[j].x - anchor_array[j].x;
    		label_array[j].y_diff = label_array[j].y - anchor_array[j].y ;
    	  }
    }

    function redrawLabels() {
    	// Redraw labels and leader lines
    	labels
    	.transition()
    	.duration(0)
    	.attr("x", function(d) { return (label_array[d.properties.index].x); })
    	.attr("y", function(d) { return (label_array[d.properties.index].y); });

    	links
    	.transition()
    	.duration(0)
    	.attr("x2",function(d) { return (label_array[d.properties.index].x); })
    	.attr("y2",function(d) { return (label_array[d.properties.index].y); });
    }



    function redraw() {
      if (d3.event) {
        projection
          .translate(d3.event.translate)
          .scale(d3.event.scale);
        }
      datelabel.text( function (d){ return currentdate;})
      var totalcount = 0;


      svg.selectAll("a")
       .attr("visibility", function (d) {
          if(d.properties.date > currentdate){ return "hidden";
          } else { totalcount ++; return "visible"; }
        })

      svg.selectAll("path").attr("d", path);
      svg.selectAll("circle").transition().duration(100)
    	.attr("cx", function (d) {
    	    return projection(d.geometry.coordinates)[0];})
    	.attr("cy", function (d) { return projection(d.geometry.coordinates)[1];});
      svg.selectAll("text").transition().duration(100)
    	.attr("x", function (d) {
    	    return projection(d.geometry.coordinates)[0] + label_array[d.properties.index].x_diff;})
    	.attr("y", function (d) { return projection(d.geometry.coordinates)[1] + label_array[d.properties.index].y_diff;});
      svg.selectAll(".link").transition().duration(100)
    	.attr("x1", function (d) { return projection(d.geometry.coordinates)[0];})
    	.attr("y1", function (d) { return projection(d.geometry.coordinates)[1];})
    	.attr("x2", function (d) { return projection(d.geometry.coordinates)[0] + label_array[d.properties.index].x_diff ;})
    	.attr("y2", function (d) { return projection(d.geometry.coordinates)[1] + label_array[d.properties.index].y_diff ;});
      var t = projection.translate();
        xAxis.attr("x1", t[0]).attr("x2", t[0]);
        yAxis.attr("y1", t[1]).attr("y2", t[1]);

      totallabel.text( function() { return totalcount +' active talking dictionaries';});


      if ((projection.scale() > last_scale*3) || (projection.scale() < last_scale/3) ) {
    	last_scale = projection.scale();
    	labels.each(function(d) {
    		anchor_array[d.properties.index].x = projection(d.geometry.coordinates)[0];
    		anchor_array[d.properties.index].y = projection(d.geometry.coordinates)[1];
    		label_array[d.properties.index].x = projection(d.geometry.coordinates)[0];
    		label_array[d.properties.index].y = projection(d.geometry.coordinates)[1];
    	});

    	annealLabels(nsweeps);
    	calcLabelsDiff();
    	redrawLabels();
    	redraw();
      }

    }


    var zoomOutHandler = d3.select("#zoom-out")
            .on("click", reset);
    var zoomInHandler = d3.select("#zoom-in")
            .on("click", zoomIn);

    function zoomIn () {
      var curr_scale = projection.scale();
      options[i].projection.scale(curr_scale*1.5);
      projection.scale(curr_scale*1.5);
      return updateZoom(options[i]);
    }

    function reset () {
      options[i].projection.translate([width/2, height/2]).scale((width/640)*100);
      return updateZoom(options[i]);
    }

  </script>
</html>
