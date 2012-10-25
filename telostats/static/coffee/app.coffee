
stationsLayer = (opts) ->
    map = opts.map
    stationData = opts.stations
    stationCoords = ([s.longitude, s.latitude] for s in stationData)


    svg = d3.select(document.body).append('svg').attr('id', 'd3svg')
    stations = svg.append('g').attr('id', 'stations')
    fadeInTime = 500
    animationDelayTime = 600

    stationColor = (station) ->
        bikes = station.poles - station.available;
        if bikes == 0
            return 0
        else if bikes <= 5
            return 1
        else if station.available <= 5
            return 3
        else if station.available == 0
            return 4
        else
            return 2  # middle state is normal.

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
                }

                d3elem.classed('selected', true)
                $.pjax(opts)
                $(newflyout).on('pjax:end', ->
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
            .attr('data-id', (d, i) -> return stationData[i].id )
            .attr('data-bucket', (d, i) -> return stationColor(stationData[i]) )
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
    telostats_tiles = {
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
    minZoom = 13
    maxZoom = 17
    m.addLayer(mapbox.layer().tilejson(telostats_tiles))
    m.ui.zoomer.add()
    mapbounds = new MM.Extent(
        32.149, 34.742,
        32.026, 34.924)
    m.setExtent(mapbounds)
    m.setPanLimits(mapbounds)
    m.setZoomRange(minZoom, maxZoom)


    d3.json('/api/v1/station/', (stations) ->
        opts = {
            'map': m,
            'stations': stations.objects,
            'minZoom': minZoom,
            'maxZoom': maxZoom,
        }
        sl = stationsLayer(opts)
        m.addLayer(sl)
    )

pushStateNav = (url) ->
    window.history.pushState(null, '', url)
    if _gaq?
        _gaq.push(['_trackPageview', url])

$ ->
    initMap()
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
