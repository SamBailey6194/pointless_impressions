// --- PURE FUNCTIONS (Defined first for Jest Testing) ---

/**
 * Renders a list of artwork cards into the designated container (#artwork-list).
 */
export function renderArtworkList(artworks) {
    const container = document.getElementById('artwork-list');
    if (!container) return;

    const isReady = typeof getCloudinaryUrl !== 'undefined' && typeof ARTWORK_DETAIL_BASE_PATH !== 'undefined';
    const clearURL = typeof ARTWORK_LIST_URL !== 'undefined' ? ARTWORK_LIST_URL : '/artworks/';

    let cardsHTML = '';
    if (artworks.length === 0) {
        cardsHTML = `
            <div class="hero min-h-[400px] col-span-full">
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
        artworks.forEach(artwork => {
            let imageHTML = '';
            const publicId = artwork.image_public_id; 
            const imageUrl = artwork.image_url;
            const altText = artwork.image_alt_text || artwork.name;
            
            // Priority 1: Use image_url if available (works for both local dev and CDN)
            if (imageUrl && imageUrl.trim() && imageUrl !== '/media/') {
                imageHTML = `<figure class="w-full"><img src="${imageUrl}" alt="${altText}" class="w-full h-64 object-cover" loading="lazy"></figure>`;
            } 
            // Priority 2: Use Cloudinary if public ID exists (for site assets)
            else if (publicId && isReady && typeof getCloudinaryUrl !== 'undefined') {
                const transformations = 'w_400,h_300,c_fill,f_auto,q_auto';
                const cloudinaryUrl = getCloudinaryUrl(publicId, transformations); 
                imageHTML = `<figure class="w-full"><img src="${cloudinaryUrl}" alt="${altText}" class="w-full h-64 object-cover" loading="lazy"></figure>`;
            }
            // Fallback: Use placeholder image
            else {
                imageHTML = `<figure class="w-full"><img src="/media/site_assets/noimage.png" alt="Placeholder" class="w-full h-64 object-cover"></figure>`;
            }
            
            // Handle artist info (may be undefined)
            let artistUrl = '#';
            let artistName = 'Unknown Artist';
            if (artwork.artist && artwork.artist.username) {
                const baseUrl = typeof ARTWORK_LIST_URL !== 'undefined' ? ARTWORK_LIST_URL : '/artworks/';
                artistUrl = `${baseUrl}?artist=${artwork.artist.username}`;
                artistName = artwork.artist.username;
            }
            const artistLine = artwork.artist && artwork.artist.username
                         ? `<p class="text-sm -mt-2 mb-2">
                             <a href="${artistUrl}" class="link link-hover">${artistName}</a>
                            </p>`
                : '';
            const detailUrl = (isReady && artwork.slug) ? ARTWORK_DETAIL_BASE_PATH + artwork.slug + '/' : '#'; 

            const bodyHTML = `
                <div class="card-body">
                    <h2 class="artwork-name card-title">${artwork.name}</h2>
                    ${artistLine}
                    <p class="artwork-description">${artwork.description}</p>
                    <div class="divider my-2"></div>
                    <p class="artwork-price text-2xl font-bold text-primary">£${artwork.price.toFixed(2)}</p>
                    
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
            cardsHTML += `<div class="artwork-card card shadow-xl hover:shadow-2xl transition-shadow" data-sku="${artwork.sku}">${imageHTML}${bodyHTML}</div>`;
        });
    }
    container.innerHTML = cardsHTML;
}

/** Filters artworks to show only those marked as available or in stock. */
export function filterAvailableArtworks(artworks) {
    return artworks.filter(a => a.is_available || a.is_in_stock);
}

/** Sorts artworks by price in ascending order. */
export function sortArtworksByPriceAsc(artworks) {
    return [...artworks].sort((a, b) => a.price - b.price); 
}

/** Sorts artworks by price in descending order. */
export function sortArtworksByPriceDesc(artworks) {
    return [...artworks].sort((a, b) => b.price - a.price); 
}

/** Sorts artworks by name in ascending order. */
export function sortArtworksByName(artworks) {
    return [...artworks].sort((a, b) => a.name.localeCompare(b.name));
}

/** Sort artworks by artist in ascending order. */
export function sortArtworksByArtist(artworks) {
    return [...artworks].sort((a, b) => {
        const nameA = a.artist?.username || a.name;
        const nameB = b.artist?.username || b.name;
        return nameA.localeCompare(nameB);
    });
}

// --- ENHANCEMENT STATE & LOGIC ---

let masterArtworkList = [];
let currentSortKey = 'price';
let currentSortDirection = 'asc';
let isEnhanced = false;

function toggleLoadingState(isLoading) {
    const container = document.getElementById('artwork-list');
    if (!container) return;
    
    if (isLoading) {
        container.classList.add('opacity-50', 'pointer-events-none');
    } else {
        container.classList.remove('opacity-50', 'pointer-events-none');
    }
}

/**
 * Applies current sorting state to the master list and triggers re-render.
 */
function applyStateAndRender() {
    let sortedList = [...masterArtworkList];

    switch (currentSortKey) {
        case 'price':
            sortedList = currentSortDirection === 'desc' 
                ? sortArtworksByPriceDesc(sortedList)
                : sortArtworksByPriceAsc(sortedList);
            break;
        case 'name':
            sortedList = sortArtworksByName(sortedList);
            break;
        case 'artist':
            sortedList = sortArtworksByArtist(sortedList);
            break;
        default:
            sortedList = sortArtworksByPriceAsc(sortedList);
    }

    renderArtworkList(sortedList);
}

/**
 * Updates button visual states to reflect current sort
 */
function updateSortButtonStates() {
    document.querySelectorAll('.sort-control[data-type="sort"]').forEach(btn => {
        const key = btn.getAttribute('data-sort-key');
        const direction = btn.getAttribute('data-sort-direction');
        if (String(key) === String(currentSortKey) && String(direction) === String(currentSortDirection)) {
            btn.classList.add('btn-active');
        } else {
            btn.classList.remove('btn-active');
        }
    });
}

/**
 * Handle sort button clicks with progressive enhancement
 */
function handleSortClick(event) {
    const button = event.target.closest('.sort-control');
    if (!button || button.dataset.type !== 'sort') return;

    if (!isEnhanced || masterArtworkList.length === 0) {
        return;
    }
    
    event.preventDefault();
    
    const key = button.dataset.sortKey;
    const direction = button.dataset.sortDirection;
    
    currentSortKey = key;
    currentSortDirection = direction;
    
    updateSortButtonStates();
    applyStateAndRender();

    const url = new URL(window.location);
    url.searchParams.set('sort', key);
    url.searchParams.set('direction', direction);
    window.history.pushState({}, '', url);
}

/**
 * Initialize sort state from URL parameters
 */
function initializeSortState() {
    const params = new URLSearchParams(window.location.search);
    currentSortKey = params.get('sort') || 'price';
    currentSortDirection = params.get('direction') || 'asc';
    
    updateSortButtonStates();
}

// -------------------------------------------------------------------
// INITIALIZATION AND EVENT HOOKS
// -------------------------------------------------------------------
function initArtworkListEnhancements() {
    initializeSortState();

    updateSortButtonStates();

    if (typeof window.ARTWORKS_JSON_DATA !== 'undefined' && window.ARTWORKS_JSON_DATA.length > 0) {
        masterArtworkList = window.ARTWORKS_JSON_DATA;
        isEnhanced = true;

        const params = new URLSearchParams(window.location.search);
        const hasActiveSorting = params.has('sort') || params.has('direction');
        
        if (hasActiveSorting) {
            applyStateAndRender();
        }
    }

    const controlsContainer = document.getElementById('controls');
    if (controlsContainer) {
        controlsContainer.addEventListener('click', handleSortClick);
    }
}

// -------------------------------------------------------------------
//  Price Filter Validation
//  Ensures min price is not negative, down button disabled at 0, and apply button disabled if min > max
// -------------------------------------------------------------------
function initPriceFilterValidation() {
    const minPriceInput = document.getElementById('min_price');
    const maxPriceInput = document.getElementById('max_price');
    const applyButton = document.getElementById('apply-filters');
    const form = applyButton?.closest('form');

    if (!minPriceInput || !maxPriceInput || !applyButton || !form) return;

    function validatePrices() {
        const minPrice = parseFloat(minPriceInput.value) || 0;
        const maxPrice = parseFloat(maxPriceInput.value) || 0;
        
        // Disable button if min > max (when both have values)
        if (minPriceInput.value && maxPriceInput.value && minPrice > maxPrice) {
            applyButton.disabled = true;
            applyButton.title = 'Min price cannot be greater than max price';
            applyButton.classList.add('btn-disabled');
        } else {
            applyButton.disabled = false;
            applyButton.title = '';
            applyButton.classList.remove('btn-disabled');
        }
    }

    // Validate on input change
    minPriceInput.addEventListener('change', validatePrices);
    minPriceInput.addEventListener('input', validatePrices);
    maxPriceInput.addEventListener('change', validatePrices);
    maxPriceInput.addEventListener('input', validatePrices);
    
    // Prevent form submission if invalid
    form.addEventListener('submit', function(e) {
        const minPrice = parseFloat(minPriceInput.value) || 0;
        const maxPrice = parseFloat(maxPriceInput.value) || 0;
        
        if (minPriceInput.value && maxPriceInput.value && minPrice > maxPrice) {
            e.preventDefault();
            alert('Min price cannot be greater than max price');
        }
    });

    // Initial validation
    validatePrices();
}

// -------------------------------------------------------------------
// Handle Artwork List Click
// -------------------------------------------------------------------
function handleArtworkListClick(event) {
  const button = event.target.closest('.add-to-cart-btn');
  
  if (!button) {
    return;
  }

  const { 
    artworkId, 
    artworkName, 
    artworkPrice, 
    artworkImage, 
    artworkQuantity 
  } = button.dataset;

  const framingOptions = JSON.parse(button.dataset.framingOptions || '[]');

  if (window.addToCartModal) {
    window.addToCartModal.init(
      artworkId,
      artworkName,
      parseFloat(artworkPrice),
      artworkImage,
      parseInt(artworkQuantity, 10),
      framingOptions
    );
  } else {
    alert('Error: Modal component is not loaded.');
  }
}


// -------------------------------------------------------------------
// DOMContentLoaded Initialization
// -------------------------------------------------------------------
document.addEventListener("DOMContentLoaded", function() {
    initArtworkListEnhancements();
    initPriceFilterValidation();

    const artworkListContainer = document.getElementById('artwork-list');
    if (artworkListContainer) {
      artworkListContainer.addEventListener('click', handleArtworkListClick);
    }
});