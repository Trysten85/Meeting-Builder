import smtplib
from email.message import EmailMessage
def send_email(subject, body, sender_email, sender_password, recipient_emails):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = ', '.join(recipient_emails)  # Join multiple emails into a single string
    msg.set_content(body)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        print("Meeting details sent successfully.")
    except Exception as e:
        print("An issue occured while attempting to send email:", e)
# example using the function
# email_list = ["trysten@example.com", "mariam@example.com", "zache@example.com"] #list will be created from particiant emails
# send_email(
#     subject="Team Meeting",
#     body="Reminder: Team meeting at 10am tomorrow.",  #will need to use the calculated best time here as
#     sender_email="your_email@gmail.com",
#     sender_password="your_app_password",  # use an app password if Gmail has 2FA
#     recipient_emails=email_list
# )

# meeting_time_app.py
# Prototype: Single-user Meeting Time App
# Data structure to hold participant availability
data = []
def enter_availability():
    print("Enter participant availability data")
    while True:
        name = input("Enter participant name (or 'done' to finish): ")
        if name.lower() == 'done':
            break
        best_times = input("Enter best times (comma-separated, e.g. 9-10am,2-3pm): ")
        worst_times = input("Enter worst times (comma-separated, e.g. 12-1pm,4-5pm): ")
        email = input("Enter participants email address: ")
        participant = {
            'name': name,
            'best_times': [t.strip() for t in best_times.split(',')],
            'worst_times': [t.strip() for t in worst_times.split(',')],
            'email': email,
        }
        data.append(participant)
        
def calculate_best_time():
    # create an empty dictionary to count votes for the best_times
    print("\nCalculating best time...")
    time_counter = {}
    for participant in data:
        for time in participant['best_times']:
            time_counter[time] = time_counter.get(time, 0) + 1
    # Convert the dictionary items into a sorted tuple in decending order with the most votes 
    # as the first item, then print the result
    sorted_times = sorted(time_counter.items(), key=lambda x: x[1], reverse=True)
    if sorted_times:
        print("Suggested time: ", sorted_times[0][0], "with", sorted_times[0][1], "votes")
    else:
        print("No times entered.")
import smtplib
from email.message import EmailMessage
def send_email(subject, body, sender_email, sender_password, recipient_emails):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = ', '.join(recipient_emails)  # Join multiple emails into a single string
    msg.set_content(body)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        print("Meeting details sent successfully.")
    except Exception as e:
        print("An issue occured while attempting to send email:", e)
# example using the function
# email_list = ["trysten@example.com", "mariam@example.com", "zache@example.com"] #list will be created from particiant emails
# send_email(
#     subject="Team Meeting",
#     body="Reminder: Team meeting at 10am tomorrow.",  #will need to use the calculated best time here as
#     sender_email="your_email@gmail.com",
#     sender_password="your_app_password",  # use an app password if Gmail has 2FA
#     recipient_emails=email_list
# )
def main():
    print("=== Meeting Time App Prototype ===")
    enter_availability()
    calculate_best_time()
    email_list = []
    for participant in data:
        email_list.append(participant['email'])
    host_password = 'epaquxrgnxtfrtgl'
    host_email = 'examplestudent8888@gmail.com'
    body = "A team meeting has been scheduled for " + meeting_time
    send_email("Team meeting", body, host_email, host_password, email_list)
if __name__ == "__main__":
    main()