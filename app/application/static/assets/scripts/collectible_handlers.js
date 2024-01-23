// Initialize Bootstrap tooltips
document.addEventListener('DOMContentLoaded', function () {
    var subcategoryLinks = document.querySelectorAll('.subcat-tabs');

    subcategoryLinks.forEach(function (link) {
        link.addEventListener('click', function () {
            var subcategory = this.getAttribute('data-subcategory');
            var achievements = this.getAttribute('data-achievements');
            subcategoryLinks.forEach((subcat)=>{
                subcat.classList.remove("active")
            })
            this.classList.add("active")
            loadSubcategoryContent(subcategory, achievements);
        });
    });

    // Load content for the selected subcategory
    function loadSubcategoryContent(subcategory, achievements) {
        var achievementContent = document.getElementById('achievementContent');
        achievementContent.innerHTML = ''; // Clear previous content
        achievementsToJSON = JSON.parse(achievements)

        // Iterate through achievements and append content for each
        achievementsToJSON.forEach(function (achievement) {
            var achievementRow = document.createElement('div');
            achievementRow.className = 'row achievement-row pb-2';

            // First column (40x40 thumbnail)
            var thumbnailColumn = document.createElement('div');
            thumbnailColumn.className = 'col-md-1 px-0';
            thumbnailColumn.innerHTML = `<img src="${achievement.icon}" alt="Achievement Thumbnail" class="achievement-icon">`;

            // Second column (Achievement details)
            var detailsColumn = document.createElement('div');
            detailsColumn.className = 'col';
            detailsColumn.innerHTML = `
                <div class="row">
                    <div class="col px-0">
                        <span class="achievement-patch">(${achievement.patch}) </span><span class="achievement-name">${achievement.name}</span> - <span class="achievement-points">${achievement.points}</span>
                    </div>
                </div>
                <div class="row">
                    <div class="col px-0">
                        <p class="achievement-description">${achievement.description}</p>
                    </div>
                </div>
            `;

            achievementHR = document.createElement("hr")
            achievementHR.className = "my-2"

            achievementRow.appendChild(thumbnailColumn);
            achievementRow.appendChild(detailsColumn);
            achievementRow.appendChild(achievementHR)

            achievementContent.appendChild(achievementRow);
        });
    }

    // Set initial content for the first subcategory
    var initialSubcategory = subcategoryLinks[0].getAttribute('data-subcategory');
    var initialAchievements = subcategoryLinks[0].getAttribute('data-achievements');
    document.getElementById(subcategoryLinks[0].getAttribute("id")).classList.add("active")
    loadSubcategoryContent(initialSubcategory, initialAchievements);
});

var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
});