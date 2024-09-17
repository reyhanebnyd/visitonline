let selectedSlot = null;  

function reserveTime(full_slot_start, element) {   
    if (selectedSlot) {  
        document.querySelector(`.selected`).classList.remove('selected');  
    }  
    selectedSlot = full_slot_start;  
    // Highlight the selected slot  
    element.classList.add('selected');  
    // Show the reserve button  
    document.getElementById("reserveButton").style.display = 'block';  
}  

function confirmReservation() {  
    if (selectedSlot) {  
// Set the value of the hidden input with the selected slot
        document.getElementById('slotInput').value = selectedSlot;

// Submit the form
        document.getElementById('reservationForm').submit();
        window.location.href = `/payment?slot=${encodeURIComponent(selectedSlot)}&doctor_id=${encodeURIComponent(document.getElementById('doctorIdInput').value)}`;
    } else {  
        alert("Please select a time slot to reserve.");  
    }  
}