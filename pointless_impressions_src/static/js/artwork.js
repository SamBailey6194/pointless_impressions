(() => {
  // pointless_impressions_src/theme/static_src/src/js/artwork.js
  function renderArtworkList(artworks) {
    const container = document.getElementById("artwork-list");
    if (!container) return;
    container.innerHTML = "";
    const newGrid = document.createElement("div");
    newGrid.className = "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6";
    const isReady = typeof getCloudinaryUrl !== "undefined" && typeof ARTWORK_DETAIL_BASE_PATH !== "undefined";
    if (artworks.length === 0) {
      newGrid.innerHTML = `
            <div class="hero min-h-[400px] bg-base-200 rounded-box col-span-full">
                <div class="hero-content text-center">
                    <div class="max-w-md">
                        <i class="fa-solid fa-palette text-6xl text-base-content/20 mb-4"></i>
                        <h2 class="text-3xl font-bold">No results found.</h2>
                        <p class="py-6 text-base-content/70">Try clearing your client-side filters.</p>
                    </div>
                </div>
            </div>`;
    }
    artworks.forEach((artwork) => {
      const card = document.createElement("div");
      card.className = "artwork-card card bg-base-100 shadow-xl hover:shadow-2xl transition-shadow";
      card.setAttribute("data-sku", artwork.sku);
      let imageHTML = "";
      const publicId = artwork.image_public_id;
      const altText = artwork.image_alt_text || artwork.name;
      if (publicId && isReady) {
        const transformations = "w_400,h_300,c_fill,f_auto,q_auto";
        const imageUrl = getCloudinaryUrl(publicId, transformations);
        imageHTML = `<figure><img src="${imageUrl}" alt="${altText}" class="w-full h-64 object-cover"></figure>`;
      } else {
        imageHTML = `<figure><div class="bg-base-300 h-64 w-full flex items-center justify-center"><i class="fa-solid fa-image text-base-content/20 text-5xl"></i></div></figure>`;
      }
      const detailUrl = isReady && artwork.slug ? ARTWORK_DETAIL_BASE_PATH + artwork.slug + "/" : "#";
      const bodyHTML = `
            <div class="card-body">
                <h2 class="artwork-name card-title">${artwork.name}</h2>
                <p class="artwork-description text-base-content/70">${artwork.description}</p>
                <div class="divider my-2"></div>
                <p class="artwork-price text-2xl font-bold text-primary">\xA3${artwork.price.toFixed(2)}</p>
                
                <div class="card-actions justify-between items-center mt-4">
                    ${artwork.is_in_stock ? `
                        <button class="add-to-cart btn btn-primary btn-sm">
                            <i class="fa-solid fa-cart-plus"></i> Add to Cart
                        </button>
                        <a href="${detailUrl}" class="btn btn-outline btn-sm"><i class="fa-solid fa-eye"></i> Details</a>
                    ` : `
                        <span class="sold-out badge badge-error">Sold Out</span>
                        <a href="${detailUrl}" class="btn btn-outline btn-sm"><i class="fa-solid fa-eye"></i> Details</a>
                    `}
                </div>
            </div>`;
      card.innerHTML = imageHTML + bodyHTML;
      newGrid.appendChild(card);
    });
    container.appendChild(newGrid);
  }
  function filterAvailableArtworks(artworks) {
    return artworks.filter((a) => a.is_available || a.is_in_stock);
  }
  function sortArtworksByPrice(artworks) {
    return [...artworks].sort((a, b) => a.price - b.price);
  }
  var masterArtworkList = [];
  var currentSortDirection = "asc";
  var isFilterActive = false;
  function toggleLoadingState(isLoading) {
    const container = document.getElementById("artwork-list");
    if (!container) return;
    if (isLoading) {
      container.classList.add("opacity-50", "pointer-events-none");
    } else {
      container.classList.remove("opacity-50", "pointer-events-none");
    }
  }
  function fetchArtworksFromAPI() {
    if (typeof ARTWORK_API_URL === "undefined") {
      console.error("ARTWORK_API_URL is missing.");
      return Promise.resolve([]);
    }
    toggleLoadingState(true);
    return fetch(ARTWORK_API_URL).then((response) => {
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      return response.json();
    }).then((data) => {
      masterArtworkList = data;
      toggleLoadingState(false);
      return data;
    }).catch((error) => {
      console.error("Error loading artworks via API:", error);
      toggleLoadingState(false);
      document.getElementById("artwork-list").innerHTML = '<p class="text-center text-error p-8">Could not load dynamic artwork data.</p>';
      return [];
    });
  }
  function applyStateAndRender() {
    let filteredList = [...masterArtworkList];
    if (isFilterActive) {
      filteredList = filterAvailableArtworks(filteredList);
    }
    filteredList = sortArtworksByPrice(filteredList);
    if (currentSortDirection === "desc") {
      filteredList.reverse();
    }
    renderArtworkList(filteredList);
  }
  function initArtworkListEnhancements() {
    const sortButton = document.getElementById("sort-price");
    const filterButton = document.getElementById("filter-available");
    fetchArtworksFromAPI().then((artworks) => {
      if (artworks.length > 0) {
        applyStateAndRender();
      }
    });
    if (sortButton) {
      sortButton.addEventListener("click", () => {
        currentSortDirection = currentSortDirection === "asc" ? "desc" : "asc";
        const icon = sortButton.querySelector("i");
        if (icon) {
          icon.className = currentSortDirection === "asc" ? "fa-solid fa-sort-amount-up" : "fa-solid fa-sort-amount-down";
        }
        applyStateAndRender();
      });
    }
    if (filterButton) {
      filterButton.addEventListener("click", () => {
        isFilterActive = !isFilterActive;
        if (isFilterActive) {
          filterButton.classList.remove("btn-outline");
          filterButton.classList.add("btn-success");
        } else {
          filterButton.classList.remove("btn-success");
          filterButton.classList.add("btn-outline");
        }
        applyStateAndRender();
      });
    }
  }
  document.addEventListener("DOMContentLoaded", initArtworkListEnhancements);
})();
//# sourceMappingURL=artwork.js.map
