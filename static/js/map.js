function initMap() {

        var myLatLng = { lat: 50.877196177898774, lng: -1.3280979847009355 };

        var map = new google.maps.Map(document.getElementById("map"), {
        zoom: 10,
        center: myLatLng,
})

        var marker = new google.maps.Marker({
        position: myLatLng,
        map: map,
        title: "Our Location",
});

        var infowindow = new google.maps.InfoWindow({
        content: "Our Sports Complex, Satchell Ln, Hamble-le-Rice, Southampton SO31 4NE",
        });

        marker.addListener("mouseover", function () {
        infowindow.open(map, marker);
});

        marker.addListener("mouseout", function () {
        infowindow.close();
});
}
