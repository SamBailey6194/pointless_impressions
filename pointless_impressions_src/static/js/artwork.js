(() => {
  // pointless_impressions_src/theme/static_src/src/js/artwork.js
  function renderArtworkList(artworks) {
    const container = document.getElementById("artwork-list");
    if (!container) return;
    const isReady = typeof getCloudinaryUrl !== "undefined" && typeof ARTWORK_DETAIL_BASE_PATH !== "undefined";
    const clearURL = "/artworks/";
    container.innerHTML = "";
    if (artworks.length === 0) {
      container.classList.remove("grid", "grid-cols-1", "md:grid-cols-2", "lg:grid-cols-3", "gap-6");
      container.classList.add("flex", "justify-center", "items-center", "min-h-[400px]");
      container.innerHTML = `
            <div class="hero w-full">
                <div class="hero-content text-center mx-auto">
                    <div class="max-w-md">
                        <i class="fa-solid fa-palette text-6xl text-base-content mb-4"></i>
                        <h2 class="text-3xl font-bold">No artworks found.</h2>
                        <p class="py-6 text-base-content/70">Try adjusting your filters or search terms to find what you're looking for.</p>
                        <a href="${clearURL}" class="clear-filters btn btn-primary">
                        <i class="fa-solid fa-refresh"></i> Clear Filters
                        </a>
                    </div>
                </div>
            </div>`;
    } else {
      container.classList.remove("flex", "justify-center", "items-center", "min-h-[400px]");
      container.classList.add("grid", "grid-cols-1", "md:grid-cols-2", "lg:grid-cols-3", "gap-6");
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
        container.appendChild(card);
      });
    }
  }
  function filterAvailableArtworks(artworks) {
    return artworks.filter((a) => a.is_available || a.is_in_stock);
  }
  function sortArtworksByPriceAsc(artworks) {
    return [...artworks].sort((a, b) => a.price - b.price);
  }
  function sortArtworksByName(artworks) {
    return [...artworks].sort((a, b) => a.name.localeCompare(b.name));
  }
  function sortArtworksByArtist(artworks) {
    return [...artworks].sort((a, b) => {
      const nameA = a.artist?.username || a.name;
      const nameB = b.artist?.username || b.name;
      return nameA.localeCompare(nameB);
    });
  }
  var masterArtworkList = [];
  var currentSortKey = "price";
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
    let sortedList;
    switch (currentSortKey) {
      case "price":
        sortedList = sortArtworksByPriceAsc(filteredList);
        break;
      case "name":
        sortedList = sortArtworksByName(filteredList);
        break;
      case "artist":
        sortedList = sortArtworksByArtist(filteredList);
        break;
      default:
        sortedList = filteredList;
    }
    if (currentSortDirection === "desc") {
      sortedList.reverse();
    }
    renderArtworkList(sortedList);
  }
  function handleControlClick(event) {
    const button = event.target.closest(".sort-control");
    if (!button) return;
    const controlType = button.dataset.type;
    if (controlType === "sort") {
      const key = button.dataset.sortKey;
      const direction = button.dataset.sortDirection;
      updateSortStateAndStyles(key, direction, button);
      applyStateAndRender();
    }
  }
  function updateSortStateAndStyles(key, direction, activeButton) {
    currentSortKey = key;
    currentSortDirection = direction;
    document.querySelectorAll('.sort-control[data-type="sort"]').forEach((btn) => {
      btn.classList.remove("btn-active-sort");
      btn.classList.add("btn-outline");
    });
    activeButton.classList.remove("btn-outline");
    activeButton.classList.add("btn-active-sort");
  }
  function initArtworkListEnhancements() {
    const hasServerFilters = window.location.search.length > 0;
    if (hasServerFilters) {
      return;
    }
    fetchArtworksFromAPI().then((artworks) => {
      if (artworks.length > 0) {
        const availableCheckbox2 = document.getElementById("available-only-checkbox");
        if (availableCheckbox2 && availableCheckbox2.checked) {
          isFilterActive = true;
        }
        const defaultSortButton = document.getElementById("sort-lowest-price");
        if (defaultSortButton) {
          updateSortStateAndStyles("price", "asc", defaultSortButton);
          applyStateAndRender();
        }
      }
    });
    const controlsContainer = document.getElementById("controls");
    if (controlsContainer) {
      controlsContainer.addEventListener("click", handleControlClick);
    }
    const availableCheckbox = document.getElementById("available-only-checkbox");
    if (availableCheckbox) {
      availableCheckbox.addEventListener("change", function(event) {
        isFilterActive = event.target.checked;
        applyStateAndRender();
      });
    }
  }
  document.addEventListener("DOMContentLoaded", initArtworkListEnhancements);
})();
//# sourceMappingURL=artwork.js.map
