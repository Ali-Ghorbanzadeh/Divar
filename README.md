
# Project: Divar

This project simulates an advertisement platform similar to "Diwar" and provides users with functionalities for posting, searching, and managing ads across various categories.

## Overview

The application is a web-based API service that allows users to publish ads under administrative management, with a structured category system, custom fields, and user role-based access.

### Features

- **User Roles**: Supports various roles, including Super Admin, Site Admin, Authenticated User, and Guest, each with specific permissions.
- **Category Management**: 
  - Categories are organized hierarchically with custom fields unique to each category level.
  - Only Super Admins can create and edit categories.
- **Authentication**: 
  - Users log in using OTP (One-Time Password) sent to their phone/email without needing a traditional password.
  - JWT-based authentication for secure session management.
- **Ad Posting and Management**: 
  - Users can post ads with required fields (e.g., title, images, description) and category-specific fields defined by admins.
  - Ads can be boosted for greater visibility within search results.
- **Search and Filters**:
  - Search functionality includes category and location filters.
  - Sorting options by date and price, with frequent searches cached for faster performance.
  
### Technical Stack

- **Backend**: Django framework with PostgreSQL for database.
- **Authentication**: JWT for secure logins and Celery for handling OTP tasks.
- **Deployment**: Docker for easy deployment.
- **Performance Optimization**: Caching frequently used queries to enhance system responsiveness.

### Setup Instructions

1. **Clone the Repository**: Retrieve the project files from GitHub.
2. **Environment Configuration**: Ensure Docker is installed and set up required dependencies.
3. **Database Configuration**: Configure PostgreSQL and apply necessary migrations.
4. **Run Services**: Start the Docker container to launch the API.

### Testing & Verification

The application includes API endpoints for functionality testing. Fake data generation is supported for system load testing.
