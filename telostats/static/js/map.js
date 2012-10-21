var m = mapbox.map('map');

function stationVoronoi() {
    var v = {}, stationData, stations, stationCoords, voronoi, city,
        stationAnimation;
    var svg = d3.select(document.body).append("svg").attr("id", "d3svg");

    var voronoiGroup = svg.append("g").attr("id", "voronoiGroup");
    var stationsGroup = svg.append("g").attr("id", "stationsGroup");

    var fadeInTime = 500;

    var color = function(station) {
        var bikes = station.poles - station.available;
        if (bikes === 0) {
            return 0;
        } else if (bikes <=5) {
            return 1;
        } else if (station.available <= 5) {
            return 3;
        } else if (station.available === 0) {
            return 4;
        } else {
            return 2;  // middle state is normal.
        }
    };

    var stationDotSize = d3.scale.quantize()
        .domain([minZoom, maxZoom])
        .range([2, 3, 4]);

    v.parent = svg.node();

    // Project a lat/lon location onto the displayed map (point)
    v.project = function(location) {
        var point = v.map.locationPoint({lat: location[1], lon: location[0]});
        return [point.x, point.y];
    };

    // redraw the layer
    // called every time something changes
    v.draw = function() {
        console.log("Draw called!");

        // position the overlay
        svg.attr("width", $("#map").width())
           .attr("height", $("#map").height());

        var delays = [];

        voronoi = voronoiGroup.selectAll("path")
            .data(stationData);

        // fade in when added
        voronoi.enter().append("path")
            .attr('id', function(d, i) { return 'station' + stationData[i].id; })
            .attr("class", function(d, i) {
                return "station_cell q" + color(stationData[i]) + "-5";
            })
            .attr("data-state", "fade-in")
          .transition().delay(function(d, i) {
                wait = stationAnimation(stationData[i].latitude);
                delays[i] = wait;
                return 600 + (fadeInTime-wait);
            }).duration(1000)
                .attr("data-state", "visible");

        // project the station cell polys onto the map
        voronoi
            .attr("d", function(d, i) {
                var poly = d3.geom.polygon(stationData[i].polygon);
                var projected = _.map(poly, v.project);
                return "M" + projected.join("L") + "Z";
            });


        // render the station dots
        // =============================================================
        stations = stationsGroup.selectAll("circle")
            .data(stationCoords);

        // Grow in when added
        stations.enter().append("circle")
            .attr("opacity", 0.0)
            .attr("r", 0)
          .transition().delay(150).duration(450)
            .attr("opacity", 0.15)
            .attr("r", 8 * stationDotSize(v.map.zoom()))
          .transition().delay(function(d, i) {
                return 600 + (fadeInTime - delays[i]);
            }).duration(200)
            .attr("r", stationDotSize(v.map.zoom()))
            .attr("opacity", 1);

        // Postion them
        stations
            // .attr("r", stationDotSize(v.map.zoom()))
            .attr("transform", function(d) { return "translate(" + v.project(d) + ")"; });
    };

    // supply the data
    // called once on load
    v.data = function(data) {
        console.log("data called!");
        stationData = data;
        stationCoords = _.map(stationData, function(s) {
            return [s.longitude, s.latitude];
        });

        stationAnimation = d3.scale.linear()
            .domain(d3.extent(stationCoords, function(coord) { return coord[1]; }))
            // .domain([0,1])
            .range([0, fadeInTime]);

        return v;
    };

    return v;
}


var telostats_tiles = {
    "tilejson": "2.0.0",
    "tiles": [TILESERVER_URL]
};
var minZoom = 13;
var maxZoom = 17;
m.addLayer(mapbox.layer().tilejson(telostats_tiles));
m.ui.zoomer.add();

var mapbounds = new MM.Extent(
    32.14920666588464,34.74252281494142,
    32.02678694143692,34.85478935546873);

m.setExtent(mapbounds);
m.setPanLimits(mapbounds);
m.setZoomRange(minZoom, maxZoom);

d3.json('/api/v1/station/', function(stations) {
    var stationMap = stationVoronoi().data(stations.objects);
    m.addLayer(stationMap);
    console.log("added d3 layer!");
    $('#map').on('click', function(event) {
        var p = m.pointLocation({x:event.pageX, y:event.pageY});
        console.log([p.lon, p.lat]);
    });
});