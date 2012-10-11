$(document).ready(function() {
var mapquest_osm = new L.TileLayer("http://{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png", {maxZoom: 14, minZoom: 1, attribution: 'Data, imagery and map information provided by <a href="http://open.mapquest.co.uk" target="_blank">MapQuest</a>, <a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> and contributors, <a href=\"http://creativecommons.org/licenses/by-sa/2.0/\" target=\"_blank\">CC-BY-SA</a>', subdomains: ["otile1","otile2","otile3","otile4"]});
        var map = new L.Map('map', {center: new L.LatLng(50, 2), zoom: 5, layers: [mapquest_osm]});
    $.getJSON('js/data.json',function(data) {
      $.each(data, function(key, val) {
      	var latlng = new L.LatLng(val["location"]["lat"],val["location"]["lng"]);
      	var marker = new L.Marker(latlng);
		var mitglieder = parseInt(val["mitglieder"]);
		var mitgliederText = "Mitglied";
		if(mitglieder > 1) {
			mitgliederText += "er";
		}
      	marker.bindPopup(val["mitglieder"]+" "+mitgliederText+" in "+val["city"]);
      	map.addLayer(marker);
      });
      });
        
});