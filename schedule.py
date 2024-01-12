from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime
import urllib
import time
import threading

# Single lock for synchronization
print_lock = threading.Lock()

def find_indices(lst, target):
    return [i for i, elem in enumerate(lst) if elem == target]

def process_course(class_id, prof_last_name):
    while True:
        while True:
            try:
                html = urlopen(f"https://classschedule.tulane.edu/Results.aspx?course={class_id}").read()
                break
            except urllib.error.URLError:
                print("\n\033[91mA connection error has occurred. Retrying in 60 seconds...\033[0m")
                time.sleep(60)
            
        soup = BeautifulSoup(html, features='html.parser')

        text = [chunk.lower() for chunk in soup.get_text().split()]

        result_prof_indices = find_indices(text, prof_last_name)
        result_seat_indices = find_indices(text, "avail.")

        with print_lock:
            formatted_datetime = datetime.now().strftime("%I:%M:%S%p %m/%d/%Y")
            print(f"\nChecking... {formatted_datetime}")

        seat_indices = [seat_i for prof_i in result_prof_indices for seat_i in result_seat_indices if seat_i > prof_i]

        if not result_prof_indices:
            with print_lock:
                print(f"{prof_last_name[:-1].capitalize()} does not teach {class_id.upper()}.")
            exit()

        for prof_i, seat_i in zip(result_prof_indices, seat_indices):
            available_seats = int(text[seat_i + 2])
            color_code = "\033[91m" if available_seats == 0 else "\033[92m"
            reset_color = "\033[0m"
            word = "seat" if available_seats == 1 else "seats"
            with print_lock:
                print(f"{class_id.upper()} - {text[prof_i].capitalize()} {text[prof_i + 1].capitalize()} - {color_code}{available_seats} available {word}{reset_color} on {text[seat_i + 8].upper()} at {text[seat_i + 9].upper()}.")

        time.sleep(30)

# Input for the number of occurrences
while True:
    try:
        num_occurrences = int(input("Enter the number of searches you would like to do: "))
        if num_occurrences > 0:
            break
        else:
            print("Please enter a positive integer.")
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

# Input for each thread
thread_info = []
for i in range(num_occurrences):
    class_id = input(f"Enter the course ID for lookup #{i+1} (format: XXXX1234): ").lower()
    prof_last_name = input(f"Enter the last name of the professor for lookup #{i+1}: ").lower() + ","
    thread_info.append((class_id, prof_last_name))

# Create threads
threads = [threading.Thread(target=process_course, args=info) for info in thread_info]

# Start threads
for thread in threads:
    thread.start()

# Wait for threads to finish
for thread in threads:
    thread.join()