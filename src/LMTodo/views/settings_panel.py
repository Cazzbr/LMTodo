from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy, QLineEdit, QScrollArea, QWidget
from PySide6.QtCore import Qt
import shutil
import os

from controllers.todo_controller import update_db_path, init_db

class SettingsPanel(QFrame):

    def __init__(self, config_parser, parent=None):
        self._parent = parent
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)

        self.config_parser = config_parser

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Scrollable Content
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(20, 20, 20, 20)
        scroll_layout.setSpacing(30)

        # Title
        title_label = QLabel("Settings")
        title_label.setAlignment(Qt.AlignCenter)  # Center the title
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        scroll_layout.addWidget(title_label)

        scroll_layout.addLayout(self.get_db_location_layout())
        scroll_layout.addLayout(self.get_shortcut_config_layout())

        # Spacer
        scroll_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def get_db_location_layout(self):
        layout = QVBoxLayout()
        layout.setSpacing(1)

        # Current DB Path Section
        db_path_layout = QHBoxLayout()
        db_path_label = QLabel("Current Database Path:")
        db_path_label.setStyleSheet(self._get_subtitle_style())

        db_path_layout.addWidget(db_path_label)
        db_path_layout.addSpacing(50)
        # Change DB Location Button
        self.change_db_btn = QPushButton("Change")
        self.change_db_btn.clicked.connect(self.change_db_location)
        db_path_layout.addWidget(self.change_db_btn)
        db_path_layout.addStretch()
        layout.addLayout(db_path_layout)

        # Current DB Path Display
        self.db_path_value_label = QLabel(self.config_parser.get_db_path())
        self.db_path_value_label.setStyleSheet("font-size: 14px; color: #555;")
        self.db_path_value_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.db_path_value_label.setToolTip(self.config_parser.get_db_path())  # Add tooltip for full path

        layout.addWidget(self.db_path_value_label)
        return layout

    def get_shortcut_config_layout(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Shortcut Configuration Section
        shortcut_label = QLabel("Shortcut Configuration:")
        shortcut_label.setStyleSheet(self._get_subtitle_style())
        layout.addWidget(shortcut_label)

        shortcuts = self.config_parser.DEFAULTS["Shortcuts"]

        # Shortcut for Add Project Button
        layout.addLayout(self._create_shortcut_row("Add Project Shortcut:", "add_project", shortcuts["add_project"]))
        # Shortcut for Edit Project Button
        layout.addLayout(self._create_shortcut_row("Edit Project Shortcut:", "edit_project", shortcuts["edit_project"]))
        # Shortcut for Delete Project Button
        layout.addLayout(self._create_shortcut_row("Delete Project Shortcut:", "delete_project", shortcuts["delete_project"]))
        # Shortcut for Add Task Button
        layout.addLayout(self._create_shortcut_row("Add Task Shortcut:", "add_task", shortcuts["add_task"]))
        # Shortcut for Edit Task Button
        layout.addLayout(self._create_shortcut_row("Edit Task Shortcut:", "edit_task", shortcuts["edit_task"]))
        # Shortcut for Remove Task Button
        layout.addLayout(self._create_shortcut_row("Remove Task Shortcut:", "remove_task", shortcuts["remove_task"]))
        # Shortcut for Mark Completed Button
        layout.addLayout(self._create_shortcut_row("Mark Completed Shortcut:", "mark_completed", shortcuts["mark_completed"]))
        # Shortcut for Mark Canceled Button
        layout.addLayout(self._create_shortcut_row("Mark Canceled Shortcut:", "mark_canceled", shortcuts["mark_canceled"]))
        # Shortcut for All Projects Button
        layout.addLayout(self._create_shortcut_row("All Projects Shortcut:", "all_projects", shortcuts["all_projects"]))
        # Shortcut for Config Panel Button
        layout.addLayout(self._create_shortcut_row("Config Panel Shortcut:", "config_panel", shortcuts["config_panel"]))
        # Shortcut for Filter Buttons
        layout.addLayout(self._create_shortcut_row("Filter All Shortcut:", "filter_all", shortcuts["filter_all"]))
        layout.addLayout(self._create_shortcut_row("On-Time Shortcut:", "on_time", shortcuts["on_time"]))
        layout.addLayout(self._create_shortcut_row("Overdue Shortcut:", "overdue", shortcuts["overdue"]))
        layout.addLayout(self._create_shortcut_row("Filter Active Shortcut:", "filter_active", shortcuts["filter_active"]))
        layout.addLayout(self._create_shortcut_row("Filter Completed Shortcut:", "filter_completed", shortcuts["filter_completed"]))
        layout.addLayout(self._create_shortcut_row("Filter Canceled Shortcut:", "filter_canceled", shortcuts["filter_canceled"]))
        # Selection shortcuts
        layout.addLayout(self._create_shortcut_row("Select Project Shortcut:", "select_project", shortcuts["select_project"]))
        layout.addLayout(self._create_shortcut_row("Select Tasks Shortcut:", "select_tasks", shortcuts["select_tasks"]))

        return layout

    def _create_shortcut_row(self, label_text, action, default_shortcut):
        row_layout = QHBoxLayout()
        row_layout.setSpacing(10)

        shortcut_label = QLabel(label_text)
        shortcut_label.setStyleSheet("font-size: 14px;")
        shortcut_label.setFixedWidth(200)

        shortcut_input = QLineEdit(self.config_parser.get("Shortcuts", action, fallback=default_shortcut))
        shortcut_input.setStyleSheet(
            "font-size: 14px; border: 1px solid #ccc; border-radius: 4px;"
        )
        shortcut_input.textChanged.connect(lambda: self.update_shortcut(action, shortcut_input.text()))

        row_layout.addWidget(shortcut_label)
        row_layout.addWidget(shortcut_input)
        row_layout.addStretch()

        return row_layout

    def update_shortcut(self, action, new_shortcut):
        """Update a shortcut and notify the main window to apply the change."""
        if self._parent:
            self._parent.update_shortcut(action, new_shortcut)

    def _get_subtitle_style(self):
        return "font-size: 14px; font-weight: bold;"

    def change_db_location(self):
        """Open a file dialog to select a new database location."""
        new_path, _ = QFileDialog.getSaveFileName(self, "Select New Database Location", "", "Database Files (*.db);;All Files (*)")

        if new_path:
            current_db_path = self.config_parser.get_db_path()

            if os.path.exists(current_db_path):
                # Ask the user if they want to move the current database
                reply = QMessageBox.question(
                    self,
                    "Move Database",
                    "Do you want to move the current database to the new location?\n\n"
                    "Warning: If you press 'No', a new database will be created at the new location, and all current information will be unavailable.",
                    QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
                )

                if reply == QMessageBox.Cancel:
                    return

                if reply == QMessageBox.Yes:
                    try:
                        shutil.move(current_db_path, new_path)
                        update_db_path(new_path)
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"Failed to move database: {e}")
                        return
                if reply == QMessageBox.No:
                    init_db(new_path)

            # Update the configuration with the new path
            self.config_parser.save_db_path(new_path)
            self.db_path_value_label.setText(new_path)  # Update the label
            self.db_path_value_label.setToolTip(new_path)  # Update the tooltip
            self._parent.load_projects()
            QMessageBox.information(self, "Success", "Database location updated successfully.")
