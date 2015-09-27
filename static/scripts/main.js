var map;
var ride;

function loadMap() {
  var mapEl = document.querySelectorAll('.map');
  if (mapEl.length === 0) {
    return;
  } else {
    mapEl = mapEl[0];
  }
  map = new mapboxgl.Map({
      container: mapEl, // container id
      style: 'mapbox://styles/mapbox/streets-v8', //stylesheet location
      center: ride.getCenter(),
      zoom: 7,
      interactive: false
  });
  map.fitBounds(ride.getBounds(), {padding: 25});

  map.on('style.load', function () {
    map.addSource('route', {
      'type': 'geojson',
      'data': ride.getGeoJSON()
    });
    map.addLayer({
      "id": "route",
      "type": "line",
      "source": "route",
      "layout": {
        "line-join": "round",
        "line-cap": "round"
      },
      "paint": {
        "line-color": "#888",
        "line-width": 4
      }
    });

    var startCoords = ride.getDataForMilage(0).coordinates;
    map.addSource('marker', {
      'type': 'geojson',
      'data': {
        'type': 'Feature',
        'geometry': {
          'type': 'Point',
          'coordinates': startCoords
        },
        'properties': {
          'marker-symbol': 'circle'
        }
      }
    });
    map.addLayer({
      'id': 'marker',
      'type': 'symbol',
      'source': 'marker',
      'layout': {
        'icon-image': '{marker-symbol}-15',
      },
    });
  });
}

document.addEventListener('DOMContentLoaded', function(event) {
  mapboxgl.accessToken = MAPBOX_TOKEN;  // Init the mapbox token

  var mapEl = document.querySelectorAll('.map');
  if (mapEl.length === 0) {
    return;
  } else {
    mapEl = mapEl[0];
  }

  if (mapEl.dataset.rideId) {
    ride = new Ride(mapEl.dataset.rideId);
    ride.on('loaded', loadMap)
    ride.load();
  }

  var mileageEl = document.querySelectorAll('.mileage span')[0];
  var speedEl = document.querySelectorAll('.speed span')[0];

  var sliderEl = document.querySelectorAll('.slider')[0];

  sliderEl.addEventListener('change', function(e) {
    if (!map) {
      return;
    }
    var miles = (parseFloat(e.target.value) / 100) * ride.distance;
    var data = ride.getDataForMilage(miles);
    map.flyTo({center: data.coordinates, zoom: 12});
  });

  sliderEl.addEventListener('input', function(e) {
    if (!map) {
      return;
    }
    var miles = (parseFloat(e.target.value) / 100) * ride.distance;
    var data = ride.getDataForMilage(miles);

    mileageEl.innerHTML = data.miles;
    speedEl.innerHTML = data.speed;


    var marker = map.getSource('marker');

    if (map.getZoom() == 12) {
      map.fitBounds(ride.getBounds(), {padding: 25});
    }

    marker.setData({
      'type': 'Feature',
      'geometry': {
        'type': 'Point',
        'coordinates': data.coordinates
      },
      'properties': {
        'marker-symbol': 'circle'
      }
    });
    map.update(true);
  });
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
  if (map) {
    var sliderEl = document.querySelectorAll('.slider')[0];
    if (sliderEl.value === 0 || sliderEl.value === 100) {
      map.fitBounds(ride.getBounds(), {padding: 25});
    } else {
      var marker = map.getSource('marker');
      if (marker) {
        map.easeTo({center: marker._data.geometry.coordinates});
      }
    }
    
  }
}, 250);

window.addEventListener('resize', debouncedResize);