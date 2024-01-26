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
    isBuisness === "True" ? layoutSwitch.checked = true : layoutSwitch.checked = false;
    layoutImageSwitcher(document.getElementById("layout").value == 2 ? true : false, imageFields);
}

// Send ajax to update db on switch state
layoutSwitch.addEventListener("change", async event=>{
    const switchState = layoutSwitchHandler(layoutSwitch.checked)
    const response = await fetch(`http://localhost:5000/rp-venue-mode?char_id=${char_id}`,{
        method: "POST",
        headers:{
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "state": switchState,
            "char_id": char_id
        })
    })
    const error = response.error
    // TODO show error as dismissable toast, advise user to try again or contact admin
})

document.getElementById('layout').addEventListener('change', function () {
    const selectedLayout = this.value;
    // TODO set value of 1/2/3 or use actual values to display
    // TODO form field disabling due to switching
    switch (selectedLayout) {
        case '1':
            // Two Images, 375x375px logo, 650x375px small venue img, no h1 name
            document.getElementById("logoImg").classList.remove("d-none");
            document.getElementById("venueImg").classList.remove("d-none");
            document.getElementById("big_venueImg").classList.add("d-none");
            businessName.style.display = 'none'
            layoutImageSwitcher(false, imageFields)
            break;
        case '2':
            // No Image, 1140x375px Space for H1 Text
            document.getElementById("logoImg").classList.add("d-none");
            document.getElementById("venueImg").classList.add("d-none");
            document.getElementById("big_venueImg").classList.remove("d-none");
            businessName.style.display = 'block'
            layoutImageSwitcher(true, imageFields)
            break;
        case '3':
            // Two Images, 375x375px logo, 650x375px small venue img, includes h1 name
            document.getElementById("logoImg").classList.remove("d-none");
            document.getElementById("venueImg").classList.remove("d-none");
            document.getElementById("big_venueImg").classList.add("d-none");
            businessName.style.display = 'block'
            layoutImageSwitcher(false, imageFields)
            break;
        default:
            break;
    }
});

// TODO image uploaders using validators
// TODO Error message format, should be
// Error code, Error message, Error explaination (in human)
document.getElementById("portrait-form").addEventListener("submit", async event=>{
    event.preventDefault();

    const req = responseMaker(`http://localhost:5000/character/portrait?char_id=${char_id}`, document.getElementById("portrait-form"));
    const response = await fetch(req);
    const data = await response.json();
    
    if(serverValidateForm(data, document.getElementById("portrait-form"))){
        imgurl=`${data["image"]}?timestamp=${Date.now()}`
        document.getElementById("avatar").src=imgurl
        document.getElementById("summary_portrait").value = "";
    } else{
        // TODO error response as toast
    }
});

document.getElementById("roleplay-settings").addEventListener("submit", async event=>{
    event.preventDefault();

    const req = responseMaker(`http://localhost:5000/character/portrait?char_id=${char_id}`, document.getElementById("roleplay-settings"));
    const response = await fetch(req);
    const data = await response.json();

    if(serverValidateForm(data, document.getElementById("roleplay-settings"))){
        imgurl=`${data["image"]}?timestamp=${Date.now()}`;
        document.getElementById("rp-avatar").src=imgurl;
        document.getElementById("rp_portrait").value = "";
    } else{
        // TODO error response as toast
    }
});

document.getElementById("business-settings").addEventListener("submit", async event=>{
    event.preventDefault();

    const req = responseMaker(`http://localhost:5000/character/venue?char_id=${char_id}`, document.getElementById("business-settings"))
    const response = await fetch(req);
    const data = await response.json();
    if(serverValidateForm(data, document.getElementById("business-settings"))){
        Object.entries(data["images"]).forEach(image=>{
            // [key, img src]
            let [key, source] = image;
            document.getElementById(`${key}Img`).src = source
        });
    } else{
        // TODO error response as toast
    }
});

document.getElementById("edit-summary-button").addEventListener("click", enableEditing);

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

async function saveChanges() {
    // Select input element and sanitise length to 200
    const inputElement = document.querySelector('#additional-text textarea');
    const newText = inputElement.value;
    const limitedText = newText.substring(0, 200);

    // form request and get response
    const request = new Request(`http://localhost:5000/char-summary?char_id=${char_id}`, {
        method: "POST",
        headers:{
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "summary": limitedText
        })
    });
    const response = await fetch(request);
    const data = await response.json();

    if (response.ok){
        const additionalTextDiv = document.getElementById('additional-text');
        additionalTextDiv.innerHTML = `<p>${data["summary"]}</p><span id='edit-summary-button' onclick='enableEditing()'>📝</span>`;
    }
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
        // May not work on some browsers, but our target is modern browsers atm
        ele.value = ""
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