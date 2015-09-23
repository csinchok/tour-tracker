var map;
var bounds; // bounds of the current viewed object
var graph;


function loadRide(rideId) {

  // We need to get the route first, so that we can get an idea of the sizing...
  var rideLayer = L.mapbox.featureLayer()
      .loadURL('/rides/' + rideId + '.json');

  rideLayer.on('ready', function() {

    rideLayer.addTo(map);

    map.fitBounds(rideLayer.getBounds());
    bounds = rideLayer.getBounds();

    // graph = new Rickshaw.Graph( {
    //         element: document.querySelector("#chart"),
    //         width: window.outerWidth,
    //         height: 75,
    //         series: [ {
    //                 color: 'steelblue',
    //                 data: data
    //         }]
    // } );

    // graph.render();
  });
}

document.addEventListener('DOMContentLoaded', function(event) {
  var mapEl = document.querySelectorAll('.map');
  if (mapEl.length === 0) {
    return;
  } else {
    mapEl = mapEl[0];
  }

  map = L.mapbox.map(mapEl, 'mapbox.streets');
  // map.dragging.disable();
  // map.touchZoom.disable();
  // map.doubleClickZoom.disable();
  // map.scrollWheelZoom.disable();

  if (mapEl.dataset.rideId) {
    loadRide(mapEl.dataset.rideId);
  }
});


function debounce(func, wait, immediate) {
  var timeout;
  return function() {
    var context = this, args = arguments;
    var later = function() {
      timeout = null;
      if (!immediate) func.apply(context, args);
    };
    var callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) func.apply(context, args);
  };
};


var debouncedResize = debounce(function() {
  if (window.bounds) {
    map.fitBounds(window.bounds);
  }
  
}, 250);

window.addEventListener('resize', debouncedResize);