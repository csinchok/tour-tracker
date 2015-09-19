function loadMap(el) {
  var map = L.mapbox.map(el, 'mapbox.streets').setView([41.881832, -87.623177], 9);

  var rideLayer = L.mapbox.featureLayer()
      .loadURL('/rides/' + el.dataset.rideId + '.json')
      .addTo(map);

  rideLayer.on('ready', function() {
    map.fitBounds(rideLayer.getBounds());
  });
}

document.addEventListener("DOMContentLoaded", function(event) {
  var maps = document.getElementsByClassName('map');

  loadMap(maps[0]);
});