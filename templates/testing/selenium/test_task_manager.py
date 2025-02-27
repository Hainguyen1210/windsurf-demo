import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# This is a minimal starter template for Selenium tests
# You can use Windsurf to expand this into a full test suite

class TaskManagerTest(unittest.TestCase):
    
    def setUp(self):
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Initialize the WebDriver
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        
        # Navigate to the application
        self.driver.get("http://localhost:3000")
        
        # Wait for the page to load
        self.wait = WebDriverWait(self.driver, 10)
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    
    def tearDown(self):
        # Close the browser
        if self.driver:
            self.driver.quit()
    
    def test_page_title(self):
        """Test that the page title is correct"""
        self.assertEqual("Task Manager", self.driver.title)
    
    def test_create_task(self):
        """Test creating a new task"""
        # Find the 'Add Task' button and click it
        add_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add Task')]"))
        )
        add_button.click()
        
        # Wait for the form to appear
        self.wait.until(EC.presence_of_element_located((By.ID, "task-form")))
        
        # Fill out the form
        title_input = self.driver.find_element(By.ID, "title")
        title_input.send_keys("Test Task")
        
        description_input = self.driver.find_element(By.ID, "description")
        description_input.send_keys("This is a test task created by Selenium")
        
        status_select = self.driver.find_element(By.ID, "status")
        status_select.send_keys("pending")
        
        # Submit the form
        submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
        submit_button.click()
        
        # Wait for the task to appear in the list
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Test Task')]"))
        )
        
        # Verify the task was created
        task_elements = self.driver.find_elements(By.XPATH, "//div[contains(text(), 'Test Task')]")
        self.assertGreaterEqual(len(task_elements), 1)
    
    def test_update_task(self):
        """Test updating an existing task"""
        # TODO: Implement test for updating a task
        pass
    
    def test_delete_task(self):
        """Test deleting a task"""
        # TODO: Implement test for deleting a task
        pass


if __name__ == "__main__":
    unittest.main()
