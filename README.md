# Commerce

## Overview
This repository contains the solution for Project 2 (Commerce) from CS50W. Commerce is a web application developed with Django, geared towards simplifying online auctions. Its functionalities enable users to generate listings for items they wish to sell, bid on available listings, engage in discussions via comments, and oversee a watchlist of items they're keen on.

## Project Structure
The project consists of the following components:

- **URL Configuration (`urls.py`):** Defines the URL patterns for different views in the application.
- **Views (`views.py`):** Contains the logic for handling HTTP requests and rendering HTML templates.
- **Models (`models.py`):** Defines the database schema using Django's ORM (Object-Relational Mapping).
- **Templates:**
  - **Layout Template (`layout.html`):** Provides a common layout structure for other templates.
  - **Individual HTML Templates:** Separate templates for different views like index, listing, category, etc.
- **Static Files:**
  - **CSS (`styles.css`):** Contains custom styles for the application.

## Functionality
### User Authentication
- Users can register for an account.
- Registered users can log in and log out.

### Listings
- Users can create new listings by providing details such as title, description, starting price, category, and an optional image URL.
- Listings display relevant information such as title, current price, creation date, and category.
- Users can view all active listings on the homepage.

### Bidding
- Registered users can place bids on active listings.
- Bids must be greater than the current price of the listing.
- The highest bid for each listing is displayed.

### Comments
- Users can comment on active listings.
- Comments are displayed on the listing page.

### Watchlist
- Registered users can add listings to their watchlist.
- Users can view all listings they've added to their watchlist.

### Categories
- Listings are categorized, and users can browse listings by category.

### Closing Listings
- Sellers can close their listings, removing them from active listings.

## Code Structure
- **helpers.py:** Contains helper functions used across views.
- **HTML Templates:**
  - Each HTML template extends the base layout template and includes specific content blocks.
  - **`error.html`:** Template for displaying error messages.

## Usage
To run the Commerce application locally:
1. Ensure you have Python and Django installed.
2. Clone the project repository.
3. Navigate to the project directory in your terminal.
4. Run the Django development server using the `python manage.py runserver` command.
5. Access the application in your web browser at the specified address.

## Conclusion
Commerce provides a platform for users to engage in online auctions, allowing them to buy and sell items in a user-friendly environment. With its various features like bidding, commenting, and categorization, it offers a comprehensive solution for online auction needs.

## Video Demonstration
[![Click to watch the video demonstration](https://img.youtube.com/vi/qh8P34Trz48/0.jpg)](https://www.youtube.com/watch?v=qh8P34Trz48)

## Acknowledgements
I wish to express my heartfelt appreciation to the CS50 staff for their exceptional materials. Their comprehensive resources were pivotal in expanding my knowledge and skills significantly. This project, assigned as part of CS50W, has served as an excellent learning opportunity, thanks to their dedication to fostering excellence in education.
