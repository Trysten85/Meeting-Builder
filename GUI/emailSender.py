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