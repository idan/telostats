
stationsLayer = (opts) ->
    map = opts.map
    stationData = opts.stations
    stationCoords = ([s.longitude, s.latitude] for s in stationData)


    svg = d3.select(document.body).append('svg').attr('id', 'd3svg')
    stationCellsGroup = svg.append('g').attr('id', 'stationcells')
    stationDotsGroup = svg.append('g').attr('id', 'stationdots')
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
        clientX = null
        clientY = null
        $(elem).on('mousedown', (event) ->
            clientX = event.clientX
            clientY = event.clientY
        )

        $(elem).on('mouseup', (event) ->
            stationary = clientX == event.clientX &&
                         clientY == event.clientY
            if stationary
                $('.station_cell').attr('data-state', 'visible')
                $('#stationflyout').attr('data-state', 'hidden')
                container = $('#stationflyout')
                opts = {
                    url: '/station/' + $(this).attr('data-id'),
                    container: container
                }

                $.pjax(opts)
                $(this).attr('data-state', 'selected')

                container.on('pjax:end', ->
                    $('#stationflyout').attr('data-state', 'visible')
                )
        )

    drawStationCells = () ->
        cells = stationCellsGroup.selectAll('path').data(stationData)

        # Animate fade-in of cells
        # happens only once, at load
        cells.enter()
            .append('path')
            .data(stationData)
            .attr('id', (d, i) -> return 'station' + stationData[i].id )
            .classed('station_cell', true)
            .attr('data-id', (d, i) -> return stationData[i].id )
            .attr('data-bucket', (d, i) -> return stationColor(stationData[i]) )
            .attr('data-state', 'loading')
            .transition()
            .delay((d, i) ->
                return animationDelayTime + fadeInTime - stationAnimationWait(i))
            .duration(1000)
            .attr('data-state', 'visible')
            .each('end', -> registerMapMouseDragHandlers(this))

        # draw the projected cells onto the map
        cells.attr('d', (d, i) ->
            poly = d3.geom.polygon(stationData[i].polygon)
            projected = (project(p) for p in poly)
            return 'M' + projected.join('L') + 'Z'
        )


    drawStationDots = () ->
        dots = stationDotsGroup.selectAll('circle').data(stationCoords)

        # Position the dots
        dots
            .attr('r', stationDotSize(map.zoom()))
            .attr('transform', (d) ->
                return 'translate(' + project(d) + ')' )

        # Animate grow-in of dots
        # happens only once, on load
        dots.enter()
            .append('circle')
            .attr('opacity', 0.0)
            .attr('r', 0)
            .attr('transform', (d) ->
                return 'translate(' + project(d) + ')' )
            .transition()
            .delay(150)
            .duration(450)
            .attr('opacity', 0.15)
            .attr('r', 8 * stationDotSize(map.zoom()))
            .transition()
            .delay((d, i) ->
                return animationDelayTime + fadeInTime - stationAnimationWait(i))
            .duration(200)
            .attr('r', stationDotSize(map.zoom()))
            .attr('opacity', 1)



    draw = ->
        # position the overlay
        svg.attr('width', $('#map').width())
           .attr('height', $('#map').height())
        drawStationCells()
        drawStationDots()

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
        'tiles': [TILESERVER_URL],
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

$ ->
    initMap()
    $(document).pjax('a[data-pjax]')
    $('.close-flyout').live('click', (e) ->
        $(this).parent().attr('data-state', 'hidden')
        url = '/'
        window.history.pushState(null, '', url)
        _gaq.push(['_trackPageview', url])
        return false
    )

    $('a#about').click( ->
        $('#aboutflyout').attr('data-state', 'visible')
        url = '/about'
        window.history.pushState(null, '', url)
        _gaq.push(['_trackPageview', url])
        return false
    )
