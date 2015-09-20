function loadMap(el) {

  // We need to get the route first, so that we can get an idea of the sizing...
  var rideLayer = L.mapbox.featureLayer()
      .loadURL('/rides/' + el.dataset.rideId + '.json');

  rideLayer.on('ready', function() {
    console.log(rideLayer.getBounds());

    var bounds = rideLayer.getBounds();
    var width = Math.abs(bounds.getWest() - bounds.getEast());
    var height = Math.abs(bounds.getNorth() - bounds.getSouth());

    var ratio = width / height;

    if (ratio >= (16 / 9)) {
      el.classList.add('aspect16x9');
    } else {
      el.classList.add('aspect1x1');
    }

    var map = L.mapbox.map(el.getElementsByClassName('content')[0], 'mapbox.streets', {zoomControl: false});

    map.dragging.disable();
    map.touchZoom.disable();
    map.doubleClickZoom.disable();
    map.scrollWheelZoom.disable();

    rideLayer.addTo(map);

    map.fitBounds(rideLayer.getBounds());

    setTimeout(function(){
      map.invalidateSize()
    }, 3000);
  });
}

document.addEventListener("DOMContentLoaded", function(event) {
  var maps = document.querySelectorAll('.map');

  loadMap(maps[0]);
});