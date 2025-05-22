from models import CruiseData, ItineraryDay, Cabin
from selenium.webdriver.common.by import By
import time
from utils import wait_for_elements, wait_for_element, wait_for_clickability
from selenium.webdriver.support.ui import  Select


def extract_data(driver, link):
    cruise_data = CruiseData()

    driver.get(link)

    try:
        title = wait_for_element(driver, (By.XPATH, "//h3[contains(@class, 'text-primary my-2 text-gradient cruise-details-package-title dir-ltr ng-star-inserted')]/child::span")).text.strip()
    except:
        title = "N/A"
    finally:
        cruise_data.title = title

    try:
        subtitle = wait_for_element(driver, (By.XPATH, "//span[contains(@class, 'package-subtitle ng-star-inserted')]")).text.strip()
    except:
        subtitle = "N/A"
    finally:
        cruise_data.subtitle = subtitle  

    try:
        shipName = wait_for_element(driver, (By.XPATH, "//span[@data-ody-id='ShipName']")).text.strip()
    except:
        shipName = "N/A"
    finally:
        cruise_data.shipName = shipName

    try:
        destinationName= wait_for_element(driver, (By.XPATH, "//div[@data-ody-id='DestinationName']")).text.strip()
    except:
        destinationName = "N/A"
    finally:
        cruise_data.destinationName = destinationName

    try:
        departureCountry = wait_for_element(driver, (By.XPATH, "//span[@data-ody-id='DepartArrivalText']/span[1]")).text.strip()
    except:
        departureCountry = "N/A"
    finally:
        cruise_data.departureCountry = departureCountry

    try:
        arrivalCountry = wait_for_element(driver, (By.XPATH, "//span[@data-ody-id='DepartArrivalText']/span[2]")).text.strip()
    except:
        arrivalCountry = "N/A"
    finally:
        cruise_data.arrivalCountry = arrivalCountry

    try:
        dates_text_nodes = driver.find_element(By.XPATH, "//div[@data-ody-id='DepartArrivalDate']").text
        dates = [dt for dt in dates_text_nodes.split("\n") if dt]
        depdate, arrdate = dates[0], dates[1]

        departureDate = depdate
        arrivalDate = arrdate
    except:
        departureDate = "N/A"
        arrivalDate = "N/A"
    finally:
        cruise_data.departureDate = departureDate
        cruise_data.arrivalDate = arrivalDate

    try:
        duration = wait_for_element(driver, (By.XPATH, "//div[@data-ody-id='Duration']")).text.strip()
    except:
        duration = "N/A"
    finally:
        cruise_data.duration = duration

    try:
        # All itinerary day nodes
        day_nodes = driver.find_elements(By.XPATH, '//itinerary[@class="col-12 d-block px-0 ng-star-inserted"]//li[@data-ody-id="itinerary-node"]')

        for node in day_nodes:
            # Day number (e.g., "Day 1:") → extract just the number
            day_text = node.find_element(By.XPATH, './/strong[@data-ody-id="CruiseItineraryDayNumber"]').text
            try:
                day_number = int(day_text.replace("Day", "").replace(":", "").strip())
            except:
                day_number = day_number

            # Location name
            location = node.find_element(By.XPATH, './/span[@data-ody-id="ItineraryInfoText"]').text.strip()

            # Date (e.g., "Fri Jun 20, 2025")
            date_full = node.find_element(By.XPATH, './/div[@data-ody-id="ItineraryDatesText"]').text.strip()
            try:
                date = date_full.split('|')[0].strip()
            except:
                date = date_full

            # Departure time (if exists)
            try:
                departure_time = date_full.split('|')[1].strip()
            except IndexError:
                departure_time = None

            # Construct the model
            itinerary_day = ItineraryDay(
                day_number=day_number,
                location=location,
                date=date,
                departure_time=departure_time
            )

            cruise_data.itinerary.append(itinerary_day)
    except Exception as e:
        print(e)
        cruise_data.itinerary = "N/A"
        raise e

    ageInput1 = wait_for_element(driver, (By.XPATH, "//input[@data-ody-id='GuestAge_0']"))
    ageInput1.click()
    ageInput1.clear()
    ageInput1.send_keys("50")

    ageInput2 = wait_for_element(driver, (By.XPATH, "//input[@data-ody-id='GuestAge_1']"))
    ageInput2.click()
    ageInput2.clear()
    ageInput2.send_keys("50")

    time.sleep(2)

    # countrySelect = wait_for_element(driver, (By.XPATH, "//select[@data-select2-id='5']"))
    countrySelect = wait_for_element(driver, (By.XPATH, "(//span[contains(@class, 'select2-selection--single')])[2]"))
    countrySelect.click()

    countryOption = wait_for_clickability(driver, (By.XPATH, "//li[contains(text(), 'AL - Alabama')]"))
    countryOption.click()

    time.sleep(1)

    continueButton = wait_for_element(driver, (By.XPATH, "//button[@data-ody-id='ContinueButton']"))
    continueButton.click()

    try:
        cabinTabs = wait_for_elements(driver, (By.XPATH, "//ul[@id='categoryTabs']/li"))
        for idx, tab in enumerate(cabinTabs):
            tabClick = driver.find_element(By.XPATH, f"//ul[@id='categoryTabs']/li[{idx+1}]")
            tabClick.click()

            print(idx)

            wait_for_element(driver, (By.XPATH, f"//div[contains(@id, 'category_price_content_{idx+1}')]"))

            try:
                cabins_grades = wait_for_elements(driver, (By.XPATH, "//div[contains(@class, 'show active')]//div[@data-ody-id='CategoryContainerView']"))
            except:
                cabins_grades = "N/A"
            
            if len(cabins_grades) == 0:
                cabins_grades = ''

            else:
                for cabin_grade_element in cabins_grades:
                    cabinData = Cabin()

                    try:
                        cabin_type = wait_for_element(driver, (By.XPATH, "//div[contains(@class, 'active')]//strong[@data-ody-id='categoryName']")).text
                    except:
                        cabin_type = "N/A"
                    finally:
                        cabinData.cabinType = cabin_type

                    try:
                        cabinGrade = cabin_grade_element.find_element(By.XPATH, ".//a[@data-ody-id='CabinCode']").text.strip()
                    except:
                        cabinGrade = "N/A"
                    finally:
                        cabinData.grade = cabinGrade

                    try:
                        cabinName = cabin_grade_element.find_element(By.XPATH, ".//span[@data-ody-id='CabinType']").text.strip()
                    except:
                        cabinName = "N/A"
                    finally:
                        cabinData.gradeName = cabinName

                    try:
                        cabinDescription = cabin_grade_element.find_element(By.XPATH, ".//div[@data-ody-id='CategorySectionDescription']").text.strip()
                    except:
                        cabinDescription = "N/A"
                    finally:
                        cabinData.description = cabinDescription

                    try:
                        cabinDeck = cabin_grade_element.find_element(By.XPATH, ".//div[@class='mt-2']").text.replace("Deck(s):", "").strip()
                    except:
                        cabinDeck = "N/A"
                    finally:
                        cabinData.deck = cabinDeck

                    try:
                        cabinPrice = cabin_grade_element.find_element(By.XPATH, ".//strong[@data-ody-id='TotalPrice']").text
                    except:
                        cabinPrice = "N/A"
                    finally:
                        cabinData.price = cabinPrice.replace('$', '').strip()

                    cruise_data.cabins.append(cabinData)

    except Exception as e:
        print(e)
        cruise_data.cabins = "N/A"
        raise e

    return cruise_data