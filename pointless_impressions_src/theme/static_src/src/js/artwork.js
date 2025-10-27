// --- PURE FUNCTIONS (Defined first for Jest Testing) ---

/**
 * Renders a list of artwork cards into the designated container (#artwork-list).
 * This function completely replaces the SSR content when called.
 */
function renderArtworkList(artworks) {
    const container = document.getElementById('artwork-list');
    if (!container) return;
    
    // Clear the existing SSR content
    container.innerHTML = ''; 

    // Create a new grid div to hold the dynamically generated cards
    const newGrid = document.createElement('div');
    newGrid.className = 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6';

    // Check for necessary globals (defined in your template)
    const isReady = typeof getCloudinaryUrl !== 'undefined' && typeof ARTWORK_DETAIL_BASE_PATH !== 'undefined';

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

    artworks.forEach(artwork => {
        const card = document.createElement('div');
        card.className = 'artwork-card card bg-base-100 shadow-xl hover:shadow-2xl transition-shadow';
        card.setAttribute('data-sku', artwork.sku);

        // --- IMAGE GENERATION ---
        let imageHTML = '';
        const publicId = artwork.image_public_id; 
        const altText = artwork.image_alt_text || artwork.name;
        
        if (publicId && isReady) {
            // Use the global helper function (assuming it's defined)
            const transformations = 'w_400,h_300,c_fill,f_auto,q_auto';
            const imageUrl = getCloudinaryUrl(publicId, transformations); 
            imageHTML = `<figure><img src="${imageUrl}" alt="${altText}" class="w-full h-64 object-cover"></figure>`;
        } else {
            imageHTML = `<figure><div class="bg-base-300 h-64 w-full flex items-center justify-center"><i class="fa-solid fa-image text-base-content/20 text-5xl"></i></div></figure>`;
        }
        
        // --- Card Body & Actions ---
        const detailUrl = (isReady && artwork.slug) ? ARTWORK_DETAIL_BASE_PATH + artwork.slug + '/' : '#'; 

        const bodyHTML = `
            <div class="card-body">
                <h2 class="artwork-name card-title">${artwork.name}</h2>
                <p class="artwork-description text-base-content/70">${artwork.description}</p>
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
        
        card.innerHTML = imageHTML + bodyHTML; 
        newGrid.appendChild(card);
    });
    
    container.appendChild(newGrid);
}

/** Filters artworks to show only those marked as available or in stock. */
function filterAvailableArtworks(artworks) {
    return artworks.filter(a => a.is_available || a.is_in_stock);
}

/** Sorts artworks by price in ascending order. */
function sortArtworksByPrice(artworks) {
    return [...artworks].sort((a, b) => a.price - b.price); 
}


// --- ENHANCEMENT STATE & LOGIC ---

let masterArtworkList = [];
let currentSortDirection = 'asc';
let isFilterActive = false;

function toggleLoadingState(isLoading) {
    const container = document.getElementById('artwork-list');
    if (!container) return;
    
    // Simple state toggle: Hide current content and show a spinner/message
    if (isLoading) {
        container.classList.add('opacity-50', 'pointer-events-none');
    } else {
        container.classList.remove('opacity-50', 'pointer-events-none');
    }
}

/**
 * Handles the API call to fetch the master list of artworks.
 */
function fetchArtworksFromAPI() {
    if (typeof ARTWORK_API_URL === 'undefined') {
        console.error("ARTWORK_API_URL is missing.");
        return Promise.resolve([]);
    }
    
    toggleLoadingState(true);

    return fetch(ARTWORK_API_URL) 
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            masterArtworkList = data;
            toggleLoadingState(false);
            return data;
        })
        .catch(error => {
            console.error("Error loading artworks via API:", error);
            toggleLoadingState(false);
            document.getElementById('artwork-list').innerHTML = 
                '<p class="text-center text-error p-8">Could not load dynamic artwork data.</p>';
            return [];
        });
}


/**
 * Applies current sorting/filtering state to the master list and triggers re-render.
 */
function applyStateAndRender() {
    let filteredList = [...masterArtworkList];

    if (isFilterActive) {
        filteredList = filterAvailableArtworks(filteredList);
    }

    filteredList = sortArtworksByPrice(filteredList);
    if (currentSortDirection === 'desc') {
        filteredList.reverse();
    }

    renderArtworkList(filteredList);
}

// -------------------------------------------------------------------
// INITIALIZATION AND EVENT HOOKS
// -------------------------------------------------------------------

function initArtworkListEnhancements() {
    const sortButton = document.getElementById('sort-price');
    const filterButton = document.getElementById('filter-available');
    // Initial fetch to populate master list
    fetchArtworksFromAPI().then(artworks => {
        // If data is successfully fetched, the SSR content can now be replaced 
        // with the full, unpaginated data to enable full client-side control.
        if (artworks.length > 0) {
            applyStateAndRender();
        } 
    });


    // --- Sorting Handler ---
    if (sortButton) {
        sortButton.addEventListener('click', () => {
            currentSortDirection = (currentSortDirection === 'asc' ? 'desc' : 'asc');

            // Update button icon
            const icon = sortButton.querySelector('i');
            if (icon) {
                 icon.className = currentSortDirection === 'asc' 
                    ? 'fa-solid fa-sort-amount-up' 
                    : 'fa-solid fa-sort-amount-down';
            }
            
            // Apply changes and re-render
            applyStateAndRender();
        });
    }

    // --- Filtering Handler ---
    if (filterButton) {
        filterButton.addEventListener('click', () => {
            isFilterActive = !isFilterActive;

            // Update button styling
            if (isFilterActive) {
                filterButton.classList.remove('btn-outline');
                filterButton.classList.add('btn-success');
            } else {
                filterButton.classList.remove('btn-success');
                filterButton.classList.add('btn-outline');
            }
            
            // Apply changes and re-render
            applyStateAndRender();
        });
    }
}

// Attach the enhancement initialization logic to the DOM load event
document.addEventListener("DOMContentLoaded", initArtworkListEnhancements);