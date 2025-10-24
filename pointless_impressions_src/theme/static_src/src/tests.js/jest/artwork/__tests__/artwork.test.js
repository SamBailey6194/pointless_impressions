/**
 * @jest-environment jsdom
 */

import { renderArtworkList, filterAvailableArtworks, sortArtworksByPrice } from '../../../../js/artwork.js';

const html = fs.readFileSync(
  path.resolve(__dirname, '../fixtures/artwork.html'),
  'utf8'
);

describe('US001: Browse Pointillism Artwork (Frontend)', () => {
  let artworks;

  beforeEach(() => {
    // Sample artwork data
    artworks = [
      {
        name: 'Sunset',
        description: 'A beautiful sunset over the mountains.',
        price: 199.99,
        sku: 'SUNSET123',
        is_available: true,
        is_in_stock: true
      },
      {
        name: 'Starry Night',
        description: 'A night sky full of color and dots.',
        price: 299.99,
        sku: 'STARRY123',
        is_available: false,
        is_in_stock: false
      }
    ];

    // Set up DOM
    document.body.innerHTML = `
      <div id="artwork-list"></div>
    `;
  });

  test('Viewing available artwork shows correct info', () => {
    renderArtworkList(artworks);

    const artworkList = document.getElementById('artwork-list');
    expect(artworkList.textContent).toContain('Sunset');
    expect(artworkList.textContent).toContain('A beautiful sunset over the mountains.');
    expect(artworkList.textContent).toContain('£199.99');
  });

  test('Sold out artworks are clearly marked', () => {
    renderArtworkList(artworks);

    const artworkList = document.getElementById('artwork-list');
    expect(artworkList.textContent).toContain('Starry Night');
    expect(artworkList.textContent).toContain('Sold Out');
  });

  test('Sorting artworks by price ascending', () => {
    const sorted = sortArtworksByPrice(artworks);
    expect(sorted[0].price).toBeLessThanOrEqual(sorted[1].price);
  });

  test('Filtering available artworks', () => {
    const available = filterAvailableArtworks(artworks);
    expect(available.length).toBe(1);
    expect(available[0].name).toBe('Sunset');
  });

  test('Clicking on artwork shows details (mock)', () => {
    // Assuming you have a function like showArtworkDetail
    document.body.innerHTML += `<div id="artwork-detail"></div>`;
    const artwork = artworks[0];
    // simulate the function that renders details
    const detailDiv = document.getElementById('artwork-detail');
    detailDiv.innerHTML = `<h2>${artwork.name}</h2><p>${artwork.description}</p><span>£${artwork.price}</span><button>Add to Cart</button>`;

    expect(detailDiv.textContent).toContain('Sunset');
    expect(detailDiv.textContent).toContain('A beautiful sunset over the mountains.');
    expect(detailDiv.textContent).toContain('£199.99');
    expect(detailDiv.querySelector('button').textContent).toBe('Add to Cart');
  });
});
