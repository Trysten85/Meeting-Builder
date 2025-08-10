from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableWidgetItem, 
                           QLineEdit, QHeaderView, QComboBox, QWidget, QHBoxLayout, QLabel)
import sys

# Import the meeting calculation functions
import meeting_calculator


class EditableHeaderView(QHeaderView):
    """Custom header view that allows editing of vertical headers"""
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.line_edit = None
        self.editing_section = -1

    def mouseDoubleClickEvent(self, event):
        """Handle double-click on header to start editing"""
        if self.orientation() == Qt.Vertical:
            section = self.logicalIndexAt(event.pos())
            if section >= 0:
                self.start_editing(section)

    def start_editing(self, section):
        """Start editing a header section"""
        if self.line_edit is not None:
            self.line_edit.hide()
            
        self.editing_section = section
        rect = self.sectionViewportPosition(section)
        size = self.sectionSize(section)
        
        self.line_edit = QLineEdit(self.parent())
        self.line_edit.setText(self.model().headerData(section, self.orientation(), Qt.DisplayRole))
        self.line_edit.setGeometry(0, rect, self.width(), size)
        self.line_edit.show()
        self.line_edit.setFocus()
        self.line_edit.selectAll()
        
        # Connect signals
        self.line_edit.editingFinished.connect(self.finish_editing)
        self.line_edit.returnPressed.connect(self.finish_editing)

    def finish_editing(self):
        """Finish editing and update the header"""
        if self.line_edit and self.editing_section >= 0:
            new_text = self.line_edit.text()
            # Update the header text
            item = QTableWidgetItem(new_text)
            self.parent().setVerticalHeaderItem(self.editing_section, item)
            
            self.line_edit.hide()
            self.line_edit = None
            self.editing_section = -1


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main_window.ui", self)  # Load the UI file

        # Track how many users are in the table
        self.user_count = 0

        # Connect buttons
        self.pushButton.clicked.connect(self.add_user)        # Add User
        self.pushButton_2.clicked.connect(self.calculate_best_times)  # Calculate

        # Configure main table
        self.tableWidget.setEditTriggers(
            self.tableWidget.DoubleClicked | 
            self.tableWidget.EditKeyPressed | 
            self.tableWidget.AnyKeyPressed
        )

        # Lock the results table
        self.tableWidget_2.setEditTriggers(self.tableWidget_2.NoEditTriggers)

        # Set column widths
        self.tableWidget.setColumnWidth(0, 120)  # User Name
        self.tableWidget.setColumnWidth(1, 200)  # Day One Times
        self.tableWidget.setColumnWidth(2, 200)  # Day Two Times
        
        # Configure results table
        self.tableWidget_2.resizeColumnsToContents()
        self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Load test data for development
        self.load_test_data()

    def load_test_data(self):
        """Load sample users and times for testing - remove this for production"""
        test_users = [
            {"name": "Alice", "day1_start": "9:00 AM", "day1_end": "12:00 PM", "day2_start": "1:00 PM", "day2_end": "4:00 PM"},
            {"name": "Bob", "day1_start": "10:00 AM", "day1_end": "2:00 PM", "day2_start": "Start", "day2_end": "End"},
            {"name": "Charlie", "day1_start": "Start", "day1_end": "End", "day2_start": "9:00 AM", "day2_end": "11:00 AM"},
            {"name": "Diana", "day1_start": "11:00 AM", "day1_end": "3:00 PM", "day2_start": "2:00 PM", "day2_end": "5:00 PM"},
        ]
        
        for user_data in test_users:
            self.add_user()
            row = self.user_count - 1
            
            # Set user name
            self.tableWidget.item(row, 0).setText(user_data["name"])
            
            # Set day 1 times
            day_one_widget = self.tableWidget.cellWidget(row, 1)
            if day_one_widget:
                start_index = day_one_widget.start_combo.findText(user_data["day1_start"])
                if start_index >= 0:
                    day_one_widget.start_combo.setCurrentIndex(start_index)
                
                end_index = day_one_widget.end_combo.findText(user_data["day1_end"])
                if end_index >= 0:
                    day_one_widget.end_combo.setCurrentIndex(end_index)
            
            # Set day 2 times
            day_two_widget = self.tableWidget.cellWidget(row, 2)
            if day_two_widget:
                start_index = day_two_widget.start_combo.findText(user_data["day2_start"])
                if start_index >= 0:
                    day_two_widget.start_combo.setCurrentIndex(start_index)
                
                end_index = day_two_widget.end_combo.findText(user_data["day2_end"])
                if end_index >= 0:
                    day_two_widget.end_combo.setCurrentIndex(end_index)

    def add_user(self):
        """Add a new user row to the table"""
        row = self.user_count
        self.tableWidget.insertRow(row)

        # Add editable user name
        user_name_item = QTableWidgetItem(f"User {row + 1}")
        user_name_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
        self.tableWidget.setItem(row, 0, user_name_item)
        
        # Add time selection dropdowns
        self.add_time_dropdown(row, 1)  # Day One
        self.add_time_dropdown(row, 2)  # Day Two

        self.user_count += 1

    def add_time_dropdown(self, row, column):
        """Add dual dropdowns (start time - end time) to a specific cell"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)
        
        # Start time dropdown
        start_combo = QComboBox()
        time_options = [
            "Start",
            "8:00 AM", "8:30 AM", "9:00 AM", "9:30 AM", "10:00 AM", "10:30 AM",
            "11:00 AM", "11:30 AM", "12:00 PM", "12:30 PM", "1:00 PM", "1:30 PM",
            "2:00 PM", "2:30 PM", "3:00 PM", "3:30 PM", "4:00 PM", "4:30 PM",
            "5:00 PM", "5:30 PM", "6:00 PM"
        ]
        start_combo.addItems(time_options)
        start_combo.setCurrentIndex(0)
        
        # Dash label
        dash_label = QLabel(" - ")
        dash_label.setAlignment(Qt.AlignCenter)
        
        # End time dropdown
        end_combo = QComboBox()
        end_time_options = [
            "End",
            "8:30 AM", "9:00 AM", "9:30 AM", "10:00 AM", "10:30 AM", "11:00 AM",
            "11:30 AM", "12:00 PM", "12:30 PM", "1:00 PM", "1:30 PM", "2:00 PM",
            "2:30 PM", "3:00 PM", "3:30 PM", "4:00 PM", "4:30 PM", "5:00 PM",
            "5:30 PM", "6:00 PM", "6:30 PM"
        ]
        end_combo.addItems(end_time_options)
        end_combo.setCurrentIndex(0)
        
        # Add to layout
        layout.addWidget(start_combo)
        layout.addWidget(dash_label)
        layout.addWidget(end_combo)
        
        # Store references for later access
        container.start_combo = start_combo
        container.end_combo = end_combo
        
        self.tableWidget.setCellWidget(row, column, container)

    def get_all_selections(self):
        """Extract all user selections from the GUI table"""
        selections = []
        for row in range(self.tableWidget.rowCount()):
            user_name = self.tableWidget.item(row, 0).text() if self.tableWidget.item(row, 0) else f"User {row + 1}"
            
            # Get day one selection
            day_one_widget = self.tableWidget.cellWidget(row, 1)
            if day_one_widget and hasattr(day_one_widget, 'start_combo'):
                day_one_start = day_one_widget.start_combo.currentText()
                day_one_end = day_one_widget.end_combo.currentText()
                if day_one_start != "Start" and day_one_end != "End":
                    day_one_time = f"{day_one_start} - {day_one_end}"
                else:
                    day_one_time = "Not selected"
            else:
                day_one_time = "Not selected"
            
            # Get day two selection
            day_two_widget = self.tableWidget.cellWidget(row, 2)
            if day_two_widget and hasattr(day_two_widget, 'start_combo'):
                day_two_start = day_two_widget.start_combo.currentText()
                day_two_end = day_two_widget.end_combo.currentText()
                if day_two_start != "Start" and day_two_end != "End":
                    day_two_time = f"{day_two_start} - {day_two_end}"
                else:
                    day_two_time = "Not selected"
            else:
                day_two_time = "Not selected"
            
            selections.append({
                'user': user_name,
                'day_one': day_one_time,
                'day_two': day_two_time
            })
        
        return selections

    def calculate_best_times(self):
        """Calculate the best meeting times using the imported algorithm"""
        user_data = self.get_all_selections()
        
        # Print debug info
        print("=== Meeting Time Picker (GUI Version) ===")
        print("Participant availability:")
        for user in user_data:
            print(f"Name: {user['user']}")
            print(f"  Day 1: {user['day_one']}")
            print(f"  Day 2: {user['day_two']}")
        
        try:
            # Use the imported calculation function
            day_one_result, day_two_result = meeting_calculator.calculate_separate_day_times(user_data)
            
            # Display results
            self.display_results(day_one_result, day_two_result)
            
            # Print to console
            print(f"\nBest Day One meeting time: {day_one_result}")
            print(f"Best Day Two meeting time: {day_two_result}")
            
            # Print debug info from the calculator
            meeting_calculator.print_debug_info()
            
        except Exception as e:
            print(f"Error in calculation: {e}")
            self.display_results("Error in calculation", "Error in calculation")

    def display_results(self, day_one_result, day_two_result):
        """Display calculation results in the results table"""
        self.tableWidget_2.setRowCount(1)
        
        # Set the results
        self.tableWidget_2.setItem(0, 0, QTableWidgetItem("Best Times"))
        self.tableWidget_2.setItem(0, 1, QTableWidgetItem(str(day_one_result)))
        self.tableWidget_2.setItem(0, 2, QTableWidgetItem(str(day_two_result)))
        
        # Auto-resize columns
        for col in range(self.tableWidget_2.columnCount()):
            item = self.tableWidget_2.item(0, col)
            if item:
                font_metrics = self.tableWidget_2.fontMetrics()
                text_width = font_metrics.horizontalAdvance(item.text())
                
                header_text = self.tableWidget_2.horizontalHeaderItem(col).text() if self.tableWidget_2.horizontalHeaderItem(col) else ""
                header_width = font_metrics.horizontalAdvance(header_text)
                
                needed_width = max(text_width, header_width) + 40
                self.tableWidget_2.setColumnWidth(col, needed_width)
        
        # Resize and center the results table
        total_width = sum(self.tableWidget_2.columnWidth(col) for col in range(self.tableWidget_2.columnCount()))
        total_width += self.tableWidget_2.verticalHeader().width() + 10
        
        current_geometry = self.tableWidget_2.geometry()
        new_width = total_width
        self.tableWidget_2.setGeometry(current_geometry.x(), current_geometry.y(), 
                                      new_width, current_geometry.height())
        
        # Center horizontally
        window_width = self.centralWidget().width()
        new_x = (window_width - new_width) // 2
        self.tableWidget_2.setGeometry(new_x, current_geometry.y(), 
                                      new_width, current_geometry.height())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())