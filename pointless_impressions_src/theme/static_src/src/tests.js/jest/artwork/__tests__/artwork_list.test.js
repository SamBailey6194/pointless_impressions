/**
 * @jest-environment jsdom
 */

import { renderArtworkList, filterAvailableArtworks, sortArtworksByPriceAsc, sortArtworksByPriceDesc, sortArtworksByName, sortArtworksByArtist } from '../../../../js/artwork_list';

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
        is_in_stock: true,
        artist: { username: 'blake' }
      },
      {
        name: 'Starry Night',
        description: 'A night sky full of color and dots.',
        price: 299.99,
        sku: 'STARRY123',
        is_available: false,
        is_in_stock: false,
        artist: { username: 'chris' }
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
    const sorted = sortArtworksByPriceAsc(artworks);
    expect(sorted[0].price).toBeLessThanOrEqual(sorted[1].price);
  });

  test('Sorting artworks by price descending', () => {
    const sorted = sortArtworksByPriceDesc(artworks);
    expect(sorted[0].price).toBeGreaterThanOrEqual(sorted[1].price);
  });

  test('Sorting artworks alphabetically', () => {
    const sorted = sortArtworksByName(artworks);
    expect(sorted[0].name.localeCompare(sorted[1].name)).toBeLessThanOrEqual(0);
  });

  test('Sorting artworks by artist', () => {
    const sorted = sortArtworksByArtist(artworks);
    expect(sorted[0].artist.username.localeCompare(sorted[1].artist.username)).toBeLessThanOrEqual(0);
  });

  test('Filtering available artworks', () => {
    const available = filterAvailableArtworks(artworks);
    expect(available.length).toBe(1);
    expect(available[0].name).toBe('Sunset');
  });
});
