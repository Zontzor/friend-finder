/**
 * Created by alex on 11/04/17.
 */

function map_init(map, options) {
    var geom = JSON.parse($("#geom").html());
    var myLatLon = L.latLng([geom.coordinates[1], geom.coordinates[0]]);

    geom = L.geoJson(geom);
    geom.addTo(map);

    map.setView(myLatLon, 16);
}