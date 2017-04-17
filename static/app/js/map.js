const map = L.map('map').setView([53.3, -6.3], 5);
const friends_list = document.getElementsByClassName("friend-list-item");
var myLatLon;

L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v10/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoiem9udHppcCIsImEiOiJjajFtbGJrYjEwMDAxMzNvdGs4OXByM2dhIn0.hzPQNENTIuVgt7fPXsUD5Q', {})
    .addTo(map);

map_init();

for (var i = 0; i < friends_list.length; i++) {
    friends_list[i].addEventListener('click', function(e) {
        map_set(this);
    })
}

function map_init() {
    var geom = JSON.parse($("#geom").html());
    myLatLon = L.latLng([geom.coordinates[1], geom.coordinates[0]]);

    geom = L.geoJson(geom);
    var marker = L.marker(myLatLon)
        .addTo(map)
        .bindPopup("Me")
        .openPopup();

    map.setView(myLatLon, 16);
}

function map_set(element) {
    var geom = JSON.parse(element.dataset.location);
    var LatLon = L.latLng([geom.coordinates[1], geom.coordinates[0]]);
    var distance = LatLon.distanceTo(myLatLon) < 1000 ? Math.round(LatLon.distanceTo(myLatLon)) + ' m' : Math.round(LatLon.distanceTo(myLatLon) / 1000) + ' km';

    var name = element.dataset.firstname + ' ' + element.dataset.lastname;

    var info = "<dl><dt>" + name + "</dt>"
           + "<dd>" + distance + "</dd>";

    geom = L.geoJson(geom);
    var marker = L.marker(LatLon)
        .addTo(map)
        .bindPopup(info)
        .openPopup();

    map.setView(LatLon, 16);
}
