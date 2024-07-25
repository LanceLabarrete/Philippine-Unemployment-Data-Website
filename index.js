document.addEventListener('DOMContentLoaded', function() {
    const regionSelect = document.getElementById('region-select');
    const regionFocus = document.getElementById('region-focus');

    regionSelect.addEventListener('change', function() {
        const selectedRegion = this.value;
        // Add your logic to update the map and unemployment data based on the selected region
        console.log(`Selected region: ${selectedRegion}`);
    });

    regionFocus.addEventListener('change', function() {
        const selectedFocus = this.value;
        // Add your logic to update the map and unemployment data based on the selected focus
        console.log(`Selected focus: ${selectedFocus}`);
    });
});
