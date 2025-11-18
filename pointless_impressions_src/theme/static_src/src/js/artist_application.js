document.addEventListener("DOMContentLoaded", function () {
    const socialLinksContainer = document.getElementById("social-links-container");
    const addSocialLinkButton = document.getElementById("add-social-link");

    // Clear any existing social link rows on page load
    socialLinksContainer.innerHTML = "";

    // Function to create a new social link row
    function createSocialLinkRow() {
        const row = document.createElement("div");
        row.classList.add("social-link-row", "flex", "gap-4", "mb-4");

        const platformInput = document.createElement("input");
        platformInput.type = "text";
        platformInput.name = "platform";
        platformInput.placeholder = "Platform";
        platformInput.classList.add("custom-input", "w-1/3");

        const urlInput = document.createElement("input");
        urlInput.type = "url";
        urlInput.name = "url";
        urlInput.placeholder = "URL";
        urlInput.classList.add("custom-input", "w-2/3");

        const removeButton = document.createElement("button");
        removeButton.type = "button";
        removeButton.textContent = "Remove";
        removeButton.classList.add("btn", "btn-ghost", "btn-outline", "remove-social");

        // Add event listener to remove button
        removeButton.addEventListener("click", function () {
            socialLinksContainer.removeChild(row);
        });

        row.appendChild(platformInput);
        row.appendChild(urlInput);
        row.appendChild(removeButton);

        return row;
    }

    // Add event listener to the Add Social Link button
    addSocialLinkButton.addEventListener("click", function () {
        const newRow = createSocialLinkRow();
        socialLinksContainer.appendChild(newRow);
    });
});