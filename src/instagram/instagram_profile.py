from .instagram_base import BaseInstagramScraper
from config import Config as config
from ..logs import Logs
from ..facebook.scroll import scroll_page_callback
from selenium.webdriver.common.by import By
from rich import print as rprint
from ..utils import output, save_to_json
from selenium.webdriver.support import expected_conditions as EC
from config import Config

logs = Logs()


class ProfileScraper(BaseInstagramScraper):
    def __init__(self, user_id: str) -> None:
        super().__init__(
            user_id, base_url=f"https://www.instagram.com/{user_id}/")
        self.success = False
        self._driver.add_cookie(
            {
                "name": "sessionid",
                "value": config.INSTAGRAM_SESSIONID_VALUE,
                "domain": ".instagram.com",
            }
        )
        self._refresh_driver()

    def _refresh_driver(self) -> None:
        """Load cookies and refresh driver"""
        self._driver.refresh()
    
    def extract_videos(self):
        extracted_video_urls = []
        print("Extracting videos...")
        try:
            def extract_callback(driver):
                # Click to reels tab
                reels_tab = self._driver.find_element(
                    By.XPATH, "//a[contains(@href, '/reels/')]"
                )
                reels_tab.click()
                # Wait for the page to load
                self._wait.until(
                    EC.presence_of_all_elements_located(
                        (By.TAG_NAME, "a")
                    )
                )
                # Find all video elements
                video_elements = self._driver.find_elements(By.TAG_NAME, "a")
                print(f"Found {len(video_elements)} video tags")
                for video_element in video_elements:
                    src_attribute = video_element.get_attribute("href")
                    if src_attribute and src_attribute not in extracted_video_urls and "/reel/" in src_attribute:
                        rprint(f"Extracted video URL: {src_attribute}")
                        extracted_video_urls.append(src_attribute)

            scroll_page_callback(self._driver, extract_callback)

        except Exception as e:
            logs.log_error(f"An error occurred while extracting videos: {e}")

        print(f"Extracted {len(extracted_video_urls)} video URLs")
        return extracted_video_urls

  

    def pipeline_videos(self) -> None:
        """
        Pipeline to scrape videos
        """
        try:
            rprint(f"[bold]Step 1 of 2 - Loading profile page[/bold]")
            video_urls = self.extract_videos()

            if not video_urls:
                output.print_no_data_info()
                self._driver.quit()
                self.success = False
            else:
                rprint(
                    f"[bold]Step 2 of 2 - Downloading and saving videos [/bold]")

                rprint(
                    "[bold red]Don't close the app![/bold red] Saving scraped data to database, it can take a while!"
                )

                # save_to_json.SaveJSON(self._user_id, video_urls).save()

                with open(Config.INSTAGRAM_FILE_PATH, 'w', encoding='utf-8') as f:
                    video_urls.sort()
                    for item in video_urls:
                        f.write(f"{item}\n")

                self._driver.quit()
                self.success = True

        except Exception as e:
            logs.log_error(f"An error occurred: {e}")
            rprint(f"An error occurred {e}")

        finally:
            self._driver.quit()
