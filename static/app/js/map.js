const map = L.map('map').setView([53.3, -6.3], 5);
const friends_list = document.getElementsByClassName("friend-list-item");

L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v10/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoiem9udHppcCIsImEiOiJjajFtbGJrYjEwMDAxMzNvdGs4OXByM2dhIn0.hzPQNENTIuVgt7fPXsUD5Q', {})
    .addTo(map);

function map_init() {
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

for (var i = 0; i < friends_list.length; i++) {
    friends_list[i].addEventListener('click', function(e) {
        map_set(this);
    })
}
