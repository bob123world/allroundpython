import calendar
import os
import platform
import sys
import urllib.request
import json

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# -------------------------------------------------------------
# -------------------------------------------------------------

# Global Variables

driver = None

# whether to download photos or not
download_uploaded_photos = True
download_friends_photos = True

# whether to download the full image or its thumbnail (small size)
# if small size is True then it will be very quick else if its false then it will open each photo to download it
# and it will take much more time
friends_small_size = True
photos_small_size = True

total_scrolls = 2500
current_scrolls = 0
scroll_time = 8

old_height = 0
firefox_profile_path = "/home/zeryx/.mozilla/firefox/0n8gmjoz.bot"
facebook_https_prefix = "https://"


CHROMEDRIVER_BINARIES_FOLDER = "frank/modules/facebook-scraper/chromedriver"

# -------------------------------------------------------------
# -------------------------------------------------------------


def check_height():
    new_height = driver.execute_script("return document.body.scrollHeight")
    return new_height != old_height


# -------------------------------------------------------------
# -------------------------------------------------------------

# helper function: used to scroll the page
def scroll():
    global old_height
    current_scrolls = 0

    while True:
        try:
            if current_scrolls == total_scrolls:
                return

            old_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(driver, scroll_time, 0.05).until(
                lambda driver: check_height()
            )
            current_scrolls += 1
        except TimeoutException:
            break

    return

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


def create_original_link(url):
    if url.find(".php") != -1:
        original_link = facebook_https_prefix + ".facebook.com/" + ((url.split("="))[1])

        if original_link.find("&") != -1:
            original_link = original_link.split("&")[0]

    elif url.find("fnr_t") != -1:
        original_link = (
            facebook_https_prefix
            + ".facebook.com/"
            + ((url.split("/"))[-1].split("?")[0])
        )
    elif url.find("_tab") != -1:
        original_link = (
            facebook_https_prefix
            + ".facebook.com/"
            + (url.split("?")[0]).split("/")[-1]
        )
    else:
        original_link = url

    return original_link


# -------------------------------------------------------------
# -------------------------------------------------------------


def save_to_file(name, elements, status, current_section):
    """helper function used to save links to files"""

    # status 0 = dealing with friends list
    # status 1 = dealing with photos
    # status 2 = dealing with videos
    # status 3 = dealing with about section
    # status 4 = dealing with posts

    try:
        f = None  # file pointer

        if status != 4:
            f = open(name, "w", encoding="utf-8", newline="\r\n")

        results = []
        img_names = []

        # dealing with Friends
        if status == 0:
            # get profile links of friends
            results = [x.get_attribute("href") for x in elements]
            results = [create_original_link(x) for x in results]

            # get names of friends
            people_names = [
                x.find_element_by_tag_name("img").get_attribute("aria-label")
                for x in elements
            ]

            # download friends' photos
            try:
                if download_friends_photos:
                    if friends_small_size:
                        img_links = [
                            x.find_element_by_css_selector("img").get_attribute("src")
                            for x in elements
                        ]
                    else:
                        links = []
                        for friend in results:
                            try:
                                driver.get(friend)
                                WebDriverWait(driver, 30).until(
                                    EC.presence_of_element_located(
                                        (By.CLASS_NAME, "profilePicThumb")
                                    )
                                )
                                l = driver.find_element_by_class_name(
                                    "profilePicThumb"
                                ).get_attribute("href")
                            except Exception:
                                l = "None"

                            links.append(l)

                        for i, _ in enumerate(links):
                            if links[i] is None:
                                links[i] = "None"
                            elif links[i].find("picture/view") != -1:
                                links[i] = "None"

                        img_links = get_facebook_images_url(links)

                    folder_names = [
                        "Friend's Photos",
                        "Mutual Friends' Photos",
                        "Following's Photos",
                        "Follower's Photos",
                        "Work Friends Photos",
                        "College Friends Photos",
                        "Current City Friends Photos",
                        "Hometown Friends Photos",
                    ]
                    print("Downloading " + folder_names[current_section])

                    img_names = image_downloader(
                        img_links, folder_names[current_section]
                    )
                else:
                    img_names = ["None"] * len(results)
            except Exception:
                print(
                    "Exception (Images)",
                    str(status),
                    "Status =",
                    current_section,
                    sys.exc_info()[0],
                )

        # dealing with About Section
        elif status == 3:
            results = elements[0].text
            f.writelines(results)

        """Write results to file"""
        if status == 0:
            for i, _ in enumerate(results):
                # friend's profile link
                f.writelines(results[i])
                f.write(",")

                # friend's name
                f.writelines(people_names[i])
                f.write(",")

                # friend's downloaded picture id
                f.writelines(img_names[i])
                f.write("\n")


        f.close()

    except Exception:
        print("Exception (save_to_file)", "Status =", str(status), sys.exc_info()[0])

    return


# ----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


def scrape_data(user_id, scan_list, section, elements_path, save_status, file_names):
    """Given some parameters, this function can scrap friends/photos/videos/about/posts(statuses) of a profile"""
    page = []

    if save_status == 4:
        page.append(user_id)

    page += [user_id + s for s in section]

    for i, _ in enumerate(scan_list):
        try:
            driver.get(page[i])

            if (
                (save_status == 0) or (save_status == 1) or (save_status == 2)
            ):  # Only run this for friends, photos and videos

                # the bar which contains all the sections
                sections_bar = driver.find_element_by_xpath(
                    "//*[@class='_3cz'][1]/div[2]/div[1]"
                )

                if sections_bar.text.find(scan_list[i]) == -1:
                    continue

            if save_status != 3:
                scroll()

            data = driver.find_elements_by_xpath(elements_path[i])

            save_to_file(file_names[i], data, save_status, i)

        except Exception:
            print(
                "Exception (scrape_data)",
                str(i),
                "Status =",
                str(save_status),
                sys.exc_info()[0],
            )
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def create_folder(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)


def scrape_profile(url):
    folder = os.path.join(os.getcwd(), "data")
    create_folder(folder)
    os.chdir(folder)

    # execute for all profiles given in input.txt file
    driver.get(url)
    url = driver.current_url
    user_id = create_original_link(url)

    print("\nScraping:", user_id)

    try:
        target_dir = os.path.join(folder, user_id.split("/")[-1])
        create_folder(target_dir)
        os.chdir(target_dir)
    except Exception:
        print("Some error occurred in creating the profile directory.")

    # ----------------------------------------------------------------------------
    print("----------------------------------------")
    print("Friends..")
    # Name, fblink, email, telephone number, birthdate, number of friends, number of mutual friends, living place, work/school

    try:
        f = open(os.path.join(folder, "friends.txt"), "w", encoding="utf-8", newline="\r\n")

        driver.get(user_id + "/friends")

        sections_bar = driver.find_element_by_xpath("//*[@class='_3cz'][1]/div[2]/div[1]")
        scroll()

        elements = driver.find_element_by_xpath("//*[contains(@id,'pagelet_timeline_medley_friends')][1]/div[2]/div/ul/li/div/a")

        results = []

        results = [x.get_attribute("href") for x in elements]
        results = [create_original_link(x) for x in results]

        # get names of friends
        people_names = [
            x.find_element_by_tag_name("img").get_attribute("aria-label")
            for x in elements
        ]

        for i, _ in enumerate(results):
            # friend's profile link
            f.writelines(people_names[i])
            f.write(",")

            # friend's name
            f.writelines(results[i])
            f.write("\n")

        print("Friends Done!")
        print("----------------------------------------")
    # print("About:")
    # # setting parameters for scrape_data() to scrap the about section
    # scan_list = [None] * 7
    # section = [
    #     "/about?section=overview",
    #     "/about?section=education",
    #     "/about?section=living",
    #     "/about?section=contact-info",
    #     "/about?section=relationship",
    #     "/about?section=bio",
    #     "/about?section=year-overviews",
    # ]
    # elements_path = [
    #     "//*[contains(@id, 'pagelet_timeline_app_collection_')]/ul/li/div/div[2]/div/div"
    # ] * 7
    # file_names = [
    #     "Overview.txt",
    #     "Work and Education.txt",
    #     "Places Lived.txt",
    #     "Contact and Basic Info.txt",
    #     "Family and Relationships.txt",
    #     "Details About.txt",
    #     "Life Events.txt",
    # ]
    # save_status = 3

    # scrape_data(user_id, scan_list, section, elements_path, save_status, file_names)
    # print("About Section Done!")

    except Exception as e:
        print(e)


    print("\nProcess Completed.")

    return


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


def safe_find_element_by_id(driver, elem_id):
    try:
        return driver.find_element_by_id(elem_id)
    except NoSuchElementException:
        return None

def login(email, password):
    """ Logging into our own profile """

    try:
        global driver

        options = Options()

        #  Code to disable notifications pop up of Chrome Browser
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--mute-audio")
        # options.add_argument("headless")

        try:
            platform_ = platform.system().lower()
            chromedriver_versions = {
                "linux": os.path.join(
                    os.getcwd(), CHROMEDRIVER_BINARIES_FOLDER, "chromedriver_linux64",
                ),
                "darwin": os.path.join(
                    os.getcwd(), CHROMEDRIVER_BINARIES_FOLDER, "chromedriver_mac64",
                ),
                "windows": os.path.join(
                    os.getcwd(), CHROMEDRIVER_BINARIES_FOLDER, "chromedriver_win32.exe",
                ),
            }

            driver = webdriver.Chrome(
                executable_path=chromedriver_versions[platform_], options=options
            )
        except Exception:
            print(
                "Kindly replace the Chrome Web Driver with the latest one from "
                "http://chromedriver.chromium.org/downloads "
                "and also make sure you have the latest Chrome Browser version."
                "\nYour OS: {}".format(platform_)
            )
            exit(1)

        fb_path = facebook_https_prefix + "facebook.com"
        driver.get(fb_path)
        driver.maximize_window()

        # filling the form
        driver.find_element_by_name("email").send_keys(email)
        driver.find_element_by_name("pass").send_keys(password)

        try:
            # clicking on login button
            driver.find_element_by_id("loginbutton").click()
        except NoSuchElementException:
            # Facebook new design
            driver.find_element_by_name("login").click()

        # if your account uses multi factor authentication
        mfa_code_input = safe_find_element_by_id(driver, "approvals_code")

        if mfa_code_input is None:
            return

        mfa_code_input.send_keys(input("Enter MFA code: "))
        driver.find_element_by_id("checkpointSubmitButton").click()

        # there are so many screens asking you to verify things. Just skip them all
        while safe_find_element_by_id(driver, "checkpointSubmitButton") is not None:
            dont_save_browser_radio = safe_find_element_by_id(driver, "u_0_3")
            if dont_save_browser_radio is not None:
                dont_save_browser_radio.click()

            driver.find_element_by_id("checkpointSubmitButton").click()

    except Exception:
        print("There's some error in log in.")
        print(sys.exc_info()[0])
        exit(1)

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


def main():
    try:
        ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

        with open(os.path.join(ROOT_DIR,"frank","config.json"), "r") as file:
            config = json.load(file)
    except Exception as e:
        print(e)
        exit()

    if "facebook" not in config:
        print("Your facebook email or password is missing. Kindly write them in config.json")
        exit(1)
        if "email" not in config["facebook"]:
            pass
        if "password" not in config["facebook"]:
            pass

    login(config["facebook"]["email"], config["facebook"]["password"])
    scrape_profile(config["facebook"]["url"])
    driver.close

# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------

if __name__ == "__main__":
    # get things rolling
    main()