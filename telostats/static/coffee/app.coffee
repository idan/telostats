
# TileJSON
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
    'grids': [],
}

MARKER_BUCKET_COLORS = {
    0: '#dd2ea3',
    1: '#ffafe5',
    2: '#ccc', # it's a lie, but station markers need to be darker
    3: '#94e1ff',
    4: '#18b4f1',
}

bucket_colors = d3.scale.ordinal()
    .range(['#dd2ea3', '#ffafe5', '#fff', '#94e1ff', '#18b4f1'])

stationClassifier = (poles, available) ->
        bikes = poles - available
        if bikes == 0
            return 0
        else if bikes <= 5
            return 1
        else if available <= 5
            return 3
        else if available == 0
            return 4
        else
            return 2  # middle state is normal.

renderStationMap = (elem) ->
    id = $(elem).attr('data-id')
    coords =
        lat: Number($(elem).attr('data-lat')),
        lon: Number($(elem).attr('data-lon')),
    bucket = stationClassifier($(elem).attr('data-poles'),
                               $(elem).attr('data-available'))

    baseLayer = mapbox.layer().tilejson(TELOSTATS_TILEJSON)
    markerLayer = mapbox.markers.layer()
    markerLayer.add_feature(
        geometry:
            type: "Point",
            coordinates: [coords.lon, coords.lat],
    ).factory((f) ->
        marker = ich.stationmarker_svg_template({bucket: bucket})
        return marker[0]
        # img = document.createElement('img')
        # img.className = 'station-marker'
        # img.setAttribute('src', f.properties.image)
        # img.setAttribute('data-bucket', bucket)
        # return img
    )

    stationmap = mapbox.map(elem, [], null, [])
    stationmap.addLayer(baseLayer)
    stationmap.addLayer(markerLayer)

    # set center and z17, no animation
    stationmap.centerzoom(coords, 17, false)


renderStationScale = (elem) ->
    id = $(elem).attr('data-id')
    poles = Number($(elem).attr('data-poles'))
    available = Number($(elem).attr('data-available'))
    bikes = poles - available
    bucket = stationClassifier(poles, available)

    switch bucket
        when 0
            section = 'empty'
            direction = 'left'
            percent = -0.09
        when 1
            section = 'empty'
            direction = 'left'
            percent = bikes / 5
        when 2
            section = 'ok'
            direction = 'left'
            percent = ((bikes - 5) / (available + bikes - 10))
        when 3
            section = 'full'
            direction = 'right'
            percent = available / 5
        when 4
            section = 'full'
            direction = 'right'
            percent = -0.09

    marker = ich.stationscale_marker_template({
        'direction': direction,
        'percent': percent * 100,
        'bikes': bikes,
        'poles': available
    })

    $("[data-id=#{id}] .station-slider-bar>.#{section}").append(marker);


renderTimeline = (data, elem) ->
    # Render a timeline using data and stick it in elem

    margin = {top: 0, right: 0, bottom: 25, left: 0}
    width = $(elem).width() - margin.right - margin.left
    console.log($(elem).height())
    height = $(elem).height() - margin.top - margin.bottom
    console.log(height)
    console.log(width)
    svg = d3.select(elem).append('svg')
                         .attr('class', 'timeline')
                         .attr('width', width + margin.right + margin.left)
                         .attr('height', height + margin.top + margin.bottom)
                         .append('g')
                         .attr("transform", "translate(#{margin.left},#{margin.top})");

    iso = d3.time.format.iso;

    x = d3.time.scale()
        .range([0, width])
        .domain(d3.extent(data, (d) -> return iso.parse(d.timestamp) ))

    xWidth = d3.scale.linear()
             .domain([0, data.length])
             .range([0, width])

    xAxis = d3.svg.axis()
            .scale(x)
            .orient('bottom')
            .ticks(d3.time.hours, 3)
            .tickSubdivide(2)
            .tickSize(5, 3)
            .tickFormat(d3.time.format('%H'))

    colors = svg.append('g')

    colors.selectAll('.timespan')
        .data(data)
        .enter().append('rect')
        .attr('height', 15)
        .attr('width', (d, i) -> xWidth(1))
        .attr('fill', (d) ->
            return bucket_colors(stationClassifier(d.poles, d.available)))
        .attr('transform', (d) ->
            offset = x(iso.parse(d.timestamp))
            return "translate(#{offset}, 0)")

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);


renderHistoryTimeline = (elem) ->
    id = $(elem).attr('data-id')
    d3.json("/api/v1/recent/#{id}", (recent) ->
        renderTimeline(recent.series, elem))


stationsLayer = (opts) ->
    map = opts.map
    stationData = opts.stations
    stationCoords = ([s.longitude, s.latitude] for s in stationData)


    svg = d3.select(document.body).append('svg').attr('id', 'd3svg')
    stations = svg.append('g').attr('id', 'stations')
    fadeInTime = 500
    animationDelayTime = 600

    stationDotSize = d3.scale.quantize()
        .domain([opts.minZoom, opts.maxZoom])
        .range([2, 3, 4])

    stationAnimation = d3.scale.linear()
        .domain(d3.extent(stationCoords, (coord) -> return coord[1] ))
        .range([0, fadeInTime])


    project = (location) ->
        point = map.locationPoint({ lat: location[1], lon: location[0] })
        return [point.x, point.y]

    stationAnimationWait = (index) ->
        return stationAnimation(stationData[index].latitude)

    registerMapMouseDragHandlers = (elem) ->
        d3elem = d3.select(elem)
        stationid = d3elem.attr('data-id')

        d3elem.classed('loading', false)
        clientX = null
        clientY = null
        d3elem.on('mousedown', (d, i) ->
            clientX = d3.event.clientX
            clientY = d3.event.clientY
        )

        d3elem.on('mouseup', (d, i) ->
            stationary = clientX == d3.event.clientX &&
                         clientY == d3.event.clientY
            if d3elem.classed('selected')
                # do nothing, we're already ok.
                return
            if stationary
                d3.selectAll('.station').classed('selected', false)
                newflyout = ich.stationflyout_template({stationid: stationid})
                $('#stationflyouts').append(newflyout)
                opts = {
                    url: '/station/' + stationid,
                    container: ".stationflyout[data-id=#{stationid}]"
                    timeout: 2000
                }

                d3elem.classed('selected', true)
                $.pjax(opts)
                $(newflyout).on('pjax:end', ->
                    mapelem = $(".station-map[data-id='#{stationid}']")[0]
                    historyelem = $(".history-timeline[data-id='#{stationid}']")[0]
                    renderStationMap(mapelem)
                    renderStationScale(mapelem)
                    renderHistoryTimeline(historyelem)
                    $(this).removeClass('hidden')
                    setTimeout( ->
                        $('.flyout.secondary:not(.stationflyout)').addClass('hidden')
                        $(".stationflyout[data-id!=#{stationid}]").remove()
                    , 200)
                )
        )

    drawStations = () ->
        stationDelay = (d, i) ->
            return animationDelayTime + fadeInTime - stationAnimationWait(i)

        cellGroups = stations.selectAll('g').data(stationData)
        groupsEnter = cellGroups.enter().append('g')
        cellsEnter = groupsEnter.append('path')
        dotsEnter = groupsEnter.append('circle')

        dots = stations.selectAll('g>circle').data(stationData)

        # Position the dots
        dots
            .attr('r', stationDotSize(map.zoom()))
            .attr('transform', (d) ->
                return 'translate(' + project([d.longitude, d.latitude]) + ')' )

        groupsEnter
            .classed('station', true)
            .classed('loading', true)
            .attr('data-id', (d, i) -> return stationData[i].id)
            .attr('data-lat', (d, i) -> return stationData[i].latitude)
            .attr('data-lon', (d, i) -> return stationData[i].longitude)
            .attr('data-bucket', (d, i) -> return stationClassifier(
                stationData[i].poles, stationData[i].available
            ))
            .attr('data-poles', (d, i) -> return stationData[i].poles)
            .attr('data-available', (d, i) -> return stationData[i].available)
            .transition()
            .delay(stationDelay)
            .duration(200)
            .each('end', -> registerMapMouseDragHandlers(this))


        # Fade in the cells on load
        cellsEnter
            .classed('station_cell', true)

        # fade in the dots on load
        dotsEnter
            .classed("station_dot", true)
            .attr('opacity', 0.0)
            .attr('r', 0)
            .attr('transform', (d) ->
                return 'translate(' + project([d.longitude, d.latitude]) + ')' )
            .transition()
            .delay(150)
            .duration(450)
            .attr('opacity', 0.15)
            .attr('r', 8 * stationDotSize(map.zoom()))
            .transition()
            .delay(stationDelay)
            .duration(200)
            .attr('r', stationDotSize(map.zoom()))
            .attr('opacity', 1)


        # draw the projected cells onto the map
        stations
            .selectAll('g>path')
            .data(stationData)
            .attr('d', (d, i) ->
                poly = d3.geom.polygon(stationData[i].polygon)
                projected = (project(p) for p in poly)
                return 'M' + projected.join('L') + 'Z'
            )

    draw = ->
        # position the overlay
        svg.attr('width', $('#map').width())
           .attr('height', $('#map').height())

        # draw the stations
        drawStations()

    layer = {
        'project': project,
        'draw': draw,
        'parent': svg.node(),
    }

    return layer

initMap = ->
    m = mapbox.map('map')
    minZoom = TELOSTATS_TILEJSON.minzoom
    maxZoom = TELOSTATS_TILEJSON.maxzoom
    m.addLayer(mapbox.layer().tilejson(TELOSTATS_TILEJSON))
    m.ui.zoomer.add()
    mapbounds = new MM.Extent(
        32.149, 34.742,
        32.026, 34.924)
    m.setExtent(mapbounds)
    m.setPanLimits(mapbounds)
    m.setZoomRange(minZoom, maxZoom)
    return m

initStations = (map, selectedid) ->
    d3.json('/api/v1/station/', (stations) ->
        opts = {
            'map': map,
            'stations': stations.objects,
            'minZoom': TELOSTATS_TILEJSON.minzoom,
            'maxZoom': TELOSTATS_TILEJSON.maxzoom,
        }
        sl = stationsLayer(opts)
        map.addLayer(sl)
        map.refresh()
        if selectedid
            elem = d3.select(".station[data-id=\"#{selectedid}\"]")
            elem.classed('selected', true)
        initStationPie(stations.objects)
    )

initStationPie = (stations) ->
    buckets = _.map(stations, (s) ->
        return stationClassifier(s.poles, s.available))
    counts = _.countBy(buckets, (b) -> return b)
    pctformat = d3.format('.1p')
    data = ({
        bucket: Number(k),
        value: Number(v),
        percentage: pctformat(Number(v) / stations.length)
        } for k,v of counts)
    data = _.sortBy(data, (x) -> return x.bucket)

    pie_w = $('#stations-overview-pie').width()
    pie_h = $('#stations-overview-pie').height()
    pie_radius = Math.min(pie_w, pie_h) / 2;
    arc = d3.svg.arc()
        .outerRadius(pie_radius - 10)
        .innerRadius(pie_radius - 70)
    pie = d3.layout.pie()
        .sort(null)
        .value((d) -> return d.value)

    piesvg = d3.select('#stations-overview-pie').append('svg')
            .attr('width', pie_w)
            .attr('height', pie_h)
          .append('g')
            .attr("transform", "translate(#{pie_w / 2},#{pie_h / 2})")

    g = piesvg.selectAll(".arc")
            .data(pie(data))
            .enter().append("g")
            .attr("class", "arc");

    g.append("path")
        .attr("d", arc)
        .style("fill", (d, i) -> return bucket_colors(d.data.bucket) )

    g.append("text")
        .attr("transform", (d) -> return "translate(#{arc.centroid(d)})" )
        .attr("dy", ".35em")
        .style("text-anchor", "middle")
        .text((d, i) -> return d.data.percentage )





pushStateNav = (url) ->
    window.history.pushState(null, '', url)
    if _gaq?
        _gaq.push(['_trackPageview', url])


$ ->
    map = initMap()
    selectedid = $('.stationflyout').attr('data-id')
    initStations(map, selectedid)
    if selectedid
        stationelem = $(".station[data-id=#{selectedid}]")[0]
        if stationelem
            d3.select(stationelem).classed('selected', true)
    _.each($(".station-map"), renderStationMap)
    _.each($(".station-map"), renderStationScale)
    _.each($(".history-timeline"), renderHistoryTimeline)
    $(document).pjax('a[data-pjax]')

    $('.close-flyout').live('click', (e) ->
        $(this).parent().addClass('hidden')
        d3.select('.selected').classed('selected', false)
        pushStateNav($(this).attr('href'))
        return false
    )

    $('a.static-flyout').click( ->
        target = $(this).attr('data-flyout')
        $(target).removeClass('hidden')
        pushStateNav($(this).attr('href'))
        return false
    )
