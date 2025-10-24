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
    
    Scenario: View artwork details
        When I visit the artwork listing page
        And I click on "Sunset"
        Then I should see "Sunset"
        And I should see "A beautiful sunset over the mountains."
        And I should see the price "£199.99"
        And I should see an "Add to Cart" button

    Scenario: Add artwork to cart
        Given I am on the artwork detail page for "Sunset"
        When I click the "Add to Cart" button
        Then "Sunset" should be added to my shopping cart
        And I should see a confirmation message "Sunset has been added to your cart."
    
    Scenario: Attempt to add sold out artwork to cart
        Given I am on the artwork detail page for "Starry Night"
        When I click the "Add to Cart" button
        Then I should see an error message "Sorry, Starry Night is currently sold out."
        And I should not see an "Add to Cart" button

# Linked to steps in artwork/features/steps/artwork_browse_steps.py
# to run tests: behave pointless_impressions_src/artwork/features/artwork_browse.feature
