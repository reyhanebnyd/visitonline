// detail.js

// Track the selected time slot
let selectedSlot = null;

// Function to handle slot reservation
function reserveTime(full_slot_start, element) {
    // Deselect previously selected slot
    if (selectedSlot) {
        document.querySelector(`.selected`).classList.remove('selected');
    }
    selectedSlot = full_slot_start;
    // Highlight the newly selected slot
    element.classList.add('selected');
    // Show the reserve button
    document.getElementById("reserveButton").style.display = 'block';
}

// Function to confirm reservation and submit the form
function confirmReservation() {
    if (selectedSlot) {
        // Set the value of the hidden input with the selected slot
        document.getElementById('slotInput').value = selectedSlot;

        // Submit the reservation form
        document.getElementById('reservationForm').submit();
    } else {
        // Alert if no slot is selected
        alert("Please select a time slot to reserve.");
    }
}
