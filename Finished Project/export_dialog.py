"""
Export Dialog for GUI - Uses classmate's email code
This file handles the GUI for sending emails, keeping it separate from the main GUI
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QTextEdit, QMessageBox)
from mail_calc import send_email  # Import from mail_calc.py


class ExportDialog(QDialog):
    """Email export dialog that uses your classmate's send_email function"""
    
    def __init__(self, day_one_result, day_two_result, participants_data, parent=None):
        super().__init__(parent)
        self.day_one_result = day_one_result
        self.day_two_result = day_two_result
        self.participants_data = participants_data
        self.setup_ui()
    
    def setup_ui(self):
        """Create the export dialog UI"""
        self.setWindowTitle("Export Meeting Results")
        self.setGeometry(200, 200, 500, 600)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("📧 Send Meeting Results")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Email settings (using defaults)
        email_section = QLabel("Email Configuration:")
        email_section.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(email_section)
        
        # Sender email
        sender_layout = QHBoxLayout()
        sender_layout.addWidget(QLabel("From:"))
        self.sender_email = QLineEdit()
        self.sender_email.setText("examplestudent8888@gmail.com")  
        sender_layout.addWidget(self.sender_email)
        layout.addLayout(sender_layout)
        
        # Password
        password_layout = QHBoxLayout()
        password_layout.addWidget(QLabel("Password:"))
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setText("epaquxrgnxtfrtgl")  
        password_layout.addWidget(self.password)
        layout.addLayout(password_layout)
        
        # Recipients
        recipients_label = QLabel("Recipients (one email per line):")
        recipients_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(recipients_label)
        
        self.recipients = QTextEdit()
        self.recipients.setMaximumHeight(100)
        # Generate placeholder emails based on participant names
        placeholder_emails = []
        for person in self.participants_data:
            name = person['name'].lower().replace(' ', '')
            placeholder_emails.append(f"{name}@example.com")
        self.recipients.setPlainText("\n".join(placeholder_emails))
        layout.addWidget(self.recipients)
        
        # Email content
        content_label = QLabel("Email Content:")
        content_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(content_label)
        
        # Subject
        subject_layout = QHBoxLayout()
        subject_layout.addWidget(QLabel("Subject:"))
        self.subject = QLineEdit()
        self.subject.setText("Team meeting")  # Matches classmate's subject
        subject_layout.addWidget(self.subject)
        layout.addLayout(subject_layout)
        
        # Body
        body_label = QLabel("Message:")
        layout.addWidget(body_label)
        
        self.body = QTextEdit()
        self.body.setPlainText(self.generate_email_body())
        layout.addWidget(self.body)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        send_btn = QPushButton("Send Email")
        send_btn.clicked.connect(self.send_email)
        send_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(send_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def generate_email_body(self):
        """Create email body with meeting results"""
        # Start with basic message similar to classmate's format
        body_lines = []
        
        # Add meeting times
        if self.day_one_result and self.day_one_result != "No day one times selected":
            body_lines.append(f"Day One meeting time: {self.day_one_result}")
        
        if self.day_two_result and self.day_two_result != "No day two times selected":
            body_lines.append(f"Day Two meeting time: {self.day_two_result}")
        
        if not body_lines:
            body_lines.append("Meeting time: TBD")
        
        # Add main message (similar to classmate's format)
        main_message = "A team meeting has been scheduled."
        if body_lines:
            main_message += "\n\nScheduled times:\n" + "\n".join(body_lines)
        
        # Add participants
        main_message += "\n\nParticipants:\n"
        for person in self.participants_data:
            main_message += f"• {person['name']}\n"
        
        main_message += "\nPlease confirm your attendance."
        
        return main_message
    
    def send_email(self):
        """Send email using classmate's send_email function"""
        # Get form data
        subject = self.subject.text().strip()
        body = self.body.toPlainText()
        sender_email = self.sender_email.text().strip()
        password = self.password.text().strip()
        
        # Get recipients
        recipients_text = self.recipients.toPlainText().strip()
        recipient_emails = [email.strip() for email in recipients_text.split('\n') if email.strip()]
        
        # Validate
        if not all([subject, body, sender_email, password]):
            QMessageBox.warning(self, "Missing Information", "Please fill in all fields.")
            return
        
        if not recipient_emails:
            QMessageBox.warning(self, "No Recipients", "Please enter at least one email address.")
            return
        
        try:
            # Use classmate's send_email function EXACTLY as they wrote it
            send_email(subject, body, sender_email, password, recipient_emails)
            
            # Show success message
            QMessageBox.information(self, "Success", 
                                  f"Email sent successfully to {len(recipient_emails)} recipients!")
            self.accept()  # Close dialog
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to send email: {e}")


def open_export_dialog(day_one_result, day_two_result, participants_data, parent=None):
    """
    Convenience function to open the export dialog
    
    Args:
        day_one_result: string with day one meeting result
        day_two_result: string with day two meeting result  
        participants_data: list of participant dictionaries
        parent: parent widget
    
    Returns:
        True if email was sent, False if cancelled
    """
    dialog = ExportDialog(day_one_result, day_two_result, participants_data, parent)
    result = dialog.exec_()
    return result == QDialog.Accepted