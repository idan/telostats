// Generated by CoffeeScript 1.4.0
(function() {
  var MARKER_BUCKET_COLORS, TELOSTATS_TILEJSON, bucket_colors, initMap, initStationPie, initStations, pushStateNav, renderAverageTimeline, renderHistoryTimeline, renderStationMap, renderStationScale, renderTimeline, stationClassifier, stationsLayer;

  TELOSTATS_TILEJSON = {
    'tilejson': '2.0.0',
    'scheme': 'xyz',
    'name': 'Tel Aviv Light',
    'description': 'A light tileset focusing on the municipality of Tel Aviv, suitable for visualizations.',
    'attribution': 'OSM contributors',
    'bounds': [34.742, 32.026, 34.924, 32.149],
    'minzoom': 13,
    'maxzoom': 17,
    'tiles': [TILESERVER_URL],
    'grids': []
  };

  MARKER_BUCKET_COLORS = {
    0: '#dd2ea3',
    1: '#ffafe5',
    2: '#ccc',
    3: '#94e1ff',
    4: '#18b4f1'
  };

  bucket_colors = d3.scale.ordinal().range(['#dd2ea3', '#ffafe5', '#fff', '#94e1ff', '#18b4f1']);

  stationClassifier = function(poles, available) {
    var bikes;
    bikes = poles - available;
    if (bikes === 0) {
      return 0;
    } else if (bikes <= 5) {
      return 1;
    } else if (available <= 5) {
      return 3;
    } else if (available === 0) {
      return 4;
    } else {
      return 2;
    }
  };

  renderStationMap = function(elem) {
    var baseLayer, bucket, coords, id, markerLayer, stationmap;
    id = $(elem).attr('data-id');
    coords = {
      lat: Number($(elem).attr('data-lat')),
      lon: Number($(elem).attr('data-lon'))
    };
    bucket = stationClassifier($(elem).attr('data-poles'), $(elem).attr('data-available'));
    baseLayer = mapbox.layer().tilejson(TELOSTATS_TILEJSON);
    markerLayer = mapbox.markers.layer();
    markerLayer.add_feature({
      geometry: {
        type: "Point",
        coordinates: [coords.lon, coords.lat]
      }
    }).factory(function(f) {
      var marker;
      marker = ich.stationmarker_svg_template({
        bucket: bucket
      });
      return marker[0];
    });
    stationmap = mapbox.map(elem, [], null, []);
    stationmap.addLayer(baseLayer);
    stationmap.addLayer(markerLayer);
    return stationmap.centerzoom(coords, 17, false);
  };

  renderStationScale = function(elem) {
    var available, bikes, bucket, direction, id, marker, percent, poles, section;
    id = $(elem).attr('data-id');
    poles = Number($(elem).attr('data-poles'));
    available = Number($(elem).attr('data-available'));
    bikes = poles - available;
    bucket = stationClassifier(poles, available);
    switch (bucket) {
      case 0:
        section = 'empty';
        direction = 'left';
        percent = -0.07;
        break;
      case 1:
        section = 'empty';
        direction = 'left';
        percent = bikes / 5;
        break;
      case 2:
        section = 'ok';
        direction = 'left';
        percent = (bikes - 5) / (available + bikes - 10);
        break;
      case 3:
        section = 'full';
        direction = 'right';
        percent = available / 5;
        break;
      case 4:
        section = 'full';
        direction = 'right';
        percent = -0.07;
    }
    marker = ich.stationscale_marker_template({
      'direction': direction,
      'percent': percent * 100,
      'bikes': bikes,
      'poles': available
    });
    return $("[data-id=" + id + "] .station-slider-bar>." + section).append(marker);
  };

  renderTimeline = function(data, elem) {
    var colors, elemHeight, elemWidth, height, iso, margin, svg, timeExtent, width, x, xAxis, xWidth, xaxisSVG;
    margin = {
      top: 0,
      right: 7,
      bottom: 25,
      left: 7
    };
    elemWidth = $(elem).width();
    elemHeight = $(elem).height();
    width = elemWidth - margin.right - margin.left;
    height = elemHeight - margin.top - margin.bottom;
    console.log("width: " + width + ", height: " + height);
    console.log("elemWidth: " + elemWidth + ", elemHeight: " + elemHeight);
    console.log("data.length: " + data.length);
    svg = d3.select(elem).append('svg').attr('class', 'timeline').attr('width', elemWidth).attr('height', elemHeight).append('g').attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    iso = d3.time.format.iso;
    timeExtent = d3.extent(data, function(d) {
      return iso.parse(d.timestamp);
    });
    timeExtent[1] = d3.time.hour.offset(timeExtent[1], 1);
    console.log(timeExtent);
    x = d3.time.scale().rangeRound([0, width]).domain(timeExtent);
    xWidth = d3.scale.linear().domain([0, data.length]).range([0, width]);
    xAxis = d3.svg.axis().scale(x).orient('bottom').ticks(d3.time.hours, 3).tickSubdivide(2).tickSize(5, 3).tickFormat(d3.time.format('%H'));
    colors = svg.append('g');
    colors.selectAll('.timespan').data(data).enter().append('rect').attr('class', function(d, i) {
      var bucket;
      bucket = stationClassifier(d.poles, d.available);
      return "timespan bucket-" + bucket;
    }).attr('height', 15).attr('width', function(d, i) {
      var end, start;
      start = iso.parse(d.timestamp);
      end = d3.time.hour.offset(start, 1);
      return width = x(end) - x(start);
    }).attr('transform', function(d) {
      var offset;
      offset = x(iso.parse(d.timestamp));
      return "translate(" + offset + ", 0)";
    });
    xaxisSVG = svg.append("g").attr("class", "x axis").attr("transform", "translate(0," + height + ")").call(xAxis);
    return xaxisSVG.selectAll("text").each(function(d) {
      return d3.select(this).attr("class", "axislabel");
    });
  };

  renderHistoryTimeline = function(elem) {
    var id;
    id = $(elem).attr('data-id');
    return d3.json("/api/v1/recent/" + id, function(recent) {
      return renderTimeline(recent.series, elem);
    });
  };

  renderAverageTimeline = function(elem) {
    var id;
    id = $(elem).attr('data-id');
    return d3.json("/api/v1/average/" + id, function(recent) {
      return renderTimeline(recent.series, elem);
    });
  };

  stationsLayer = function(opts) {
    var animationDelayTime, draw, drawStations, fadeInTime, layer, map, project, registerMapMouseDragHandlers, s, stationAnimation, stationAnimationWait, stationCoords, stationData, stationDotSize, stations, svg;
    map = opts.map;
    stationData = opts.stations;
    stationCoords = (function() {
      var _i, _len, _results;
      _results = [];
      for (_i = 0, _len = stationData.length; _i < _len; _i++) {
        s = stationData[_i];
        _results.push([s.longitude, s.latitude]);
      }
      return _results;
    })();
    svg = d3.select(document.body).append('svg').attr('id', 'd3svg');
    stations = svg.append('g').attr('id', 'stations');
    fadeInTime = 500;
    animationDelayTime = 600;
    stationDotSize = d3.scale.quantize().domain([opts.minZoom, opts.maxZoom]).range([2, 3, 4]);
    stationAnimation = d3.scale.linear().domain(d3.extent(stationCoords, function(coord) {
      return coord[1];
    })).range([0, fadeInTime]);
    project = function(location) {
      var point;
      point = map.locationPoint({
        lat: location[1],
        lon: location[0]
      });
      return [point.x, point.y];
    };
    stationAnimationWait = function(index) {
      return stationAnimation(stationData[index].latitude);
    };
    registerMapMouseDragHandlers = function(elem) {
      var clientX, clientY, d3elem, stationid;
      d3elem = d3.select(elem);
      stationid = d3elem.attr('data-id');
      d3elem.classed('loading', false);
      clientX = null;
      clientY = null;
      d3elem.on('mousedown', function(d, i) {
        clientX = d3.event.clientX;
        return clientY = d3.event.clientY;
      });
      return d3elem.on('mouseup', function(d, i) {
        var newflyout, stationary;
        stationary = clientX === d3.event.clientX && clientY === d3.event.clientY;
        if (d3elem.classed('selected')) {
          return;
        }
        if (stationary) {
          d3.selectAll('.station').classed('selected', false);
          newflyout = ich.stationflyout_template({
            stationid: stationid
          });
          $('#stationflyouts').append(newflyout);
          opts = {
            url: '/station/' + stationid,
            container: ".stationflyout[data-id=" + stationid + "]",
            timeout: 2000
          };
          d3elem.classed('selected', true);
          $.pjax(opts);
          return $(newflyout).on('pjax:end', function() {
            var averageelem, historyelem, mapelem;
            mapelem = $(".station-map[data-id='" + stationid + "']")[0];
            historyelem = $(".history-timeline[data-id='" + stationid + "']")[0];
            averageelem = $(".average-timeline[data-id='" + stationid + "']")[0];
            renderStationMap(mapelem);
            renderStationScale(mapelem);
            renderHistoryTimeline(historyelem);
            renderAverageTimeline(averageelem);
            $(this).removeClass('hidden');
            return setTimeout(function() {
              $('.flyout.secondary:not(.stationflyout)').addClass('hidden');
              return $(".stationflyout[data-id!=" + stationid + "]").remove();
            }, 200);
          });
        }
      });
    };
    drawStations = function() {
      var cellGroups, cellsEnter, dots, dotsEnter, groupsEnter, stationDelay;
      stationDelay = function(d, i) {
        return animationDelayTime + fadeInTime - stationAnimationWait(i);
      };
      cellGroups = stations.selectAll('g').data(stationData);
      groupsEnter = cellGroups.enter().append('g');
      cellsEnter = groupsEnter.append('path');
      dotsEnter = groupsEnter.append('circle');
      dots = stations.selectAll('g>circle').data(stationData);
      dots.attr('r', stationDotSize(map.zoom())).attr('transform', function(d) {
        return 'translate(' + project([d.longitude, d.latitude]) + ')';
      });
      groupsEnter.classed('station', true).classed('loading', true).attr('data-id', function(d, i) {
        return stationData[i].id;
      }).attr('data-lat', function(d, i) {
        return stationData[i].latitude;
      }).attr('data-lon', function(d, i) {
        return stationData[i].longitude;
      }).attr('data-bucket', function(d, i) {
        return stationClassifier(stationData[i].poles, stationData[i].available);
      }).attr('data-poles', function(d, i) {
        return stationData[i].poles;
      }).attr('data-available', function(d, i) {
        return stationData[i].available;
      }).transition().delay(stationDelay).duration(200).each('end', function() {
        return registerMapMouseDragHandlers(this);
      });
      cellsEnter.classed('station_cell', true);
      dotsEnter.classed("station_dot", true).attr('opacity', 0.0).attr('r', 0).attr('transform', function(d) {
        return 'translate(' + project([d.longitude, d.latitude]) + ')';
      }).transition().delay(150).duration(450).attr('opacity', 0.15).attr('r', 8 * stationDotSize(map.zoom())).transition().delay(stationDelay).duration(200).attr('r', stationDotSize(map.zoom())).attr('opacity', 1);
      return stations.selectAll('g>path').data(stationData).attr('d', function(d, i) {
        var p, poly, projected;
        poly = d3.geom.polygon(stationData[i].polygon);
        projected = (function() {
          var _i, _len, _results;
          _results = [];
          for (_i = 0, _len = poly.length; _i < _len; _i++) {
            p = poly[_i];
            _results.push(project(p));
          }
          return _results;
        })();
        return 'M' + projected.join('L') + 'Z';
      });
    };
    draw = function() {
      svg.attr('width', $('#map').width()).attr('height', $('#map').height());
      return drawStations();
    };
    layer = {
      'project': project,
      'draw': draw,
      'parent': svg.node()
    };
    return layer;
  };

  initMap = function() {
    var m, mapbounds, maxZoom, minZoom;
    m = mapbox.map('map');
    minZoom = TELOSTATS_TILEJSON.minzoom;
    maxZoom = TELOSTATS_TILEJSON.maxzoom;
    m.addLayer(mapbox.layer().tilejson(TELOSTATS_TILEJSON));
    m.ui.zoomer.add();
    mapbounds = new MM.Extent(32.149, 34.742, 32.026, 34.924);
    m.setExtent(mapbounds);
    m.setPanLimits(mapbounds);
    m.setZoomRange(minZoom, maxZoom);
    return m;
  };

  initStations = function(map, selectedid) {
    return d3.json('/api/v1/station/', function(stations) {
      var elem, opts, sl;
      opts = {
        'map': map,
        'stations': stations.objects,
        'minZoom': TELOSTATS_TILEJSON.minzoom,
        'maxZoom': TELOSTATS_TILEJSON.maxzoom
      };
      sl = stationsLayer(opts);
      map.addLayer(sl);
      map.refresh();
      if (selectedid) {
        elem = d3.select(".station[data-id=\"" + selectedid + "\"]");
        elem.classed('selected', true);
      }
      return initStationPie(stations.objects);
    });
  };

  initStationPie = function(stations) {
    var arc, buckets, counts, data, g, k, pctformat, pie, pie_h, pie_radius, pie_w, piesvg, v;
    buckets = _.map(stations, function(s) {
      return stationClassifier(s.poles, s.available);
    });
    counts = _.countBy(buckets, function(b) {
      return b;
    });
    pctformat = d3.format('.1p');
    data = (function() {
      var _results;
      _results = [];
      for (k in counts) {
        v = counts[k];
        _results.push({
          bucket: Number(k),
          value: Number(v),
          percentage: pctformat(Number(v) / stations.length)
        });
      }
      return _results;
    })();
    data = _.sortBy(data, function(x) {
      return x.bucket;
    });
    pie_w = $('#stations-overview-pie').width();
    pie_h = $('#stations-overview-pie').height();
    pie_radius = Math.min(pie_w, pie_h) / 2;
    arc = d3.svg.arc().outerRadius(pie_radius - 10).innerRadius(pie_radius - 70);
    pie = d3.layout.pie().sort(null).value(function(d) {
      return d.value;
    });
    piesvg = d3.select('#stations-overview-pie').append('svg').attr('width', pie_w).attr('height', pie_h).append('g').attr("transform", "translate(" + (pie_w / 2) + "," + (pie_h / 2) + ")");
    g = piesvg.selectAll(".arc").data(pie(data)).enter().append("g").attr("class", "arc");
    g.append("path").attr("d", arc).style("fill", function(d, i) {
      return bucket_colors(d.data.bucket);
    });
    return g.append("text").attr("transform", function(d) {
      return "translate(" + (arc.centroid(d)) + ")";
    }).attr("dy", ".35em").style("text-anchor", "middle").text(function(d, i) {
      return d.data.percentage;
    });
  };

  pushStateNav = function(url) {
    window.history.pushState(null, '', url);
    if (typeof _gaq !== "undefined" && _gaq !== null) {
      return _gaq.push(['_trackPageview', url]);
    }
  };

  $(function() {
    var map, selectedid, stationelem;
    map = initMap();
    selectedid = $('.stationflyout').attr('data-id');
    initStations(map, selectedid);
    if (selectedid) {
      stationelem = $(".station[data-id=" + selectedid + "]")[0];
      if (stationelem) {
        d3.select(stationelem).classed('selected', true);
      }
    }
    _.each($('.station-map'), renderStationMap);
    _.each($('.station-map'), renderStationScale);
    _.each($('.history-timeline'), renderHistoryTimeline);
    _.each($('.average-timeline'), renderAverageTimeline);
    $(document).pjax('a[data-pjax]');
    $('.close-flyout').live('click', function(e) {
      $(this).parent().addClass('hidden');
      d3.select('.selected').classed('selected', false);
      pushStateNav($(this).attr('href'));
      return false;
    });
    $('a.static-flyout').click(function() {
      var target;
      target = $(this).attr('data-flyout');
      $(target).removeClass('hidden');
      pushStateNav($(this).attr('href'));
      return false;
    });
    return $(document).keyup(function(e) {
      if (e.keyCode === 27) {
        return $('.close-flyout').click();
      }
    });
  });

}).call(this);
