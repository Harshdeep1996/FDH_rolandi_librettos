var mymap = L.map('mapid').setView([43, 11], 6);

// Stop the map from moving on left and right, by user input
mymap.dragging.disable();

// Public token (for mapbox): pk.eyJ1IjoiaGFyc2hjczE5OTYiLCJhIjoiY2tndGdrcmZ3MGF0ZjJ6cGVtenNlMXdzOCJ9.xXRLIH9aN6I7W9bHyXK-ag

L.tileLayer('http://{s}.tile.stamen.com/toner-background/{z}/{x}/{y}.png', {
    attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
    subdomains: 'abcd',
    // Fix the zoom, so that users cannot move the zoom
    minZoom: 5,
    maxZoom: 6
}).addTo(mymap);

//Data is usable here
var max_year = -Number.MAX_VALUE;
var min_year = Number.MAX_VALUE;

// Index containing the year, and maps the value selected on the slider 
var dictYearsObj = {};
var global_results = null;
var latLongMap = {};
var markersCurrently = [];


function doStuff(data) {
    //Data is usable here
    var years = [];

    data.forEach(function (o) {
      if (typeof o[3] !== 'string') {
        years.push(parseInt(o[3], 10));
      }
    });

   years = years.slice(0, 692);
   min_year = Math.min(...years);
   max_year = Math.max(...years);

   // Taking the range for every 22 years
   var ranges = _.range(min_year, max_year, 22);
   var total_ranges = ranges.length;

   // Setting the range of the slider and setting the half value
   document.getElementById('myRange').max = (total_ranges - 1) * 10;
   document.getElementById('myRange').value = (parseInt(total_ranges / 2, 10) + 3) * 10;

   // get the wrapper element for adding the ticks
   var step_list = document.getElementsByClassName('menuwrapper')[0];
   var step_list_two = document.getElementsByClassName('menuwrapper2')[0];

   // Adding years with marking on the slider as p tags
   for (var index = 0; index <= total_ranges - 1; index++) {
     dictYearsObj[index] = ranges[index];
     var span = document.createElement("span");
     span.style.marginTop = "-14px";
     span.style.marginLeft = "2px";
     span.innerHTML = '|';
     step_list.appendChild(span);

     // for the labels
     var span_two = document.createElement("span");
     span_two.innerHTML = ranges[index];
     span_two.style.marginTop = "-14px";
     step_list_two.appendChild(span_two);
   }
}

// Parse data from papa parse CSV
function parseData(url, callBack) {
  Papa.parse(url, {
    download: true,
    dynamicTyping: true,
    complete: function(results) {
        // Assigning the results so that we can play with it
        global_results = results.data;
        callBack(results.data);
    }
  });
}
parseData("http://0.0.0.0:1234/data/get_librettos.csv", doStuff);

function hoverAndDoThings() {
    // Make a textual pane when we find the city and click on the point
    // and then we remove it, when we click on something else
    var city_name = this._tooltip._content.split(":")[2];
    console.log(city_name);
}

function plotIntensityMap(cityResults) {    
    // console.log(cityResults);
    Object.keys(cityResults).forEach(function(o){
        var lat = latLongMap[o][0];
        var long = latLongMap[o][1];
        // Adding a marker and an associated popup
        // Use circle marker to get the right radius
        var marker = L.circleMarker([lat, long], {color: 'grey', fillColor: 'rgb(123,61,63)', fillOpacity: 0.9, radius: 15}).addTo(mymap);
        marker.bindTooltip("Number of librettos: " + cityResults[o] + " in city of: " + o, {
            permanent: false, className: "my-label", offset: [0, 0]
        });
        marker.on('click', hoverAndDoThings);
        mymap.addLayer(marker);
        markersCurrently.push(marker);
    });
}

// Detecting the slider in HTML
var slider = document.getElementById("myRange");

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
  // Remove any exists markers which might be present on the map
  if(markersCurrently.length !== 0) {
    for (var index = 0; index < markersCurrently.length; index++) {
        mymap.removeLayer(markersCurrently[index]);
    }
    markersCurrently = [];
  }

  var value_selected = slider.value / 10;
  // console.log(value_selected / 10);

  var getSubResult = {};
  global_results.forEach(function (o) {
    if ((typeof o[3] !== 'string') && ((o[3 ] >= dictYearsObj[value_selected]) && (o[3] <= dictYearsObj[value_selected] + 22))) {
        latLongMap[o[7]] = [o[8], o[9]];
        getSubResult[o[7]] = (getSubResult[o[7]] || 0) + 1;
    }
  });

  plotIntensityMap(getSubResult);
}
