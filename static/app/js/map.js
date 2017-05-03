const myGeom = JSON.parse($("#geom").html());
const myLatLon = L.latLng([myGeom.coordinates[1], myGeom.coordinates[0]]);

// Maps (Live and Dev)
const mapUrl = 'https://api.mapbox.com/styles/v1/mapbox/streets-v10/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoiem9udHppcCIsImEiOiJjajFtbGJrYjEwMDAxMzNvdGs4OXByM2dhIn0.hzPQNENTIuVgt7fPXsUD5Q';

// Friend marker array
const markers = {};

// Create map
const map = L.map('map').setView([53.3, -6.3], 5);
    L.tileLayer(mapUrl, {})
        .addTo(map);

init_map();

function init_map() {
    // Init user geo
    set_user();

    // Init friends list geo
    const friends_list = document.getElementsByClassName("friend-list-item");
    for (var i = 0; i < friends_list.length; i++) {
        friends_list[i].addEventListener('click', function(e) {
            set_friend(this);
        })
    }
}


function set_user() {
    var marker = L.marker(myLatLon)
        .addTo(map)
        .bindPopup("Me")
        .openPopup();

    map.setView(myLatLon, 16);
}


function set_friend(element) {
    if (element.dataset.location === '') {
        return;
    }
    var geom = JSON.parse(element.dataset.location);
    var LatLon = L.latLng([geom.coordinates[1], geom.coordinates[0]]);
    var distance = LatLon.distanceTo(myLatLon) < 1000 ? Math.round(LatLon.distanceTo(myLatLon)) + ' m' : Math.round(LatLon.distanceTo(myLatLon) / 1000) + ' km';
    var info = "<dl>" + "<dt>" + element.dataset.firstname + ' ' + element.dataset.lastname + "</dt>" + "<dt>" + distance + "</dt>" + "</dl>";

    if (markers[element.dataset.id]) {
        map.removeLayer(markers[element.dataset.id]);
        markers[element.dataset.id] = null;
    } else {
        markers[element.dataset.id] = L.marker(LatLon)
        .addTo(map)
        .bindPopup(info)
        .openPopup();

        map.panTo(LatLon, 16);
    }
}
