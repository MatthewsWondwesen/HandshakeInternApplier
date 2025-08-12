from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import getpass

class LinkedInBot:
    def __init__(self, email, password):
        # Initialize the webdriver (Chrome in this case)
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.email = email
        self.password = password
        
    def login(self):
        """Login to LinkedIn"""
        try:
            self.driver.get("https://www.linkedin.com/login")
            
            # Find and fill in email
            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_field.send_keys(self.email)
            
            # Find and fill in password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(self.password)
            
            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            time.sleep(3)  # Wait for login to complete
            return True
            
        except Exception as e:
            print(f"Error during login: {str(e)}")
            return False
    
    def search_internships(self, keywords):
        """Search for internships with given keywords"""
        try:
            # Open a new tab with the jobs page
            self.driver.execute_script("window.open('https://www.linkedin.com/jobs/', '_blank')")
            
            # Switch to the new tab (it will be the last tab opened)
            self.driver.switch_to.window(self.driver.window_handles[-1])
            
            # Wait for the page to load and find the search box
            search_box = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Search by title, skill, or company']"))
            )
            
            # Clear any existing text and enter the search terms
            search_box.clear()
            search_box.send_keys(f"{keywords} internship")
            search_box.send_keys(Keys.RETURN)  # Press Enter to submit
            
            # Wait for results to load
            time.sleep(3)
            
            try:
                # Click on Experience Level filter using the specific button
                experience_button = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Experience level filter. Clicking this button displays all Experience level filter options.']"))
                )
                experience_button.click()
                
                # Wait for the filter modal to appear and click Internship checkbox
                internship_checkbox = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[id='experience-1']"))
                )
                # Click the label instead of the checkbox for better interaction
                internship_label = self.driver.find_element(By.CSS_SELECTOR, "label[for='experience-1']")
                internship_label.click()
                
                # Click Show Results button
                show_results = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Apply current filter to show results']"))
                )
                show_results.click()
                
                # Wait for results to update
                time.sleep(2)
                
                return True
                
            except Exception as e:
                print("Error during filter application:", str(e))
                return False
                
        except Exception as e:
            print(f"Error during search: {str(e)}")
            return False
    
    def apply_to_jobs(self, num_applications=10):
        """Apply to jobs from search results"""
        applied_count = 0
        
        try:
            # Get all job cards
            job_cards = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".job-card-container"))
            )
            
            for job_card in job_cards[:num_applications]:
                try:
                    # Click on the job card
                    job_card.click()
                    time.sleep(2)
                    
                    # Look for the easy apply button
                    apply_button = self.driver.find_element(By.CSS_SELECTOR, ".jobs-apply-button")
                    
                    if "Easy Apply" in apply_button.text:
                        apply_button.click()
                        time.sleep(2)
                        
                        # Submit application if it's a simple one
                        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Submit application']")
                        if submit_button.is_enabled():
                            submit_button.click()
                            applied_count += 1
                            print(f"Successfully applied to job {applied_count}")
                            time.sleep(2)
                        
                except Exception as e:
                    print(f"Error applying to a job: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"Error in apply_to_jobs: {str(e)}")
            
        return applied_count
    
    def close(self):
        """Close the browser"""
        self.driver.quit()

def get_credentials():
    """Get user credentials securely"""
    print("\n=== LinkedIn Automation Login ===")
    print("Please enter your LinkedIn credentials:")
    email = input("Email: ").strip()
    # Using getpass for secure password input (won't show characters as typed)
    password = getpass.getpass("Password: ").strip()
    
    # Basic validation
    while not email or not password:
        print("\nBoth email and password are required!")
        if not email:
            email = input("Email: ").strip()
        if not password:
            password = getpass.getpass("Password: ").strip()
    
    return email, password

def main():
    print("Welcome to LinkedIn Internship Application Bot!")
    
    # Get credentials from user
    email, password = get_credentials()
    
    # Initialize bot with user credentials
    bot = LinkedInBot(email, password)
    
    if bot.login():
        print("\nSuccessfully logged in!")
        
        # Ask user for search preferences
        while True:
            search_terms = input("\nWhat type of internship are you looking for? (e.g., 'software developer', 'mechanical engineer'): ").strip()
            if search_terms:
                break
            print("Please enter valid search terms.")
        
        if bot.search_internships(search_terms):
            print(f"\nSearching for {search_terms} internships...")
            
            num_applications = input("How many applications would you like to submit? (default: 10): ").strip()
            num_applications = int(num_applications) if num_applications.isdigit() else 10
            
            # Apply to specified number of jobs
            applied_count = bot.apply_to_jobs(num_applications)
            print(f"\nApplied to {applied_count} jobs")
    else:
        print("\nLogin failed. Please check your credentials and try again.")
    
    print("\nClosing browser...")
    bot.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Exiting...")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
    finally:
        print("\nProgram finished.")