var Ride = function (rideId) {
  this.id = rideId;

  this.eventListeners = {};
};

Ride.prototype.on = function(eventName, callback) {
  this.eventListeners[eventName] = callback;
}

Ride.prototype.load = function() {
  var self = this;
  var url = '/rides/' + this.id + '.json'
  var request = new XMLHttpRequest();
  request.open('GET', url, true);
  
  request.onload = function() {
    if (request.status >= 200 && request.status < 400) {
      var rideData = JSON.parse(request.responseText);

      for (var key in rideData) {
        self[key] = rideData[key];
      }
    } else {
      console.log('loading error');
    }
    if (self.eventListeners.loaded) {
      self.eventListeners.loaded();  // Run the callback
    };
  }

  request.onerror = function() {
    console.log('loading error');
  };

  request.send();
};

Ride.prototype.getBounds = function() {
  var extent = turf.extent(this.getGeoJSON());

  return [
    [extent[0], extent[1]],
    [extent[2], extent[3]],
  ]
}

Ride.prototype.getCenter = function() {
  return turf.center(this.getGeoJSON()).geometry.coordinates
}

Ride.prototype.getGeoJSON = function() {
  var coordinates = [];
  for(var i=0;i<this.data.length;i++) {
    coordinates.push(this.data[i]['coordinates']);
  }

  return {
    'type': 'FeatureCollection',
    'features': [
      {
        'type': 'Feature',
        'geometry': {
          'type': 'LineString',
          'coordinates': coordinates
        },
        'properties': {}
      }
    ]
  }
}

Ride.prototype.getDataForMilage = function(miles) {
  var minIndex = 0;
  var maxIndex = this.data.length - 1;
  var currentIndex;
  var currentElement;
 
  while (minIndex <= maxIndex) {
    currentIndex = (minIndex + maxIndex) / 2 | 0;
    currentElement = this.data[currentIndex];

    if (currentElement.miles < miles) {
      minIndex = currentIndex + 1;
    }
    else if (currentElement.miles > miles) {
      maxIndex = currentIndex - 1;
    }
    else {
      break;
    }
  }
  return currentElement;
}