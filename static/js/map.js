function initMap() {
        var myLatLng = { lat: 50.79583018533471, lng: -0.6933898249468823 };

        var map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: myLatLng,
        });

        var marker = new google.maps.Marker({
        position: myLatLng,
        map: map,
        title: "Our Location",
        });
}

var contentString = "<h1>Our Loacation</h1>";

var infowindow = new google.maps.InfoWindow({
        content: contentString,
});

marker.addListener("click", function () {
        infowindow.open(map, marker);
});