# Tulane Class Schedule Web Scraper
This Python script allows you to automatically check for available seats in a given class.
When ran, it will ask for the course ID and the last name of the professor that teaches that given course. It also asks for how many searches you'd like to execute at the same time which is made possible through multi-threading.

Hard Limitations:
Due to the nature of the web scraper, this does not entirely work for courses that contain many sections to the point where the class schedule's site generates a second page
Known courses that this limitation affects: SPAN2030
