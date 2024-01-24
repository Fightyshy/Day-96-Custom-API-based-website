//housing type switcher consts and init lets
const apartmentSwitch = document.getElementById("is_apartment");
const wardField = document.getElementById("housing_ward");
const plotField = document.getElementById("ward_plot");
const apartmentField = document.getElementById("apartment_num");

let apartmentState;
// let char_id;

function initVenueModals(as, ci){
    apartmentState = as;
    char_id = ci;

    apartmentState==true?housingTypeSwitcher(true):housingTypeSwitcher(false);
}
document.getElementById("VenueNameAndTaglineModal").addEventListener("show.bs.modal", async event=>{
    const res = await fetch(`http://localhost:5000/rp-venue-names?char_id=${char_id}`)
    const data = await res.json();
    if(data["status"] === "ok"){
        populateFields(data);
    } else{
        // bad response send bootstrap alert to top of modal
    }
});


document.getElementById("venuenameform").addEventListener("submit", async event=>{
    event.preventDefault();

    const req = responseMaker(`http://localhost:5000/rp-venue-names?char_id=${char_id}`, document.getElementById("venuenameform"));
    const res = await fetch(req);
    const data = await res.json();

    // check if response ok and data ok
    if(res.ok){
        const errorState = serverValidateForm(data, document.getElementById("venuenameform"));
        if(errorState){
            // Hide/Reveal based on alias response
            updatePageFields(data);
            modalCloseOnSuccess("VenueNameAndTaglineModal");
        }
    } else{
        // server error/bad response
    }
});

    
document.getElementById("VenueStaffDetailsModal").addEventListener("show.bs.modal", async event=>{
    const res = await fetch(`http://localhost:5000/rp-venue-staff?char_id=${char_id}`)
    const data = await res.json();
    if(data["status"] === "ok"){
        populateFields(data);
    } else{
        // bad response send bootstrap alert to top of modal
    }
});

document.getElementById("venuestaffform").addEventListener("submit", async event=>{
    event.preventDefault();

    const req = responseMaker(`http://localhost:5000/rp-venue-staff?char_id=${char_id}`, document.getElementById("venuestaffform"));
    const res = await fetch(req);
    const data = await res.json();

    // check if response ok and data ok
    if(res.ok){
        const errorState = serverValidateForm(data, document.getElementById("venuestaffform"));
        if(errorState){
            // Hide/Reveal based on alias response
            updatePageFields(data);
            modalCloseOnSuccess("VenueStaffDetailsModal");
        }
    } else{
        // server error/bad response
    }
});

document.getElementById("VenueContactAndSocialsModal").addEventListener("show.bs.modal", async event=>{
    const res = await fetch(`http://localhost:5000/rp-venue-contacts?char_id=${char_id}`)
    const data = await res.json();
    if(data["status"] === "ok"){
        populateFields(data);
    } else{
        // bad response send bootstrap alert to top of modal
    }
});

document.getElementById("venuecontactform").addEventListener("submit", async event=>{
    event.preventDefault();

    const req = responseMaker(`http://localhost:5000/rp-venue-contacts?char_id=${char_id}`, document.getElementById("venuecontactform"));
    const res = await fetch(req);
    const data = await res.json();

    // check if response ok and data ok
    if(res.ok){
        const errorState = serverValidateForm(data, document.getElementById("venuecontactform"));
        if(errorState){
            // Hide/Reveal based on alias response
            updatePageFields(data);
            modalCloseOnSuccess("VenueContactAndSocialsModal");
        }
    } else{
        // server error/bad response
    }
});

document.getElementById("is_apartment").addEventListener("change", event=>{
    housingTypeSwitcher(apartmentSwitch.checked)
});