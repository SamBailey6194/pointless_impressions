Feature: US002 - View Artwork Details
  As a customer,
  I want to view detailed information about an artwork,
  so that I can decide whether to purchase it.

  Scenario: Customer views artwork details
    Given the following artworks exist
    | name           | artist  | price   | category  | availability | stock |
    | Mountain Peak  | Michael | £249.99 | Landscape | Available    | 2     |
    | Ocean Breeze   | Michael | £199.99 | Seascape  | Available    | 1     |
    | Sold Out Art   | Michael | £149.99 | Portrait  | Unavailable  | 0     |
    When I view the details for "Mountain Peak"
    Then I should see the artwork title "Mountain Peak"
    And I should see the artwork description
    And the artwork price should be "£249.99"
    And I should see the artwork image
    And I should see the "Add to Cart" button

  Scenario: Customer sees larger image on detail page
    Given the following artworks exist
    | name           | artist  | price   | category  | availability | stock |
    | Mountain Peak  | Michael | £249.99 | Landscape | Available    | 2     |
    | Ocean Breeze   | Michael | £199.99 | Seascape  | Available    | 1     |
    | Sold Out Art   | Michael | £149.99 | Portrait  | Unavailable  | 0     |
    When I view the details for "Mountain Peak"
    Then I should see a high-quality image of the artwork
    And the image should be larger than on the browse page

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

  Scenario: Customer can add available artwork to cart from detail page
    Given the following artworks exist
    | name           | artist  | price   | category  | availability | stock |
    | Mountain Peak  | Michael | £249.99 | Landscape | Available    | 2     |
    | Ocean Breeze   | Michael | £199.99 | Seascape  | Available    | 1     |
    | Sold Out Art   | Michael | £149.99 | Portrait  | Unavailable  | 0     |
    When I view the details for "Mountain Peak"
    And I click the "Add to Cart" button
    Then the artwork should be added to my cart
    And I should see a confirmation message
