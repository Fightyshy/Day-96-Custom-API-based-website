//Scripts - RP field handling
let hookCounter = "{{database.roleplaying.hooks|length}}"==="0" ? 1 : parseInt("{{database.roleplaying.hooks|length}}");
// https://stackoverflow.com/questions/40006617/get-count-of-list-items-that-meet-a-condition-with-jinja2
// list|select element on condition type == "pos"/"neg"|cast list|length
// set 1 if returns 0, otherwise it breaks add/remove mechanism
let posCounter = "{{database.roleplaying.traits|selectattr('type','equalto','pos')|list|length}}"==="0" ? 1 : parseInt("{{database.roleplaying.traits|selectattr('type','equalto','pos')|list|length}}");
let negCounter = "{{database.roleplaying.traits|selectattr('type','equalto','neg')|list|length}}"==="0" ? 1 : parseInt("{{database.roleplaying.traits|selectattr('type','equalto','neg')|list|length}}");

//housing type switcher consts
const apartmentSwitch = document.getElementById("is_apartment");
const wardField = document.getElementById("housing_ward");
const plotField = document.getElementById("ward_plot");
const apartmentField = document.getElementById("apartment_num");
// set init switch state
"{{database.business.venue_address.is_apartment}}"==true?housingTypeSwitcher(true):housingTypeSwitcher(false);

document.addEventListener("DOMContentLoaded", ()=>{

    initHookForm();
    initTraitForm();
    
    // TODO initial add hook fields

    //rp hook field adders/removers
    document.getElementById("addHook").addEventListener("click", (event)=>{
        event.preventDefault();
        if(hookCounter < 3){
            hookCounter++;
            let revealedHookTitle = document.getElementById(`hook${hookCounter}_title`);
            let revealedHookBody = document.getElementById(`hook${hookCounter}_body`);
            let revealedHookTitleLabel = document.getElementById(`hook${hookCounter}_title_label`);
            let revealedHookBodyLabel = document.getElementById(`hook${hookCounter}_body_label`);

            revealedHookTitle.classList.remove("d-none");
            revealedHookTitle.classList.remove("is-valid");
            revealedHookBody.classList.remove("d-none");
            revealedHookBody.classList.remove("is-valid");

            revealedHookTitleLabel.classList.remove("d-none");
            revealedHookBodyLabel.classList.remove("d-none");
        }
    });

    document.getElementById("removeHook").addEventListener("click", (event)=>{
        event.preventDefault();
        if(hookCounter > 1){
            let revealedHookTitle = document.getElementById(`hook${hookCounter}_title`);
            let revealedHookBody = document.getElementById(`hook${hookCounter}_body`);
            let revealedHookTitleLabel = document.getElementById(`hook${hookCounter}_title_label`);
            let revealedHookBodyLabel = document.getElementById(`hook${hookCounter}_body_label`);
            
            revealedHookTitle.classList.add("d-none");
            revealedHookBody.classList.add("d-none");
            revealedHookTitle.classList.remove("is-valid");
            revealedHookTitle.classList.remove("is-invalid");
            revealedHookBody.classList.remove("is-valid");
            revealedHookBody.classList.remove("is-invalid");
            revealedHookTitle.value="";
            revealedHookBody.value="";
            revealedHookTitleLabel.classList.add("d-none");
            revealedHookBodyLabel.classList.add("d-none");
            hookCounter--;
        }
    });

    //rp trait field adders/removers
    //positive traits
    document.getElementById("addPosTrait").addEventListener("click", (event)=>{
        event.preventDefault();

        if(posCounter < 5){
            posCounter++;

            let revealedPosTrait = document.getElementById(`pos_trait${posCounter}`);
            let revealedPosTraitLabel = document.getElementById(`pos_trait${posCounter}_label`);

            revealedPosTrait.classList.remove("d-none");
            revealedPosTrait.classList.remove("is-valid");
            revealedPosTraitLabel.classList.remove("d-none");
        }
    });

    document.getElementById("removePosTrait").addEventListener("click", (event)=>{
        event.preventDefault();

        if(posCounter > 1){
            let revealedPosTrait = document.getElementById(`pos_trait${posCounter}`);
            let revealedPosTraitLabel = document.getElementById(`pos_trait${posCounter}_label`);

            revealedPosTrait.classList.add("d-none");
            revealedPosTrait.classList.remove("is-valid");
            revealedPosTrait.value = ""
            revealedPosTraitLabel.classList.add("d-none");

            posCounter--;
        }
    });

    //negative traits
    document.getElementById("addNegTrait").addEventListener("click", (event)=>{
        event.preventDefault();

        if(negCounter < 5){
            negCounter++;

            let revealedNegTrait = document.getElementById(`neg_trait${negCounter}`);
            let revealedNegTraitLabel = document.getElementById(`neg_trait${negCounter}_label`);

            revealedNegTrait.classList.remove("d-none");
            revealedNegTrait.classList.remove("is-valid");
            revealedNegTraitLabel.classList.remove("d-none");
        }
    });

    document.getElementById("removeNegTrait").addEventListener("click", (event)=>{
        event.preventDefault();

        if(negCounter > 1){
            let revealedNegTrait = document.getElementById(`neg_trait${negCounter}`);
            let revealedNegTraitLabel = document.getElementById(`neg_trait${negCounter}_label`);

            revealedNegTrait.classList.add("d-none");
            revealedNegTrait.classList.remove("is-valid");
            revealedNegTrait.value = ""
            revealedNegTraitLabel.classList.add("d-none");

            negCounter--;
        }
    });

    //TODO handle submit ajax
    //TODO update hooks with response from server

    document.getElementById("RPCharNicknamesModal").addEventListener("show.bs.modal", event=>{
        $.get(
            "{{url_for('card_maker.save_roleplaying_alias', char_id=database.char_id)}}",
            data=>{
                if(data.status==="ok"){
                    populateFields(data);
                }
            }
        );
    });

    document.getElementById("nicknames-form").addEventListener("submit", event=>{
        event.preventDefault();
        const formData = new FormData(document.getElementById("nicknames-form"));
        formData.append("char_id", "{{database.char_id}}");

        $.ajax({
            url:"{{url_for('card_maker.save_roleplaying_alias')}}",
            data: formData,
            contentType: false,
            processData: false,
            type:"POST",
            success: data=>{
                serverValidateForm(data, document.getElementById("nicknames-form"));
                updatePageFields(data);
                modalCloseOnSuccess("RPCharNicknamesModal")
            },
        });
    });

    document.getElementById("RPCharSummaryModal").addEventListener("show.bs.modal", event=>{
        $.get(
            "{{url_for('card_maker.save_roleplaying_summary', char_id=database.char_id)}}",
            data=>{
                if(data.status==="ok"){
                    populateFields(data);
                }
            }
        );
    })

    document.getElementById("charsummary").addEventListener("submit", event=>{
        event.preventDefault();

        const formData = new FormData(document.getElementById("charsummary"));
        formData.append("char_id", "{{database.char_id}}");
        $.ajax({
            url: "{{url_for('card_maker.save_roleplaying_summary')}}",
            data: formData,
            contentType: false,
            processData: false,
            type: "POST",
            success: data=>{
                // Do validation and handle data
                const errorState = serverValidateForm(data, document.getElementById("charsummary"));
                if(errorState){
                    updatePageFields(data);
                    modalCloseOnSuccess("RPCharSummaryModal");
                }
            }
        });
    });

    document.getElementById("RPSocialsModal").addEventListener("show.bs.modal", event=>{
        $.get(
            "{{url_for('card_maker.save_roleplaying_socials', char_id=database.char_id)}}",
            data=>{
                if(data.status==="ok"){
                    populateFields(data);
                }
            }
        );
    });

    document.getElementById("rpsocialsform").addEventListener("submit", event=>{
        event.preventDefault();

        const formData = new FormData(document.getElementById("rpsocialsform"));
        formData.append("char_id", "{{database.char_id}}")
        $.ajax({
            url: "{{url_for('card_maker.save_roleplaying_socials')}}",
            data: formData,
            contentType: false,
            processData: false,
            type: "POST",
            success: data=>{
                const errorState = serverValidateForm(data, document.getElementById("rpsocialsform"));
                if(errorState){
                    updatePageFields(data);
                    modalCloseOnSuccess("RPSocialsModal");
                }
            }
        });
    });

    document.getElementById("RPAboutMeModal").addEventListener("show.bs.modal", event=>{
        $.get(
            "{{url_for('card_maker.save_roleplaying_about_me', char_id=database.char_id)}}",
            data=>{
                if(data.status==="ok"){
                    populateFields(data);
                }
            }
        );
    })

    document.getElementById("rpaboutmeform").addEventListener("submit", event=>{
        event.preventDefault();

        const formData = new FormData(document.getElementById("rpaboutmeform"));
        formData.append("char_id", "{{database.char_id}}");
        $.ajax({
            url: "{{url_for('card_maker.save_roleplaying_about_me')}}",
            data: formData,
            contentType: false,
            processData: false,
            type: "POST",
            success: data=>{
                const errorState = serverValidateForm(data, document.getElementById("rpaboutmeform"));
                if(errorState){
                    updatePageFields(data);
                    modalCloseOnSuccess("RPAboutMeModal");
                }
            }
        });
    });

    document.getElementById("RPCharQuoteModal").addEventListener("show.bs.modal", event=>{
        $.get(
            "{{url_for('card_maker.save_roleplaying_quote', char_id=database.char_id)}}",
            data=>{
                if(data.status==="ok"){
                    populateFields(data);
                }
            }
        );
    });

    document.getElementById("charquoteform").addEventListener("submit", event=>{
        event.preventDefault();

        const formData = new FormData(document.getElementById("charquoteform"));
        formData.append("char_id", "{{database.char_id}}")
        $.ajax({
            url: "{{url_for('card_maker.save_roleplaying_quote')}}",
            data: formData,
            contentType: false,
            processData: false,
            type: "POST",
            success: data=>{
                const errorState = serverValidateForm(data, document.getElementById("charquoteform"));
                if(errorState){
                    updatePageFields(data);
                    modalCloseOnSuccess("RPCharQuoteModal");
                }
            }
        });
    });

    // WARN/BUG - Certain action sequences with the HookModal and TraitsModal seem to "break" the modal display
    // afterwards. Backdrop will be summoned while modal remains hidden.
    // WARN/TODO - All modal show.bs.modal calls seem to run twice. Using once: true seems to break them
    // TODO - read up on how js event lifecycle should work.
    document.getElementById("RPHooksModal").addEventListener("show.bs.modal", event=>{
        $.get(
            "{{url_for('card_maker.save_roleplaying_hooks', char_id=database.char_id)}}",
            data=>{
                if(data.status==="ok"){
                    //Forcing modal to show via js seems to work
                    //Form request data is not compromised
                    let toOpen = bootstrap.Modal.getInstance("#RPHooksModal");
                    toOpen.show();
                    populateFields(data);
                }
            }
        );
    });

    document.getElementById("hookForm").addEventListener("submit", event=>{
        event.preventDefault();

        const formData = new FormData(document.getElementById("hookForm"));
        formData.append("char_id", "{{database.char_id}}")
        $.ajax({
            url: "{{url_for('card_maker.save_roleplaying_hooks')}}",
            data: formData,
            contentType: false,
            processData: false,
            type: "POST",
            success: data=>{
                const errorState = serverValidateForm(data, document.getElementById("hookForm"));
                if(errorState){
                    const keys = Object.keys(data).filter(k=>k!=="status");
                    let hookList = document.getElementById("hooks-list");
                    hookList.innerHTML=""; //delete
                    for(let i=0; i<keys.length/2; i++){
                        let listField = document.createElement("li");
                        let hookTitle = document.createElement("h4");
                        let hookBody = document.createElement("span");
                        hookTitle.innerHTML = `hook${i+1}_title`==="hook1_title" ? `${data[`hook${i+1}_title`]} <span data-bs-toggle="modal" data-bs-target="#RPHooksModal">📝</span></h4>` : data[`hook${i+1}_title`];
                        hookBody = data[`hook${i+1}_body`];
                        listField.append(hookTitle);
                        listField.append(hookBody);
                        hookList.append(listField);
                    }
                    hookCounter = keys.length/2
                    initHookForm();
                    modalCloseOnSuccess("RPHooksModal");
                }

            }
        });
    });

    document.getElementById("RPTraitsModal").addEventListener("show.bs.modal", event=>{
        $.get(
            "{{url_for('card_maker.save_roleplaying_traits', char_id=database.char_id)}}",
            data=>{
                if(data.status==="ok"){
                    //Forcing modal to show via js seems to work
                    //Form request data is not compromised
                    let toOpen = bootstrap.Modal.getInstance("#RPTraitsModal");
                    toOpen.show();
                    populateFields(data);
                }
            }
        );
    });

    document.getElementById("traitForm").addEventListener("submit", event=>{
        event.preventDefault();

        const formData = new FormData(document.getElementById("traitForm"));
        formData.append("char_id", "{{database.char_id}}")
        $.ajax({
            url: "{{url_for('card_maker.save_roleplaying_traits')}}",
            data: formData,
            contentType: false,
            processData: false,
            type: "POST",
            success: data=>{
                const errorState = serverValidateForm(data, document.getElementById("traitForm"));
                if(errorState){
                    let posNo = 0;
                    let negNo = 0;
                    let posList = document.getElementById("positive-traits-list");
                    let negList = document.getElementById("negative-traits-list");
                    posList.innerHTML = "";
                    negList.innerHTML = "";

                    Object.keys(data).filter(k=>k!=="status").forEach(k=>{
                        let listField = document.createElement("li");
                        if(k.slice(0,3) === "pos"){
                            listField.innerText = data[k];
                            posList.appendChild(listField);
                            posNo++;
                        } else{
                            listField.innerText = data[k];
                            negList.appendChild(listField);
                            negNo++;
                        }
                    })

                    posCounter = posNo;
                    negCounter = negNo;
                    initTraitForm();
                    modalCloseOnSuccess("RPTraitsModal")
                }
            }
        });
    });

    document.getElementById("VenueNameAndTaglineModal").addEventListener("show.bs.modal", event=>{
        $.get(
            "{{url_for('card_maker.save_venue_names', char_id=database.char_id)}}",
            data=>{
                if(data.status==="ok"){
                    populateFields(data);
                }
            }
        );
    });


    document.getElementById("venuenameform").addEventListener("submit", event=>{
        event.preventDefault();

        const formData = new FormData(document.getElementById("venuenameform"));
        formData.append("char_id", "{{database.char_id}}");
        $.ajax({
            url: "{{url_for('card_maker.save_venue_names')}}",
            data: formData,
            contentType: false,
            processData: false,
            type: "POST",
            success: data=>{
                const errorState = serverValidateForm(data, document.getElementById("venuenameform"));
                if(errorState){
                    updatePageFields(data);
                    modalCloseOnSuccess("VenueNameAndTaglineModal");
                }
            }
        });
    });

    
    document.getElementById("VenueStaffDetailsModal").addEventListener("show.bs.modal", event=>{
        $.get(
            "{{url_for('card_maker.save_venue_staff_details', char_id=database.char_id)}}",
            data=>{
                if(data.status==="ok"){
                    populateFields(data);
                }
            }
        );
    });

    document.getElementById("venuestaffform").addEventListener("submit", event=>{
        event.preventDefault();

        const formData = new FormData(document.getElementById("venuestaffform"));
        formData.append("char_id", "{{database.char_id}}");
        $.ajax({
            url: "{{url_for('card_maker.save_venue_staff_details')}}",
            data: formData,
            contentType: false,
            processData: false,
            type: "POST",
            success: data=>{
                const errorState = serverValidateForm(data, document.getElementById("venuestaffform"));
                if(errorState){
                    updatePageFields(data);
                    modalCloseOnSuccess("VenueStaffDetailsModal");
                }
            }
        });
    });

    document.getElementById("VenueContactAndSocialsModal").addEventListener("show.bs.modal", event=>{
        $.get(
            "{{url_for('card_maker.save_business_contacts', char_id=database.char_id)}}",
            data=>{
                if(data.status=="ok"){
                    populateFields(data);
                    data["is_apartment"] == true ? housingTypeSwitcher(true) : housingTypeSwitcher(false);
                }
            }
        )
    });

    document.getElementById("venuecontactform").addEventListener("submit", event=>{
        event.preventDefault();

        const formData = new FormData(document.getElementById("venuecontactform"));
        formData.append("char_id", "{{database.char_id}}");

        $.ajax({
            url: "{{url_for('card_maker.save_business_contacts')}}",
            data: formData,
            contentType: false,
            processData: false,
            type: "POST",
            success: data=>{
                const errorState = serverValidateForm(data, document.getElementById("venuecontactform"));
                if(errorState){
                    if(data.status==="ok"){
                        updatePageFields(data);
                        modalCloseOnSuccess("VenueContactAndSocialsModal");
                    }
                }
            }
        })
    });

    document.getElementById("is_apartment").addEventListener("change", event=>{
        housingTypeSwitcher(apartmentSwitch.checked)
    });

});

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