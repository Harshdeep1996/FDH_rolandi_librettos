// Global latitude and longiitude
const globalLat = 43;
const globalLong = 11;

//Data is usable here
var max_year = -Number.MAX_VALUE;
var min_year = Number.MAX_VALUE;

// Index containing the year, and maps the value selected on the slider 
var dictYearsObj = {};
var global_results = null;
var latLongMap = {};
var markersCurrently = [];
var zoomClick = false;
var lastCityClicked = null;

// Indexes for array to trace in the data we retrieve from CSV
const TITLE_INDEX = 2;
const YEAR_INDEX = 3;
const CITY_INDEX = 7;
const LAT_INDEX = 8;
const LONG_INDEX = 9;
const THEATER_LAT = 15;
const THEATER_LONG = 16;

var mymap = L.map('mapid').setView([globalLat, globalLong], 6);

// Stop the map from moving on left and right, by user input
mymap.dragging.disable();

// Public token (for mapbox): pk.eyJ1IjoiaGFyc2hjczE5OTYiLCJhIjoiY2tndGdrcmZ3MGF0ZjJ6cGVtenNlMXdzOCJ9.xXRLIH9aN6I7W9bHyXK-ag

L.tileLayer('http://{s}.tile.stamen.com/toner-background/{z}/{x}/{y}.png', {
    attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
    subdomains: 'abcd',
    // Fix the zoom, so that users cannot move the zoom
    minZoom: 5,
    maxZoom: 10
}).addTo(mymap);

function doStuff(data) {
    //Data is usable here
    var years = [];

    data.forEach(function (o) {
      if (typeof o[YEAR_INDEX] !== 'string') {
        years.push(parseInt(o[YEAR_INDEX], 10));
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

parseData("http://0.0.0.0:1234/data/get_librettos_dummies.csv", doStuff);

function hoverAndDoThings(mouseObj, yearSelected) {
    // Make a textual pane when we find the city and click on the point
    // and then we remove it, when we click on something else
    var scrollTextPane = document.getElementById('scrollText');
    var city_name = mouseObj._tooltip._content.split(":")[2].replace(/\s+/, "");

    // Remove the panel cards if some of them exists already
    if(scrollTextPane.children.length !== 0) {
      var panels = document.getElementsByClassName("w3-panel w3-blue w3-card-4");
      // pop off each of the panels
      while (panels.length > 0) {
        panels[0].parentNode.removeChild(panels[0]);
      }
      var heading = document.getElementsByClassName("headingFDHPanel")[0];
      heading.parentNode.removeChild(heading);
    }

    // Adding heading for the right bar
    var h4 = document.createElement("h4");
    h4.setAttribute("class", "headingFDHPanel");
    h4.innerHTML = "List of Librettos for years: " + "<b>" + yearSelected + "-" + (yearSelected + 22) + "</b>" + " in city: " + "<b>" + city_name + "</b>";
    h4.style.fontSize = "21px";
    h4.style.textAlign = "center";
    scrollTextPane.appendChild(h4);

    global_results.forEach(function (o) {
      if ((typeof o[YEAR_INDEX] !== 'string') && ((o[YEAR_INDEX] >= yearSelected && (o[YEAR_INDEX] <= yearSelected + 22))) && (o[CITY_INDEX] === city_name)) {
        var div = document.createElement("div");
        div.setAttribute("class", "w3-panel w3-blue w3-card-4");

        // Adding title pane
        var p_title = document.createElement("p");
        p_title.innerHTML = "Title";
        p_title.style.fontSize = "15px";

        var p_title_text = document.createElement("p");
        p_title_text.innerHTML = o[TITLE_INDEX];
        p_title_text.style.fontSize = "10px";

        // Adding year pane
        var p_title_year = document.createElement("p");
        p_title_year.innerHTML = "Year";
        p_title_year.style.fontSize = "15px";

        var p_title_year_text = document.createElement("p");
        p_title_year_text.innerHTML = o[YEAR_INDEX];
        p_title_year_text.style.fontSize = "10px";

        // Adding the paras to each child
        div.appendChild(p_title);
        div.appendChild(p_title_text);
        div.appendChild(p_title_year);
        div.appendChild(p_title_year_text);
        scrollTextPane.appendChild(div);
      }
    });
}

function plotIntensityMap(cityCount, subTheatres, yearSelected) {    
    // console.log(cityCount);
    Object.keys(cityCount).forEach(function(o){
        var lat = latLongMap[o][0];
        var long = latLongMap[o][1];
        // Adding a marker and an associated popup
        // Use circle marker to get the right radius
        var marker = L.circleMarker([lat, long], {color: 'grey', fillColor: 'rgb(123,61,63)', fillOpacity: 0.9, radius: 15}).addTo(mymap);
        marker._path.classList.add("cityMarker");
        marker.bindTooltip("Number of librettos: " + cityCount[o] + " in city of: " + o, {
            permanent: false, className: "my-label", offset: [0, 0]
        });

        // Get all the city markers
        var allCityMarkers = document.getElementsByClassName("cityMarker");

        marker.on('click', function(){
          var temp_city_name = this._tooltip._content.split(":")[2].replace(/\s+/, "");
          if(!zoomClick && ((temp_city_name !== lastCityClicked) || (lastCityClicked === null))) {
            hoverAndDoThings(this, yearSelected);
            lastCityClicked = temp_city_name;
          } else {
            // Zoom in into the point if you click again
            subTheatres[temp_city_name].forEach(function(coord) {
            var theatre_marker = L.circleMarker(
              coord, {color: 'skyblue', fillColor: 'black', 
              fillOpacity: 0.2, radius: 10}).addTo(mymap);
            theatre_marker._path.classList.add("theatreMarker"); // path.leaflet-interactive.theatreMarker
            theatre_marker.on('click', function(){
              revertBackToCityView(allCityMarkers);
              lastCityClicked = null;
            });
          });

            // Remove all the city markers since we are zoomed into a region
            for(i = 0; i < allCityMarkers.length; i++) {
              allCityMarkers[i].style.display = 'none';
            }
            mymap.flyTo([latLongMap[temp_city_name][0], latLongMap[temp_city_name][1]], 10);
            lastCityClicked = temp_city_name;
            zoomClick = false;
          }
        });
        mymap.addLayer(marker);
        markersCurrently.push(marker);
    });
}

function revertBackToCityView(allCityMarkers) {
  // Check if you are zoomed in or not, if you are zoom out
  var allTheatreMarkers = document.getElementsByClassName("theatreMarker");
  // pop off each of the theatre markers
  while (allTheatreMarkers.length > 0) {
    allTheatreMarkers[0].parentNode.removeChild(allTheatreMarkers[0]);
  }

  // Set the display back for all the city markers
  for(i = 0; i < allCityMarkers.length; i++) {
    allCityMarkers[i].style.display = 'initial';
  }
  mymap.flyTo([globalLat, globalLong], 6);
  zoomClick = false;
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

  var getIntensityCount = {};
  var getSubTheatres = {};
  global_results.forEach(function (o) {
    if ((typeof o[YEAR_INDEX] !== 'string') && ((o[YEAR_INDEX] >= dictYearsObj[value_selected]) && (o[YEAR_INDEX] <= dictYearsObj[value_selected] + 22))) {
        latLongMap[o[CITY_INDEX]] = [o[LAT_INDEX], o[LONG_INDEX]];
        getIntensityCount[o[CITY_INDEX]] = (getIntensityCount[o[CITY_INDEX]] || 0) + 1;
        getSubTheatres[o[CITY_INDEX]] = getSubTheatres[o[CITY_INDEX]] || [];
        getSubTheatres[o[CITY_INDEX]].push([o[THEATER_LAT], o[THEATER_LONG]]);
    }
  });

  plotIntensityMap(getIntensityCount, getSubTheatres, dictYearsObj[value_selected]);
}
