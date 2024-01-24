//Scripts - RP field handling
// init modal lets
let hookCounter;
let posCounter;
let negCounter;
let char_id;

// Basically a constructor
function initRPModals (hk, pc, nc, ci){
    // Init vars
    hookCounter = hk === "0" ? 1 : Number(hk);
    posCounter = pc === "0" ? 1 : Number(pc);
    negCounter = nc === "0" ? 1 : Number(nc);
    char_id = ci

    // Set states
    initHookForm();
    initTraitForm();
};
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

// TODO refactor to fetch api
document.getElementById("RPCharNicknamesModal").addEventListener("show.bs.modal", async event=>{
    const res = await fetch(`http://localhost:5000/rp-alias?char_id=${char_id}`)
    const data = await res.json();
    if(data["status"] === "ok"){
        populateFields(data);
    } else{
        // bad response send bootstrap alert to top of modal
    }
});

document.getElementById("nicknames-form").addEventListener("submit", async event=>{
    event.preventDefault();

    const req = responseMaker(`http://localhost:5000/rp-alias?char_id=${char_id}`, document.getElementById("nicknames-form"));
    const res = await fetch(req);
    const data = await res.json();

    // check if response ok and data ok
    if(res.ok){
        const errorState = serverValidateForm(data, document.getElementById("nicknames-form"));
        if(errorState){
            // Hide/Reveal based on alias response
            data["alias"].length >= 1 ? document.getElementById("character-alias").parentElement.classList.remove("d-none") : document.getElementById("character-alias").parentElement.classList.add("d-none");
            updatePageFields(data);
            modalCloseOnSuccess("RPCharNicknamesModal");
        }
    } else{
        // server error/bad response
    }
});

document.getElementById("RPCharSummaryModal").addEventListener("show.bs.modal", async event=>{
    const res = await fetch(`http://localhost:5000/rp-summary?char_id=${char_id}`)
    const data = await res.json();
    if(data["status"] === "ok"){
        populateFields(data);
    } else{
        // bad response send bootstrap alert to top of modal
    }
})

document.getElementById("charsummary").addEventListener("submit", async event=>{
    event.preventDefault();
    const req = responseMaker(`http://localhost:5000/rp-summary?char_id=${char_id}`, document.getElementById("charsummary"));
    const res = await fetch(req);
    const data = await res.json();

    // check if response ok and data ok
    if(res.ok){
        const errorState = serverValidateForm(data, document.getElementById("charsummary"));
        if(errorState){
            updatePageFields(data);
            modalCloseOnSuccess("RPCharSummaryModal");
        }
    } else{
        // server error/bad response
    }
});

document.getElementById("RPSocialsModal").addEventListener("show.bs.modal", async event=>{
    const res = await fetch(`http://localhost:5000/rp-socials?char_id=${char_id}`)
    const data = await res.json();
    if(data["status"] === "ok"){
        populateFields(data);
    } else{
        // bad response send bootstrap alert to top of modal
    }
});

document.getElementById("rpsocialsform").addEventListener("submit", async event=>{
    event.preventDefault();
    const req = responseMaker(`http://localhost:5000/rp-socials?char_id=${char_id}`, document.getElementById("rpsocialsform"));
    const res = await fetch(req);
    const data = await res.json();

    // check if response ok and data ok
    if(res.ok){
        const errorState = serverValidateForm(data, document.getElementById("rpsocialsform"));
        if(errorState){
            updatePageFields(data);
            modalCloseOnSuccess("RPSocialsModal");
        }
    } else{
        // server error/bad response
    }
});

document.getElementById("RPAboutMeModal").addEventListener("show.bs.modal", async event=>{
    const res = await fetch(`http://localhost:5000/rp-about-me?char_id=${char_id}`)
    const data = await res.json();
    if(data["status"] === "ok"){
        populateFields(data);
    } else{
        // bad response send bootstrap alert to top of modal
    }
})

document.getElementById("rpaboutmeform").addEventListener("submit", async event=>{
    event.preventDefault();
    const req = responseMaker(`http://localhost:5000/rp-about-me?char_id=${char_id}`, document.getElementById("rpaboutmeform"));
    const res = await fetch(req);
    const data = await res.json();

    // check if response ok and data ok
    if(res.ok){
        const errorState = serverValidateForm(data, document.getElementById("rpaboutmeform"));
        if(errorState){
            updatePageFields(data);
            modalCloseOnSuccess("RPAboutMeModal");
        }
    } else{
        // server error/bad response
    }
});

document.getElementById("RPCharQuoteModal").addEventListener("show.bs.modal", async event=>{
    const res = await fetch(`http://localhost:5000/rp-char-quote?char_id=${char_id}`)
    const data = await res.json();
    if(data["status"] === "ok"){
        populateFields(data);
    } else{
        // bad response send bootstrap alert to top of modal
    }
});

document.getElementById("charquoteform").addEventListener("submit", async event=>{
    event.preventDefault();
    const req = responseMaker(`http://localhost:5000/rp-char-quote?char_id=${char_id}`, document.getElementById("charquoteform"));
    const res = await fetch(req);
    const data = await res.json();

    // check if response ok and data ok
    if(res.ok){
        const errorState = serverValidateForm(data, document.getElementById("charquoteform"));
        if(errorState){
            updatePageFields(data);
            modalCloseOnSuccess("RPCharQuoteModal");
        }
    } else{
        // server error/bad response
    }
});

// WARN/BUG - Certain action sequences with the HookModal and TraitsModal seem to "break" the modal display
// afterwards. Backdrop will be summoned while modal remains hidden.
// WARN/TODO - All modal show.bs.modal calls seem to run twice. Using once: true seems to break them
// TODO - read up on how js event lifecycle should work.
document.getElementById("RPHooksModal").addEventListener("show.bs.modal", async event=>{
    const res = await fetch(`http://localhost:5000/rp-hooks?char_id=${char_id}`)
    const data = await res.json();
    if(data["status"] === "ok"){
        populateFields(data);
    } else{
        // bad response send bootstrap alert to top of modal
    }
});

document.getElementById("hookForm").addEventListener("submit", async event=>{
    event.preventDefault();
    const req = responseMaker(`http://localhost:5000/rp-hooks?char_id=${char_id}`, document.getElementById("hookForm"));
    const res = await fetch(req);
    const data = await res.json();

    // check if response ok and data ok
    if(res.ok){
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
    else{
        // server error/bad response
    }
});

document.getElementById("RPTraitsModal").addEventListener("show.bs.modal", async event=>{
    const res = await fetch(`http://localhost:5000/rp-traits?char_id=${char_id}`)
    const data = await res.json();
    if(data["status"] === "ok"){
        populateFields(data);
    } else{
        // bad response send bootstrap alert to top of modal
    }
});

// TODO fix empty input or enforce field required input if revealed
document.getElementById("traitForm").addEventListener("submit", async event=>{
    event.preventDefault();
    const req = responseMaker(`http://localhost:5000/rp-traits?char_id=${char_id}`, document.getElementById("traitForm"));
    const res = await fetch(req);
    const data = await res.json();

    if(res.ok){
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
                } else if(k.slice(0,3) === "neg"){
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
    } else{
        // bad response send bootstrap alert to top of modal
    }
});
