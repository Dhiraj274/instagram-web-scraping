# Instagram Web Scraping Project

## Overview

This project is designed to scrape data from Instagram user profiles, including the number of posts, followers, and following counts. The data is extracted using Selenium and saved in a CSV file for further analysis.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Project Structure](#project-structure)
4. [Functionality](#functionality)
5. [Contributing](#contributing)

## Installation

### Prerequisites

- Python 3.x
- [Google Chrome](https://www.google.com/chrome/) browser
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) (compatible with your Chrome browser version)
- [Git](https://git-scm.com/) (optional, for cloning the repository)

### Environment Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Dhiraj274/instagram-web-scraping.git
    cd instagram-web-scraping
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - **Windows:**

        ```bash
        .\venv\Scripts\activate
        ```

    - **macOS/Linux:**

        ```bash
        source venv/bin/activate
        ```

4. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Set up environment variables:**

    - Create a `.env` file in the project directory and add your Instagram credentials:

        ```text
        INSTAGRAM_USERNAME=your_username
        INSTAGRAM_PASSWORD=your_password
        ```

## Usage

1. **Edit the list of user profiles:**

    - Open the Python script and modify the `user_profiles` list with the Instagram usernames you want to scrape.

2. **Run the script:**

    ```bash
    python instagram_scraper.py
    ```

3. **View the extracted data:**

    - The data will be saved in a CSV file named `instagram_user_data.csv` in the project directory.

## Functionality

- **Login to Instagram:**
    - Uses Selenium to automate the login process with provided credentials.
- **Search and navigate to user profiles:**
    - Searches for each username in the list and navigates to their profile page.
- **Extract data:**
    - Retrieves the number of posts, followers, and following counts.
- **Save data:**
    - Stores the extracted data in a CSV file for further analysis.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.


