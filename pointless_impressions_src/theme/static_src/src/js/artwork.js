// pointless_impressions/pointless_impressions_src/theme/static_src/src/js/artwork.js

export function renderArtworkList(artworks) {
    // TODO: implement rendering
    return null;
}

export function filterAvailableArtworks(artworks) {
    // TODO: implement filtering
    return [];
}

export function sortArtworksByPrice(artworks) {
    // TODO: implement sorting
    return artworks;
}

// Wait for the DOM to be ready
document.addEventListener("DOMContentLoaded", () => {
    const artworks = [
        { name: "Sunset", price: 199.99, description: "A beautiful sunset over the mountains.", is_available: true, sku: "SUNSET123" },
        { name: "Starry Night", price: 299.99, description: "A night sky full of color and dots.", is_available: false, sku: "STARRY123" },
    ];

    // Currently just calls the stub, will not render anything
    renderArtworkList(artworks);
});
