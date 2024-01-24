// Init global vars for elements
const layoutSwitch = document.getElementById('layoutSwitch');
const layoutSwitchDiv = layoutSwitch.parentElement
const editingContainer = document.getElementById('settings')
const combinedImageSpace = document.getElementById('combinedImageSpace');
const venueImage = document.getElementById('venueImage');
const businessName = document.getElementById('character-venue_name');
const imageFields = [document.getElementById('logo'), document.getElementById('venue'), document.getElementById('big_venue')];

let isBuisness;

function initMains(ib){
    isBuisness = ib;

    isBuisness === "True" ? layoutSwitchHandler(true) : layoutSwitchHandler(false);
    isBuisness === "True" ? layoutSwitch.checked : layoutSwitch.checked = false;
    layoutImageSwitcher(document.getElementById("layout").value == 2 ? true : false, imageFields);
}

// after DOM loaded, do
// document.addEventListener('load', function () {
//     // setup initial roleplay tab state and setting switch
//     "{{database.is_business}}" === "True" ? layoutSwitchHandler(true) : layoutSwitchHandler(false);
//     "{{database.is_business}}" === "True" ? layoutSwitch.checked = true : layoutSwitch.checked = false;
//     layoutImageSwitcher(document.getElementById("layout").value == 2 ? true : false, imageFields);
// });

// Send ajax to update db on switch state
layoutSwitch.addEventListener("change", function(){
    const switchState = layoutSwitchHandler(layoutSwitch.checked)
    $.ajax({
        url:"{{url_for('card_maker.swtich_rp_venue')}}",
        data: JSON.stringify({"state": switchState, "char_id": "{{database.char_id}}"}),
        type:"POST",
        contentType:"application/json"
    })
})

document.getElementById('layout').addEventListener('change', function () {
    const selectedLayout = this.value;
    // TODO set value of 1/2/3 or use actual values to display
    // TODO form field disabling due to switching
    switch (selectedLayout) {
        case '1':
            // Two Images, 375x375px logo, 650x375px small venue img, no h1 name
            document.getElementById("businessImg").classList.remove("d-none");
            document.getElementById("venueImg").classList.remove("d-none");
            document.getElementById("bigImg").classList.add("d-none");
            businessName.style.display = 'none'
            layoutImageSwitcher(false, imageFields)
            break;
        case '2':
            // No Image, 1140x375px Space for H1 Text
            document.getElementById("businessImg").classList.add("d-none");
            document.getElementById("venueImg").classList.add("d-none");
            document.getElementById("bigImg").classList.remove("d-none");
            businessName.style.display = 'block'
            layoutImageSwitcher(true, imageFields)
            break;
        case '3':
            // Two Images, 375x375px logo, 650x375px small venue img, includes h1 name
            document.getElementById("businessImg").classList.remove("d-none");
            document.getElementById("venueImg").classList.remove("d-none");
            document.getElementById("bigImg").classList.add("d-none");
            businessName.style.display = 'block'
            layoutImageSwitcher(false, imageFields)
            break;
        default:
            break;
    }
});

$("#portrait-form").submit(event=>{
    event.preventDefault();

    const editForm = new FormData(document.getElementById("portrait-form"))
    editForm.append("source", "summary")

    $.ajax({
        url: "{{url_for('card_maker.upload_portrait')}}",
        data: editForm,
        contentType: false,
        processData: false,
        type: "POST",
    }).done(data=>{
        imgurl=`${data["src"]}?timestamp=${Date.now()}`
        document.getElementById("avatar").src=imgurl
    })
})

$("#roleplay-settings").submit(event=>{
    event.preventDefault();

    const editForm = new FormData(document.getElementById("roleplay-settings"))
    editForm.append("source", "roleplay")

    $.ajax({
        url: "{{url_for('card_maker.upload_portrait')}}",
        data: editForm,
        contentType: false,
        processData: false,
        type: "POST",
    }).done(data=>{
        imgurl=`${data["src"]}?timestamp=${Date.now()}`
        document.getElementById("rp-avatar").src=imgurl
    })
})

$("#business-settings").submit(event=>{
    event.preventDefault();

    const editForm = new FormData(document.getElementById("business-settings"))

    $.ajax({
        url: "{{url_for('card_maker.upload_venue_images')}}",
        data: editForm,
        contentType: false,
        processData: false,
        type: "POST",
    }).done(data=>{
        if(data["uploaded"] === "two"){
            imgOneUrl = `${data["src"]["one"]}?timestamp=${Date.now()}`
            imgTwoUrl = `${data["src"]["two"]}?timestamp=${Date.now()}`
            document.getElementById("businessImg").src = imgOneUrl != null ? imgOneUrl : "https://via.placeholder.com/375x375"
            document.getElementById("venueImg").src = imgTwoUrl != null ? imgTwoUrl : "https://via.placeholder.com/650x375"
        }else{
            imgBigUrl = `${data["src"]}?timestamp=${Date.now()}`
            document.getElementById("bigImg").src = imgBigUrl != null ? imgBigUrl : "https://via.placeholder.com/1140x375"
        }
    })
})

function layoutSwitchHandler(state){
    let switchState = state;
    if(state){
        document.getElementById("roleplayingLayout").classList.add('d-none');
        document.getElementById("businessCardLayout").classList.remove('d-none');
        document.getElementById("roleplay-settings").classList.add('d-none');
        document.getElementById("business-settings").classList.remove('d-none');
        switchState = true;
    }else{
        document.getElementById("roleplayingLayout").classList.remove('d-none');
        document.getElementById("businessCardLayout").classList.add('d-none');
        document.getElementById("roleplay-settings").classList.remove('d-none');
        document.getElementById("business-settings").classList.add('d-none');
        switchState = false;
    }
    return switchState;
}

function saveChanges() {
    // Get the input element and its value
    const inputElement = document.querySelector('#additional-text textarea');
    const newText = inputElement.value;
    // Force limit the text to 200 characters to send
    const limitedText = newText.substring(0, 200);

    // jQuery for now to show it's working, gonna figure out async fetch later
    $.ajax({
        url: "{{url_for('card_maker.save_char_summary')}}",
        data: JSON.stringify({
            "char_id": "{{database.char_id}}",
            "summary": limitedText
        }),
        type: "POST",
        contentType: "application/json"
    }).done(data=>{
        const additionalTextDiv = document.getElementById('additional-text');
        additionalTextDiv.innerHTML = `<p>${data["summary"]}</p><span id='edit-summary-button' onclick='enableEditing()'>📝</span>`;
    })

    // Replace the input and button with the updated text
}

function enableEditing() {
    // Get the existing text content
    const existingText = document.querySelector('#additional-text p').innerText;

    // Create an input element for editing
    const inputElement = document.createElement('textarea');
    // inputElement.type = 'text';
    inputElement.value = existingText;
    inputElement.maxLength = 200; // Set the maximum character limit
    inputElement.classList.add("w-100")
    inputElement.classList.add("form-control")
    inputElement.style.height = "6.5rem"
    inputElement.style.fontSize = "1rem"
    inputElement.style.resize = "none"

    // Create a button for confirmation
    const confirmButton = document.createElement('button');
    confirmButton.innerText = 'Confirm';
    confirmButton.onclick = saveChanges;
    confirmButton.classList.add("form-control")
    confirmButton.classList.add("btn")
    confirmButton.classList.add("btn-primary")

    // Replace the existing div content with the input and button
    document.getElementById("edit-summary-button").remove()
    const additionalTextDiv = document.getElementById('additional-text');
    additionalTextDiv.innerHTML = ''; // Clear existing content
    additionalTextDiv.appendChild(inputElement);
    additionalTextDiv.appendChild(confirmButton);

    // Focus on the input field
    inputElement.focus();
}

function layoutImageSwitcher(state, images){
    // state bool is for big image, two images is inversed
    images.forEach(ele=>{
        if(state) {
            if(ele.id === "big_venue"){
                ele.removeAttribute("disabled")
            }else{
                ele.setAttribute("disabled", true)
            }
        }else{
            if(ele.id === "big_venue"){
                ele.setAttribute("disabled", true)
            } else{
                ele.removeAttribute("disabled")
            }
        }
    })
}

function twoImages(row){
    let logoDiv = document.createElement("div")
    let venueDiv = document.createElement("div")
    let logoImg = document.createElement("img")
    let venueImg = document.createElement("img")

    logoDiv.classList.add("col-md-5")
    venueDiv.classList.add("col-md-7")
    venueDiv.classList.add("text-end")
    
    logoImg.id = "businessImg"
    venueImg.id = "venueImg"

    logoImg.src = "https://via.placeholder.com/375x375"
    venueImg.src = "https://via.placeholder.com/650x375"
    logoImg.classList.add("img-fluid")
    venueImg.classList.add("img-fluid")
    
    logoDiv.appendChild(logoImg)
    venueDiv.appendChild(venueImg)
    row.appendChild(logoDiv)
    row.appendChild(venueDiv)
}