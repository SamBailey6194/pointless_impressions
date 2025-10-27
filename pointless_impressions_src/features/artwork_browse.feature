# US001: Browse Pointillism Artwork

Feature: Browse Pointillism Artwork
    As a customer
    I want to browse available artwork
    So that I can view what is currently for sale

    Background:
        Given the following artworks exist:
        | name         | description                           | price  | sku         | is_available | is_in_stock |
        | Sunset       | A beautiful sunset over the mountains. | 199.99 | SUNSET123   | True         | True        |
        | Starry Night | A night sky full of color and dots.    | 299.99 | STARRY123   | False        | False       |

    Scenario: Viewing available artwork
        When I visit the artwork listing page
        Then I should see "Sunset"
        And I should see "A beautiful sunset over the mountains."
        And I should see the price "£199.99"

    Scenario: Sold out artworks are clearly marked
        When I visit the artwork listing page
        Then I should see "Starry Night"
        And I should see "Sold Out" next to "Starry Night"

    Scenario: Sort artworks by price
        When I visit the artwork listing page sorted by "price"
        Then artworks should be displayed in ascending price order

    Scenario: Filter artworks by availability
        When I visit the artwork listing page with filter "available"
        Then I should see "Sunset"
        And I should not see "Starry Night"
