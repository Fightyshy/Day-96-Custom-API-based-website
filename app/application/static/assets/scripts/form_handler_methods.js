
const responseMaker = (url, form) =>{
    const formData = new FormData(form);
    formData.append("char_id", char_id);
    const req = new Request(url, {
        method: "POST",
        body: formData,
        "Content-Type": false,
        "Process-Data": false
    });
    return req;
}

function housingTypeSwitcher(switchState){
    if(switchState){
        plotField.classList.add("d-none");
        plotField.labels[0].classList.add("d-none");
        plotField.classList.remove("is-valid");
        plotField.classList.remove("is-invalid");
        apartmentField.classList.remove("d-none");
        apartmentField.labels[0].classList.remove("d-none");
        apartmentField.classList.remove("is-valid");
        apartmentField.classList.remove("is-invalid");
        apartmentSwitch.checked = true;
    } else{
        plotField.classList.remove("d-none");
        plotField.labels[0].classList.remove("d-none");
        plotField.classList.remove("is-valid");
        plotField.classList.remove("is-invalid");
        apartmentField.classList.add("d-none");
        apartmentField.labels[0].classList.add("d-none");
        apartmentField.classList.remove("is-valid");
        apartmentField.classList.remove("is-invalid");
        apartmentSwitch.checked = false;
    }
}

function initHookForm(){
    // initial form state
    for(let i=0;i<hookCounter;i++){
        document.getElementById(`hook${i+1}_title`).classList.remove("d-none");
        document.getElementById(`hook${i+1}_body`).classList.remove("d-none");
        document.getElementById(`hook${i+1}_title_label`).classList.remove("d-none");
        document.getElementById(`hook${i+1}_body_label`).classList.remove("d-none");
    }
}

function initTraitForm(){
    // It's literally 10 data points at worst, just loop twice
    for(let i=0;i<posCounter;i++){
        document.getElementById(`pos_trait${i+1}`).classList.remove("d-none");
        document.getElementById(`pos_trait${i+1}_label`).classList.remove("d-none");
    }
    for(let j=0;j<negCounter;j++){
        document.getElementById(`neg_trait${j+1}`).classList.remove("d-none");
        document.getElementById(`neg_trait${j+1}_label`).classList.remove("d-none");
    }
}

function updatePageFields(data){
    //populate spans
    console.log(data);
    Object.keys(data).filter(k=>k!=="status").forEach(k => {
        // TODO empty field handling, both here and in jinja render
        data[k]===""?undefined:document.getElementById(`character-${k}`).innerText = data[k];
    });
}

// helper funcs for modals
// https://stackoverflow.com/questions/71903920/how-to-hide-bootstrap-5-modal-on-button-click
function modalCloseOnSuccess(modal){
    let toClose = bootstrap.Modal.getInstance(`#${modal}`);
    setTimeout(()=>{
        // close (hide) modal
        toClose.hide();
        // Manually remove static backdrop
        document.getElementsByClassName("modal-backdrop")[0].remove();
    }, 1500);
}

// BUG sometimes when forms are submit too fast it will load the modal properly
function populateFields(data){
    Object.keys(data).filter(k=>k!=="status").forEach(k=>{
        //reset field state
        let formField = document.getElementById(k);
        let errorFeedback = document.getElementById(`${k}-invalid-feedback`);
        formField.classList.remove("is-valid");
        formField.classList.remove("is-invalid");
        formField.parentElement.contains(errorFeedback)?errorFeedback.remove():undefined;
        // populate
        formField.value = data[k];
    });
}

function serverValidateForm(data, form){
    // data status can only be error or ok
    // TODO proper error coding and handle malformed data
    // TODO user-friendly response to server-error
        // FORMAT -> Error type, Error code, Error desc, render as dismissable field on top of modal
    if(data.status === "error"){
        [...form.elements].filter(input=> input.tagName === "TEXTAREA" || input.type === "text" || input.type === "number" || input.tagName === "SELECT").forEach(input=>{
            let formField =document.getElementById(input.id)
            let errorFeedback = document.getElementById(`${input.id}-invalid-feedback`);
            if(data.errors[input.id] !== undefined){
                formField.parentElement.contains(errorFeedback)?errorFeedback.remove():undefined;
                let invalidFeedback = document.createElement("div");

                invalidFeedback.id = `${input.id}-invalid-feedback`;
                invalidFeedback.classList.add("invalid-feedback");
                invalidFeedback.innerText = data.errors[input.id][0];

                formField.classList.add("is-invalid");
                formField.parentElement.appendChild(invalidFeedback);
            } else{
                formField.classList.remove("is-invalid");
                formField.classList.add("is-valid");
                formField.parentElement.contains(errorFeedback)?errorFeedback.remove():undefined;
            }
        });
        return false;
    } else{
        // Go through form and make everything valid, remove feedback if present
        [...form.elements].filter(input=> input.tagName === "TEXTAREA" || input.type === "text" || input.type === "number" || input.tagName === "SELECT").forEach(input=>{
            let formField = document.getElementById(input.id);
            let errorFeedback = document.getElementById(`${input.id}-invalid-feedback`);
            formField.classList.remove("is-invalid");
            formField.parentElement.contains(errorFeedback)?errorFeedback.remove():undefined;
            formField.classList.add("is-valid");
        });
        return true
    }
}