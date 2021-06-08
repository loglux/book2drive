from dvabooking import Driving
import time
if __name__ == '__main__':
    reference = 1234567890
    licence = 123456789
    birth = "11/01/1970"
    dva = Driving()
    # True for headless
    headless = False
    dva.start_chrome(headless)
    dva.first_data(birth, licence, reference)
    steps = 2
    for step in range(steps):
        dva.get_centre(0)
        dva.get_date(step)
        dva.get_notice()
        time.sleep(5)
        if step < steps - 1:
            dva.get_back()
    # uncomment for headless:
    # dva.get_exit()