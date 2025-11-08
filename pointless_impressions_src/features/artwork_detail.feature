Feature: US002 - View Artwork Details
  As a customer,
  I want to view detailed information about an artwork,
  so that I can decide whether to purchase it.

  Scenario: Customer views availability status
    Given the following artworks exist
    | name           | artist  | price   | category  | availability | stock |
    | Mountain Peak  | Michael | £249.99 | Landscape | Available    | 2     |
    | Ocean Breeze   | Michael | £199.99 | Seascape  | Available    | 1     |
    | Sold Out Art   | Michael | £149.99 | Portrait  | Unavailable  | 0     |
    When I view the details for "Mountain Peak"
    Then I should see "Available" status
    And I should see "Add to Cart" button
    
  Scenario: Customer cannot add sold out artwork to cart
    Given the following artworks exist
    | name           | artist  | price   | category  | availability | stock |
    | Mountain Peak  | Michael | £249.99 | Landscape | Available    | 2     |
    | Ocean Breeze   | Michael | £199.99 | Seascape  | Available    | 1     |
    | Sold Out Art   | Michael | £149.99 | Portrait  | Unavailable  | 0     |
    When I view the details for "Sold Out Art"
    Then I should see "Sold Out" status
    And I should not see the "Add to Cart" button

  Scenario: Customer views artist information
    Given the following artworks exist
    | name           | artist  | price   | category  | availability | stock |
    | Mountain Peak  | Michael | £249.99 | Landscape | Available    | 2     |
    | Ocean Breeze   | Michael | £199.99 | Seascape  | Available    | 1     |
    | Sold Out Art   | Michael | £149.99 | Portrait  | Unavailable  | 0     |
    When I view the details for "Mountain Peak"
    Then I should see the artist name "Michael"
    And I should see the artist profile link

  Scenario: Customer views related artworks
    Given the following artworks exist
    | name           | artist  | price   | category  | availability | stock |
    | Mountain Peak  | Michael | £249.99 | Landscape | Available    | 2     |
    | Ocean Breeze   | Michael | £199.99 | Seascape  | Available    | 1     |
    | Sold Out Art   | Michael | £149.99 | Portrait  | Unavailable  | 0     |
    When I view the details for "Mountain Peak"
    Then I should see related artworks section
    And I should see other artworks in the same category

  Scenario: Customer views artwork size and framing options
    Given the following artworks exist
    | name           | artist  | price   | category  | availability | stock |
    | Mountain Peak  | Michael | £249.99 | Landscape | Available    | 2     |
    | Ocean Breeze   | Michael | £199.99 | Seascape  | Available    | 1     |
    | Sold Out Art   | Michael | £149.99 | Portrait  | Unavailable  | 0     |
    When I view the details for "Mountain Peak"
    Then I should see artwork dimensions
    And I should see available framing conditions
