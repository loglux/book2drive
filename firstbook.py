from dvabooking import Driving
import time
if __name__ == '__main__':
    licence = 12345678900
    birth = "10/01/1900"
    dva = Driving()
    # True for headless
    headless = False
    dva.start_chrome(headless)
    dva.first_data(birth, licence)
    steps = 5
    for step in range(steps):
        dva.get_centre(0)
        dva.get_date(step)
        dva.get_notice()
        time.sleep(5)
        if step < steps - 1:
            dva.get_back()
    # uncomment for headless mode:
    #dva.get_exit()