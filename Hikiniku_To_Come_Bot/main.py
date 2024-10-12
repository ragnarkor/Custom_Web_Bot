### Main script to run the booking process
from datetime import datetime, date, timedelta
import undetected_chromedriver as uc
from booking import Booking
import yaml

# surname: "Chan"
# first_name: "Tai Man"
# gender: M
# phone: 60897654
# email: "taimanchan@gmail.com"
# credit_card_num: 4006161316299193
# expired_date: 022028
# cvv: 643

def _load_yml(yml_path):

    with open(yml_path, "r") as file:
        booker_info = yaml.safe_load(file)

    return booker_info

def _IsValidTimeSlot(time_slot_list:str) -> bool:

    if not isinstance(time_slot_list, list):
        raise TypeError("Please input a list")

    time_format = "%H%M"

    for time_slot in time_slot_list:
        time_fstr = datetime.strptime(time_slot, time_format)
        StartTime = datetime.strptime("1100", time_format)
        EndTime = datetime.strptime("2115", time_format)

        if not StartTime <= time_fstr <= EndTime:
            raise Exception(f"Time Slot: {time_fstr.strftime(time_format)} exceed the range 11:00 - 21:15")

    return True

def main(
    options_list:list,
    keep_alive:bool = False,
    url:str = None,
    selected_date:str = None,
    party_size: int = 2,
    time_slot_list:list = []
):
    
    assert 0 < party_size < 5, "Party Size exceed the range 1 - 4"
    assert _IsValidTimeSlot(time_slot_list), "Invalid time slot"

    options = uc.ChromeOptions()
    if options_list:
        for setting in options_list:
            options.add_argument(setting)

    ### KeepAlive: Determine if the browser keep or not after run the script.
    driver = uc.Chrome(options=options,
                    enable_cdp_events=keep_alive)
    driver.get(url)

    booker_info = _load_yml(r"C:\web_bot\Web_Bot\Hikiniku_To_Come_Bot\booker_info.yml")

    bot = Booking(driver)

    bot.select_partysize(party_size)

    bot.select_date(selected_date)

    for time_slot in time_slot_list:
        bot.select_time_slot(time_slot)
        bot.payment(booker_info)


if __name__ == "__main__":

    url = "https://inline.app/booking/-NxpjjSJhxwTw6cV0Lm3:inline-live-3/-Nxpjjmuxwpudr9s2kHN"

    PartySize = 1
    selected_date = date.today() + timedelta(days=7)
    # TimeSlot = ["17-00", "18-00", "21-00", "21-15"]
    TimeSlot = ["1700"]

    options_list = ["--disable-gpu",
                    "--user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"]

    main(options_list, True, url, selected_date, PartySize, TimeSlot)