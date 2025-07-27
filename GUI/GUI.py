from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableWidgetItem, 
                           QLineEdit, QHeaderView, QComboBox, QWidget, QHBoxLayout, QLabel)

import sys


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

        # DON'T override the UI file settings - it already has 3 columns!
        # The UI file defines: User Name, Day One Times, Day Two Times

        # Connect the Add User button
        self.pushButton.clicked.connect(self.add_user)

        # Allow editing only for specific cells (User Name column) in main table
        self.tableWidget.setEditTriggers(
            self.tableWidget.DoubleClicked | 
            self.tableWidget.EditKeyPressed | 
            self.tableWidget.AnyKeyPressed
        )

        # Lock the availability/results table completely
        self.tableWidget_2.setEditTriggers(self.tableWidget_2.NoEditTriggers)

        # Set column widths to accommodate the dual dropdowns
        self.tableWidget.setColumnWidth(0, 120)  # User Name column
        self.tableWidget.setColumnWidth(1, 200)  # Day One Times column
        self.tableWidget.setColumnWidth(2, 200)  # Day Two Times column
        
        # Alternative: Make columns stretch to fill available space
        # self.tableWidget.horizontalHeader().setStretchLastSection(True)
        
        # Alternative: Auto-resize columns to content
        # self.tableWidget.resizeColumnsToContents()

    def add_user(self):
        row = self.user_count
        self.tableWidget.insertRow(row)

        # Put the user name IN the User Name column (column 0), make it editable
        user_name_item = QTableWidgetItem(f"User {row + 1}")
        user_name_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
        self.tableWidget.setItem(row, 0, user_name_item)
        
        # Column 1: Day One Times - Add dropdown for time selection
        self.add_time_dropdown(row, 1)

        # Column 2: Day Two Times - Add dropdown for time selection  
        self.add_time_dropdown(row, 2)

        self.user_count += 1

    def add_time_dropdown(self, row, column):
        """Add dual dropdowns (start time - end time) to a specific cell"""
        # Create a container widget
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(2, 2, 2, 2)  # Tight margins
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
        
        # Add widgets to layout
        layout.addWidget(start_combo)
        layout.addWidget(dash_label)
        layout.addWidget(end_combo)
        
        # Store references to the combo boxes for later retrieval
        container.start_combo = start_combo
        container.end_combo = end_combo
        
        # Add the container to the table
        self.tableWidget.setCellWidget(row, column, container)

    def get_all_selections(self):
        """Get all user selections from the table"""
        selections = []
        for row in range(self.tableWidget.rowCount()):
            user_name = self.tableWidget.item(row, 0).text() if self.tableWidget.item(row, 0) else f"User {row + 1}"
            
            # Get dual dropdown selections
            day_one_widget = self.tableWidget.cellWidget(row, 1)
            day_two_widget = self.tableWidget.cellWidget(row, 2)
            
            # Extract start and end times for day one
            if day_one_widget and hasattr(day_one_widget, 'start_combo'):
                day_one_start = day_one_widget.start_combo.currentText()
                day_one_end = day_one_widget.end_combo.currentText()
                day_one_time = f"{day_one_start} - {day_one_end}" if day_one_start != "Start" and day_one_end != "End" else "Not selected"
            else:
                day_one_time = "Not selected"
            
            # Extract start and end times for day two
            if day_two_widget and hasattr(day_two_widget, 'start_combo'):
                day_two_start = day_two_widget.start_combo.currentText()
                day_two_end = day_two_widget.end_combo.currentText()
                day_two_time = f"{day_two_start} - {day_two_end}" if day_two_start != "Start" and day_two_end != "End" else "Not selected"
            else:
                day_two_time = "Not selected"
            
            selections.append({
                'user': user_name,
                'day_one': day_one_time,
                'day_two': day_two_time
            })
        
        return selections


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())