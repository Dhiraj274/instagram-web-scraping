from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os
from dotenv import load_dotenv
import csv

# Load environment variables from .env file
load_dotenv('MyInsta.env')

# Load list of user profiles
user_profiles = [
    "instagram",
    "cristiano",
    "nasa",
    "linkedin"
]


driver_path = "chromedriver-win64/chromedriver.exe"
service = Service(driver_path)
driver = webdriver.Chrome(service=service)
driver.get('https://www.instagram.com/accounts/login/')

# Allow the page to load
time.sleep(5)

# Login to Instagram
username = driver.find_element(By.NAME, 'username')
password = driver.find_element(By.NAME, 'password')

username.send_keys(os.getenv('INSTAGRAM_USERNAME'))
password.send_keys(os.getenv('INSTAGRAM_PASSWORD'))

# Submit the login form
password.send_keys(Keys.RETURN)

# Wait for the URL to change indicating redirection
try:
    WebDriverWait(driver, 10).until(EC.url_contains('onetap'))
    print("Redirected to one-tap page")
except Exception as e:
    print(f"Redirection to one-tap page not detected: {e}")

# Handle the "Save Your Login Info?" prompt
try:
    not_now_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, '_ac8f'))
    )
    not_now_button.click()
    print("Clicked 'Not Now' on Save Your Login Info window")
except Exception as e:
    print(f"Error clicking 'Not Now' button: {e}")

# Handle the "Turn on Notifications" prompt
try:
    turn_on_notifications_not_now = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now']"))
    )
    turn_on_notifications_not_now.click()
    print("Clicked 'Not Now' on Turn on Notifications prompt")
except Exception as e:
    print(f"Turn on Notifications prompt not found: {e}")


# Function to find the search bar
def find_search_bar(driver):
    search_bar = None
    
    # List of XPaths for potential search bar locations
    search_bar_xpaths = [
        "//input[@placeholder='Search']",
        "//input[@aria-label='Search']",
        "//input[@type='text' and @aria-label]",
        "//input[@type='text' and not(@aria-label='')]",
        "//input[@type='text']",
    ]
    
    # click on the search icon to bring up the search input
    try:
        search_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[class*='x1i10hfl'][role='link'][href='#']"))
        )
        search_icon.click()
        
        # Retry locating the search bar
        for xpath in search_bar_xpaths:
            try:
                search_bar = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                if search_bar:
                    return search_bar
            except:
                pass
    except:
        pass


    # Try locating the search bar directly
    for xpath in search_bar_xpaths:
        try:
            search_bar = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            if search_bar:
                return search_bar
        except:
            pass
    
    return search_bar


# Extract data for each user profile
followers_data = []

for username in user_profiles:

    # Use the search bar to find the user
    search_bar = find_search_bar(driver)
    if search_bar is None:
        raise Exception("Search bar not found")
    
    search_bar.clear()
    search_bar.send_keys(username)
    time.sleep(3)  # Allow search results to populate

    # Click on the user's profile from the search results
    try:
        profile_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//a[contains(@href, '/{username}/')]"))
        )
        profile_link.click()
    except Exception as e:
        print(f"Error clicking on profile link for {username}: {e}")
        continue  # Skip to the next user if there's an error

    time.sleep(3)  # Let the profile page load

    # Extract post count using the span tag with class _ac2a
    try:
        post_count = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span._ac2a span"))
        ).text
    except Exception as e:
        print(f"Error extracting post count: {e}")
        post_count = "N/A"

    # Extract follower count using CSS_SELECTOR
    try:
        follower_count_element = driver.find_element(By.CSS_SELECTOR, "ul li:nth-child(2) a span")
        follower_count_text = follower_count_element.text
        
        print("Follower Count:", follower_count_text)
    except Exception as e:
        print(f"Error extracting follower count: {e}")
        follower_count = "N/A"

    # Extract following count using CSS_SELECTOR
    try:
        following_count_element = driver.find_element(By.CSS_SELECTOR, "ul li:nth-child(3) a span")
        following_count_text = following_count_element.text

        print("Following Count:", following_count_text)
    except Exception as e:
        print(f"Error extracting following count: {e}")
        following_count = "N/A"


    # Append the extracted data to the list
    followers_data.append({
        "Username": username,
        "Post Count": post_count,
        "Follower Count": follower_count_text,
        "Following Count": following_count_text
    })

    # Navigate back to the previous page (search bar)
    driver.back()
    time.sleep(3)  # Wait for the previous page to load

# Save data to CSV
csv_file_path = "instagram_user_data.csv"
with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["Username", "Post Count", "Follower Count", "Following Count"])
    writer.writeheader()
    for data in followers_data:
        writer.writerow(data)


# Close the driver
driver.quit()

print("Data extraction and CSV creation completed successfully.")
