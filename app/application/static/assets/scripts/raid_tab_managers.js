document.addEventListener('DOMContentLoaded', function () {
    var initialTab = new bootstrap.Tab(document.getElementById('ultimates-tab'));
    initialTab.show(); // Activate the Ultimates tab

    var ultimatesTab = new bootstrap.Tab(document.getElementById('the-omega-protocol-tab'));
    ultimatesTab.show(); // Activate the Omega Protocol subtab
});

// TODO onclick for each major tab to enable each subtab
document.getElementById("ultimates-tab").addEventListener("click", function(){
    var ultimatesTab = new bootstrap.Tab(document.getElementById('the-omega-protocol-tab'));
    ultimatesTab.show(); // Activate the Omega Protocol subtab
})

document.getElementById("endwalker-tab").addEventListener("click", function(){
    var endwalkerTab = new bootstrap.Tab(document.getElementById("anabaseios-tab"));
        endwalkerTab.show()
})

document.getElementById("shadowbringers-tab").addEventListener("click", function(){
    var endwalkerTab = new bootstrap.Tab(document.getElementById("eden-promise-tab"));
        endwalkerTab.show()
})

document.getElementById("stormblood-tab").addEventListener("click", function(){
    var endwalkerTab = new bootstrap.Tab(document.getElementById("alphascape-tab"));
        endwalkerTab.show()
})

    document.getElementById("heavensward-tab").addEventListener("click", function(){
    var endwalkerTab = new bootstrap.Tab(document.getElementById("alexander:-the-creator-tab"));
        endwalkerTab.show()
})