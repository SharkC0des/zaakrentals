
const hamburger = document.getElementById('hamburger');
const menubar = document.getElementById('menubar');

hamburger.addEventListener('click', () => {
  hamburger.classList.toggle('hamburger-active');
  menubar.classList.toggle('active');
});


window.addEventListener('resize', () => {
  if (window.innerWidth > 790) {
    hamburger.classList.remove('hamburger-active');
    menubar.classList.remove('active');
  }
});


document.querySelectorAll('#menubar a').forEach(link => {
  link.addEventListener('click', () => {
    hamburger.classList.remove('hamburger-active');
    menubar.classList.remove('active');
  });
});


// A static list of locations
const ALL_LOCATIONS = [
    { name: "New York City, NY", id: "nyc" },
    { name: "Los Angeles, CA", id: "la" },
    { name: "Syracuse, NY", id: "syr" },
    { name: "Miami International Airport (MIA)", id: "mia" },
    // ... more locations
];

const locationInput = document.getElementById('location-input');
const suggestionsList = document.getElementById('suggestions');
const selectedLocationValue = document.getElementById('selected-location-value');

locationInput.addEventListener('input', function() {
    const query = this.value.toLowerCase().trim();
    suggestionsList.innerHTML = ''; // Clear old suggestions

    if (query.length === 0) {
        return; // Don't show suggestions if input is empty
    }

    // 1. Filter the list
    const filteredLocations = ALL_LOCATIONS.filter(location => 
        location.name.toLowerCase().includes(query)
    );

    // 2. Display the suggestions
    filteredLocations.forEach(location => {
        const li = document.createElement('li');
        li.textContent = location.name;
        li.dataset.id = location.id; // Store the ID for submission
        li.classList.add('suggestion-item');
        
        // 3. Attach a click handler
        li.addEventListener('click', function() {
            // Fill the input with the selected location's name
            locationInput.value = location.name;
            // Store the ID in the hidden field for form submission
            selectedLocationValue.value = location.id;
            // Hide the suggestions list
            suggestionsList.innerHTML = '';
        });
        
        suggestionsList.appendChild(li);
    });
});

// Optional: Hide suggestions when clicking outside
document.addEventListener('click', (e) => {
    if (!locationInput.contains(e.target) && !suggestionsList.contains(e.target)) {
        suggestionsList.innerHTML = '';
    }
});



// Function to show the date and time popup for either 'start' or 'end'
function showDateTimePopup(type) {
    document.getElementById('date-time-popup').classList.add('show');
    document.getElementById('popup-header-title').innerText = `Select ${type.charAt(0).toUpperCase() + type.slice(1)} Date and Time`;
    
    // Store the current type (start or end) so we know which field to update
    window.currentPopupType = type;
}

// Function to close the popup
function closePopup() {
    document.getElementById('date-time-popup').classList.remove('show');
}

// Function to select the date and time from the popup and update the relevant field
function selectDateTime() {
    const selectedDate = document.getElementById('popup-date').value;
    const selectedTime = document.getElementById('popup-time').value;

    if (selectedDate && selectedTime) {
        // Format the selected date and time to display as "MM/DD/YYYY 10:00 AM"
        const formattedDateTime = formatDateTime(selectedDate, selectedTime);

        // Update the correct field based on the type (start or end)
        if (window.currentPopupType === 'start') {
            document.getElementById('start-date').value = formattedDateTime;
            document.getElementById('start-time').value = selectedTime;
        } else if (window.currentPopupType === 'end') {
            document.getElementById('end-date').value = formattedDateTime;
            document.getElementById('end-time').value = selectedTime;
        }
    }

    closePopup();
}

// Helper function to format the date and time
function formatDateTime(date, time) {
    const dateObj = new Date(date);
    const hours = parseInt(time.split(':')[0]);
    const minutes = time.split(':')[1];
    const ampm = hours >= 12 ? 'PM' : 'AM';

    const formattedDate = `${dateObj.getMonth() + 1}/${dateObj.getDate()}/${dateObj.getFullYear()} ${hours % 12}:${minutes} ${ampm}`;
    return formattedDate;
}
