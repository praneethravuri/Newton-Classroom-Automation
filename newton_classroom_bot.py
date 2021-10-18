__author__ = "Ravuri Praneeth"
__credits__ = ["Ravuri Praneeth"]
__version__ = "1.0"
__maintainer__ = "Ravuri Praneeth"
__github_repo_link__ = "https://github.com/praneethravuri/Newton-Classroom-Automation"

import os
import time
import requests
from xpath_logs import *
from bs4 import BeautifulSoup
from tabulate import tabulate
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, InvalidSessionIdException, NoSuchAttributeException,TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


class NewtonClassroomAutomation:
    def __init__(self):  # Initialize
        self.driver = None
        self.soup = None

    @staticmethod
    def auto_update():
        # Update the xpath_logs.txt

        print("\nUpdating xpath_log.py ...")
        xpath_logs_url = "https://raw.githubusercontent.com/praneethravuri/Newton-Classroom-Automation/master/xpath_logs.py"

        xpath_logs_contents = requests.get(xpath_logs_url)

        with open("xpath_logs.py", "r+") as f:
            f.truncate(0)
            f.close()

        with open("xpath_logs.py", "w") as f:
            f.write(xpath_logs_contents.text)
            f.close()

        print("xpath_logs.py successfully updated\n")

    def open_browser(self):  # Open the browser

        """
        1. Open browser
        2. Add the preferences enable camera, microphone and notifications
        3. Open the link
        """

        opt = Options()

        opt.add_argument("--disable-infobars")
        opt.add_argument("--disable-extensions")
        opt.add_argument("--start-maximized")
        opt.add_argument('--log-level=OFF')
        opt.add_experimental_option('excludeSwitches', ['enable-logging'])

        # Pass the argument 1 to allow and 2 to block
        opt.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1,  # Allow access to the microphone
            "profile.default_content_setting_values.media_stream_camera": 1,  # Allow access to the camera
            "profile.default_content_setting_values.notifications": 1  # Allow access to all the notifications
        })

        url = "https://griet.newtonclassroom.com/"  # Newton Classroom link
        # Installing chrome web driver in cache and adding the attribute for enabling audio/video
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=opt)
        self.driver.get(url)  # Opening the url

        print("\n" + "=" * 20 + " NEWTON CLASSROOM BOT " + "=" * 20)

        print("\n****** DO NOT CLOSE THIS CONSOLE WINDOW OR THE BROWSER ******\n")

        print("="*17 + " " + str(current_date_time) + " " + "="*17 + "\n")

        print("\nOpened the browser")

    @staticmethod
    def get_credentials():
        """
        1. If there are no contents in credentials.txt, ask the user for the email and password
        2. If there are contents in credentials.txt, continue the script
        """

        path_creds = "credentials.txt"  # Path of the text file containing the student credentials
        # Path of the text file containing the developer notes and information about the script

        if not os.path.isfile(path_creds) or os.path.getsize(path_creds) == 0:   
            input_email = input("Enter email address: ")
            input_password = input("Enter password: ")
            f = open(path_creds, "w", encoding="utf8")
            f.write(input_email + "\n" + input_password)  # Add the credentials to credentials.txt
            f.close()
            print("Login credentials are stored in 'credentials.txt'")
            return [input_email, input_password]

        else:
            f = open(path_creds)
            creds = f.readlines()  # Read the file to get the credentials
            f.close()
            print("Login credentials are present in 'credentials.txt'")
            ex_email = creds[0][0:-1]
            ex_password = creds[1]
            return [ex_email, ex_password]

    def enter_credentials(self, credentials_info):  # Enter the email and password

        """
        1. Wait till "Sign in with google button appears" and click it
        2. Wait till email text box appears and enter email address and click on next
        3. Wait till password text box appears and enter password and click on next
        """

        email = credentials_info[0]
        password = credentials_info[1]

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, google_login_button))).click()  # Clicking on the 'Sign In with Google' button

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, email_text_box))).send_keys(
            email)  # Entering the email address
        self.driver.find_element_by_xpath(next_button).click()  # Click on the 'Next' button
        print("\nEntered the email address")

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, password_text_box))).send_keys(
            password)  # Entering the password
        self.driver.find_element_by_xpath(next_button).click()  # Click on the 'Next' button
        print("Entered the password")

        print("The credentials have been entered successfully")

    def extract_webpage_information(self):

        """
        1. Parse through the webpage using BeautifulSoup
        2. Get the information of current day's subjects and their timings
        """

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, page_loaded_element)))
        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')  # Parsing through the webpage

        classes = self.soup.find_all('div', {
            "class": classes_info_class_value})  # To be used when there is not information about next day's classes

        periods_information = [[periods.text[0:-13], periods.text[-13:]] for periods in classes]

        print("\nWebpage information successfully extracted\n")

        # Possible that there are no classes today and as the user to close the browser
        if len(periods_information) == 0:
            confirmation = input("It seems to be that there are no classes today. "
                                 "Would you like to close the browser and terminate the script?\n(Y/N): ").lower()
            if confirmation == "n":
                pass
            else:
                self.driver.close()
                exit()

        return periods_information  # Contains the period_name and timings

    @staticmethod
    def display_time_table(periods_info):

        """
        1. Calculate the number of periods in today's session
        2. Create and display the timetable
        """

        table = periods_info  # List of all periods and their timings
        time_table = tabulate(table, headers=["Period Number", "Subject Name", "Timings"], showindex='always',
                              tablefmt="fancy_grid")  # Create the timetable
        print("\nToday's timetable:\n")
        print(time_table)

    @staticmethod
    def get_timings(period_number, periods_info):

        """
        1. Get the current period
        2. Get the period name and period timings
        3. Calculate current time
        4. Get the starting time of the period
        5. Get the ending time of the period
        6. Calculate the duration of the current period
        7. Calculate the time left for the period to start
        8. Create a dictionary of all the time periods
        """

        current_period = periods_info[period_number]  # Get the current period
        period_name = current_period[0]
        period_time = current_period[1]

        now_time = datetime.datetime.now().strftime("%H:%M:%S")  # Get current time
        current_time = datetime.datetime.strptime(now_time, "%H:%M:%S")  # Get current time

        starting_time = datetime.datetime.strptime(period_time[0:5] + ":00", '%H:%M:%S')  # Format starting_time
        ending_time = datetime.datetime.strptime(period_time[8:] + ":00", '%H:%M:%S')  # Format ending_time

        time_left = (starting_time - current_time).total_seconds()  # Get time left for the class to start

        # Calculate period duration
        if time_left <= 0:
            duration = ((ending_time - current_time).total_seconds())
            print("\n" + "=" * 50 + "\n" +
                  "Current Class: " + period_name + "\n" +
                  "Starting Time: " + str(starting_time.time()) + "\n" +
                  "Ending Time: " + str(ending_time.time()) + "\n" +
                  "Class Duration: " + str(round(duration / 60, 2)) + " minute(s)\n" +
                  "Time Left : 0 second(s)")
        else:
            duration = (ending_time - starting_time).total_seconds()
            print("\n" + "=" * 50 + "\n" +
                  "Upcoming Class: " + period_name + "\n" +
                  "Starting Time: " + str(starting_time.time()) + "\n" +
                  "Ending Time: " + str(ending_time.time()) + "\n" +
                  "Class Duration: " + str(round(duration / 60, 2)) + " minute(s)\n" +
                  "Time left for the class to start: ", str(time_left) + " second(s)\n")

        # Creating a dictionary of all the timings and sending it to the join_and_exit_class() function
        timings = {"starting_time": starting_time,
                   "ending_time": ending_time,
                   "duration": duration,
                   "time_left": time_left,
                   "current_class": period_name}

        return timings

    def join_and_exit_class(self, timings):

        """
        1. Open link
        2. Disable camera and microphone
        3. Join the class
        4. Stay till the class ends
        5. Exit the class
        6. Go back to newton classroom
        7. repeat the process
        """

        duration = timings["duration"]
        time_left = timings["time_left"]
        current_class = timings['current_class']

        def join_and_exit_class_sub_func(current_class):
            try:

                time.sleep(2)

                self.driver.find_element_by_xpath(click_current_class).click()

                # Create a list to store  all the classroom links and the current class link
                links = self.driver.find_elements_by_tag_name("a")  # Searching the 'a' tags

                # Get the last link as it is the class link
                classroom_link = [link.get_attribute("href") for link in links][-1]

                print(current_class + " class link: " + str(classroom_link))

                self.driver.get(classroom_link)  # Open the google meet link for the class

                # "//div[@class='uArJ5e UQuaGc Y5sE8d uyXBBb xKiqt']"
                WebDriverWait(self.driver, 120).until(EC.element_to_be_clickable((By.XPATH, join_now_button)))

                self.driver.find_element_by_xpath("//body").send_keys(Keys.CONTROL + "d")  # Disable microphone
                self.driver.find_element_by_xpath("//body").send_keys(Keys.CONTROL + "e")  # Disable camera
                time.sleep(2)

                WebDriverWait(self.driver, 120).until(EC.element_to_be_clickable(
                    (By.XPATH, join_now_button))).click()  # Click on the join button until it is clickable

                print("The class has started. Waiting for the class to end...")

                time.sleep(duration)  # Sleep till the class is finished

                try:
                    self.driver.find_element_by_xpath(exit_class).click()  # Click on the end class button
                    print("Left the class")
                except:
                    self.driver.get("https://griet.newtonclassroom.com/")

                self.driver.get("https://griet.newtonclassroom.com/")  # Go back to the homepage to join the other classes

                print("Redirecting to homepage\n" + "=" * 50 + "\n")
            except NoSuchElementException:
                time.sleep(20)
                join_and_exit_class_sub_func(current_class)

        if time_left > 0:
            print("\nWaiting to join the class. Do not close the browser or the program.")
            time.sleep(time_left)  # Wait till the class is active and then execute the function
            join_and_exit_class_sub_func(current_class)

        elif time_left <= 0:  # Indicates that the class has already started and execute the function immediately
            print("\nThe class has already started. Joining the class now.")

            join_and_exit_class_sub_func(current_class)

    def repeat_process(self, information_periods_info):
        for i in range(len(information_periods_info)):
            timings = my_classroom_bot.get_timings(i, information_periods_info)
            my_classroom_bot.join_and_exit_class(timings)

        print("\n" + "=" * 50 + "\nAll the classes are now over. Closing the browser and program in 45 seconds.")
        time.sleep(45)
        self.driver.close()
        exit()


if __name__ == '__main__':
    my_classroom_bot = NewtonClassroomAutomation()


    my_classroom_bot.open_browser()  # Will open the browser

    my_classroom_bot.auto_update()

    credentials = my_classroom_bot.get_credentials()

    my_classroom_bot.enter_credentials(credentials)

    # Will return a list of all periods and timings
    information_periods = my_classroom_bot.extract_webpage_information()

    my_classroom_bot.display_time_table(information_periods)  # Will display the timetable in a tabular format

    my_classroom_bot.repeat_process(information_periods)
