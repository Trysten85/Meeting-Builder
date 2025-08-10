🚀 How to Run
Launch the application:
Open GUI.py to run the application.

🔧 How It Works
1. Main Interface (GUI.py)

Loads the Qt Designer UI from main_window.ui
Provides table interface for entering participant availability
Three main buttons: Add User, Calculate, Export

2. User Input

Add User: Creates new rows for participant data
Time Selection: Dual dropdown menus (Start Time - End Time) for Day One and Day Two
Editable Names: Click on user names to customize them

3. Meeting Calculation (meeting_calculator.py)

Converts GUI time ranges into hourly time slots
Tracks participant availability separately for Day One and Day Two
Finds most popular time slots using voting algorithm
Handles ties by showing all equally popular times

4. Results Display

Shows best meeting times for both days in results table
Displays vote counts for transparency
Auto-resizes and centers results table

5. Email Export (export_dialog.py + mail_calc.py)

Export Button: Opens email composition dialog
Pre-filled Content: Automatically generates meeting invitation with:

Calculated best meeting times
Participant list
Professional meeting invitation format


Email Sending: Uses Gmail SMTP to send invitations to all participants

💡 Usage Example

Launch: Run python GUI.py
Add Participants: Click "Add User" for each team member
Set Availability: Use dropdowns to select each person's available times
Calculate: Click "Calculate" to find optimal meeting times
Export: Click "Export" to send email invitations

⚙️ Technical Details
Time Processing

Converts time ranges (e.g., "9:00 AM - 2:00 PM") into hourly slots
Handles 12/24 hour time conversion automatically
Sorts time slots chronologically for clean output

Voting Algorithm

Each participant "votes" for their available time slots
Algorithm finds time slots with maximum votes
Handles ties by showing all equally popular options
Separate calculations for Day One and Day Two

Email Integration

Uses Gmail SMTP with SSL encryption
Supports multiple recipients
Generates professional meeting invitations
Includes participant availability summary

🔒 Security Notes

Email credentials are handled securely through Gmail app passwords
No passwords are stored permanently in the application
SMTP connection uses SSL encryption

🛠️ Customization

Time Options: Modify time lists in add_time_dropdown() method
Email Template: Edit generate_email_body() in export_dialog.py
UI Layout: Modify main_window.ui with Qt Designer
Calculation Logic: Extend algorithms in meeting_calculator.py

📧 Email Setup
To use email functionality:

Enable 2-factor authentication on your Gmail account
Generate an app password for this application
Enter your Gmail address and app password in the export dialog