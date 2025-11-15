# US003: Add Artwork to Cart

Feature: Add Artwork to Cart
    As a customer
    I want to add artwork to a shopping cart
    So that I can review and purchase it later

    Scenario: Add available artwork to cart
        Given the following artworks exist:
        | name               | description                    | price  | sku          | is_available | is_in_stock | quantity |
        | Sunset Pointilism  | Beautiful sunset with dots     | 199.99 | SUNSET-001   | True         | True        | 5        |
        When I navigate to the artwork "Sunset Pointilism" detail page
        And I click the "Add to Cart" button
        Then the artwork should be added to my cart
        And the cart should show 1 item
        And the cart total should be "£199.99"

    Scenario: Prevent adding sold-out artwork to cart
        Given the following artworks exist:
        | name               | description                    | price  | sku          | is_available | is_in_stock | quantity |
        | Sold Out Artwork   | This artwork is sold out       | 299.99 | SOLDOUT-001  | False        | False       | 0        |
        When I navigate to the artwork "Sold Out Artwork" detail page
        Then the "Add to Cart" button should not be visible or should be disabled

    Scenario: Add multiple different artworks to cart
        Given the following artworks exist:
        | name               | description                    | price  | sku          | is_available | is_in_stock | quantity |
        | Sunset Pointilism  | Beautiful sunset with dots     | 199.99 | SUNSET-001   | True         | True        | 5        |
        | Ocean Waves        | Ocean pointillism              | 249.99 | OCEAN-001    | True         | True        | 3        |
        When I navigate to the artwork "Sunset Pointilism" detail page
        And I click the "Add to Cart" button
        And I navigate to the artwork "Ocean Waves" detail page
        And I click the "Add to Cart" button
        Then the cart should show 2 items
        And the cart total should be "£449.98"

    Scenario: Increment quantity when adding same artwork twice
        Given the following artworks exist:
        | name               | description                    | price  | sku          | is_available | is_in_stock | quantity |
        | Sunset Pointilism  | Beautiful sunset with dots     | 199.99 | SUNSET-001   | True         | True        | 5        |
        When I navigate to the artwork "Sunset Pointilism" detail page
        And I click the "Add to Cart" button
        And I click the "Add to Cart" button again
        Then the cart should show 1 item (2 quantity)
        And the cart total should be "£399.98"

    Scenario: Cart shows item name, price, and total
        Given the following artworks exist:
        | name               | description                    | price  | sku          | is_available | is_in_stock | quantity |
        | Mountain Peak      | Mountain pointillism           | 179.99 | MOUNTAIN-001 | True         | True        | 4        |
        When I navigate to the artwork "Mountain Peak" detail page
        And I click the "Add to Cart" button
        And I navigate to the cart page
        Then I should see the item "Mountain Peak" in the cart
        And the cart should contain price "£179.99"
        And I should see the total price

    Scenario: Remove artwork from cart
        Given the following artworks exist:
        | name               | description                    | price  | sku          | is_available | is_in_stock | quantity |
        | Sunset Pointilism  | Beautiful sunset with dots     | 199.99 | SUNSET-001   | True         | True        | 5        |
        | Ocean Waves        | Ocean pointillism              | 249.99 | OCEAN-001    | True         | True        | 3        |
        When I navigate to the artwork "Sunset Pointilism" detail page
        And I click the "Add to Cart" button
        And I navigate to the artwork "Ocean Waves" detail page
        And I click the "Add to Cart" button
        And I navigate to the cart page
        And I click the remove button for "Ocean Waves"
        Then the cart should show 1 item
        And I should see "Sunset Pointilism" in the cart
        And I should not see "Ocean Waves" in the cart
        And the cart total should be "£199.99"

    Scenario: Update cart quantity
        Given the following artworks exist:
        | name               | description                    | price  | sku          | is_available | is_in_stock | quantity |
        | Sunset Pointilism  | Beautiful sunset with dots     | 199.99 | SUNSET-001   | True         | True        | 5        |
        When I navigate to the artwork "Sunset Pointilism" detail page
        And I click the "Add to Cart" button
        And I navigate to the cart page
        And I update the quantity to 3
        Then the item quantity should be 3
        And the cart total should be "£599.97"

    Scenario: Prevent quantity exceeding available stock
        Given the following artworks exist:
        | name               | description                    | price  | sku          | is_available | is_in_stock | quantity |
        | Limited Artwork    | Only 2 available               | 149.99 | LIMITED-001  | True         | True        | 2        |
        When I navigate to the artwork "Limited Artwork" detail page
        And I click the "Add to Cart" button
        And I navigate to the cart page
        And I try to update the quantity to 5
        Then the quantity should remain at 1 (or max allowed: 2)
        And an error message should be shown about insufficient stock
