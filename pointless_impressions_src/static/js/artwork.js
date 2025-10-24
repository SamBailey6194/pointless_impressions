(() => {
  // pointless_impressions_src/theme/static_src/src/js/artwork.js
  function renderArtworkList(artworks) {
    return null;
  }
  function filterAvailableArtworks(artworks) {
    return [];
  }
  function sortArtworksByPrice(artworks) {
    return artworks;
  }
  document.addEventListener("DOMContentLoaded", () => {
    const artworks = [
      { name: "Sunset", price: 199.99, description: "A beautiful sunset over the mountains.", is_available: true, sku: "SUNSET123" },
      { name: "Starry Night", price: 299.99, description: "A night sky full of color and dots.", is_available: false, sku: "STARRY123" }
    ];
    renderArtworkList(artworks);
  });
})();
//# sourceMappingURL=artwork.js.map
