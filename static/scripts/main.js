function loadMap(el) {

  // We need to get the route first, so that we can get an idea of the sizing...
  var rideLayer = L.mapbox.featureLayer()
      .loadURL('/rides/' + el.dataset.rideId + '.json');

  rideLayer.on('ready', function() {
    var map = L.mapbox.map(el.getElementsByClassName('content')[0], 'mapbox.streets', {zoomControl: false});
    map.dragging.disable();
    map.touchZoom.disable();
    map.doubleClickZoom.disable();
    map.scrollWheelZoom.disable();

    rideLayer.addTo(map);

    map.fitBounds(rideLayer.getBounds());
  });
}

document.addEventListener("DOMContentLoaded", function(event) {
  var maps = document.querySelectorAll('.map');

  loadMap(maps[0]);
});