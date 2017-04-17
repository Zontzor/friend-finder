/**
 * Created by alex on 11/04/17.
 */

const friends_list = document.getElementsByClassName("friend-list-item");
var leafletmap = null;

function map_init(map, options) {
    leafletmap = map;
    var geom = JSON.parse($("#geom").html());
    var myLatLon = L.latLng([geom.coordinates[1], geom.coordinates[0]]);

    geom = L.geoJson(geom);
    geom.addTo(map);

    map.setView(myLatLon, 16);
}

function map_set(element) {
    var geom = JSON.parse(element.dataset.location);
    var myLatLon = L.latLng([geom.coordinates[1], geom.coordinates[0]]);

    geom = L.geoJson(geom);
    geom.addTo(leafletmap);

    leafletmap.setView(myLatLon, 16);
}

function resize() {
    var heights = window.innerHeight;
    document.getElementById("map").style.height = heights-52 + "px";
}

resize();

window.onresize = function() {
    resize();
};


for (var i = 0; i < friends_list.length; i++) {
    friends_list[i].addEventListener('click', function(e) {
        map_set(this);
    })
}
