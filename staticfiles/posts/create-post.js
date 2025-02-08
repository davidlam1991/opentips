// Google Places
$.getScript( "https://maps.googleapis.com/maps/api/js?key=" + google_api_key + "&libraries=places")
.done(function( script, textStatus ) {
    google.maps.event.addDomListener(window, "load", searchAddressBox);
});

function searchAddressBox() {
    // Autocomplete for restaurant name
    var restaurantNameField = new google.maps.places.Autocomplete(
        document.getElementById('id_restaurant_name'),
        {
            type: ['establishment'],
            componentRestrictions: {'country': ['ca']}
        });

    // Listen for the place change event on the restaurant name field
    restaurantNameField.addListener('place_changed', function () {
        var place = restaurantNameField.getPlace();

        // Extract the address from the selected place
        if (place.address_components) {
            var restaurantName = place.name;
            var address = place.formatted_address;

            // Set the restaurant name field to the name only
            document.getElementById('id_restaurant_name').value = restaurantName;

            // Set the address in the address field
            document.getElementById('id_address').value = address;
        }
    });
}


// Date Format MM/YYY
document.addEventListener("DOMContentLoaded", function() {
    const dateInput = document.getElementById('id_date');

    if (dateInput) {
        dateInput.addEventListener('input', function(e) {
            const value = e.target.value.replace(/\D/g, ''); // Remove all non-digit characters
            if (value.length >= 2) {
                e.target.value = value.slice(0, 2) + '/' + value.slice(2, 6);
            } else {
                e.target.value = value;
            }
        });
    }
});


// Control Hidden
document.addEventListener('DOMContentLoaded', function() {
    const tipsSituation = document.getElementById('id_tips_situation');
    const tipsSitDetailContainer = document.getElementById('tips_sit_detail_container');

        function toggleTipsDetail() {
            if (tipsSituation.value === 'C') {
                tipsSitDetailContainer.classList.remove('hidden');
            } else {
                tipsSitDetailContainer.classList.add('hidden');
            }
        }

        tipsSituation.addEventListener('change', toggleTipsDetail);

        toggleTipsDetail();

})