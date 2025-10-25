from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QSizePolicy, QDateEdit, QFrame, QComboBox
from PySide6.QtGui import QPainter, QBrush, QColor, QPolygon, QFont
from PySide6.QtCore import Qt, QPoint, QDate
from views.translations import translate
from models.parser import get_config_parser


class BubbleWidget(QWidget):
    
    def __init__(self, parent, label_text, button_text, anchor_btn, initial_text="", show_input=True, cancel_text=None, warning_text=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumWidth(240)
        self.setMinimumHeight(170)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.anchor_btn = anchor_btn
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(10)
        label = QLabel(translate(label_text))
        label.setStyleSheet("color: #f0f0f0; font-size: 14px;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        if warning_text:
            warning = QLabel(warning_text)
            warning.setStyleSheet("color: #e57373; font-size: 12px; font-style: italic;")
            warning.setAlignment(Qt.AlignCenter)
            layout.addWidget(warning)
        self.name_input = QLineEdit()
        self.name_input.setText(initial_text)
        self.name_input.setStyleSheet("background: #222; color: #f0f0f0; border-radius: 6px; padding: 4px 8px;")
        if show_input:
            layout.addWidget(self.name_input)
        self.action_btn = QPushButton(translate(button_text))
        self.action_btn.setStyleSheet("background: #c00; color: #fff; border-radius: 6px; padding: 4px 12px;")
        btn_row = QHBoxLayout()
        btn_row.addWidget(self.action_btn)
        if cancel_text:
            self.cancel_btn = QPushButton(translate(cancel_text))
            self.cancel_btn.setStyleSheet("background: #444; color: #f0f0f0; border-radius: 6px; padding: 4px 12px;")
            btn_row.addWidget(self.cancel_btn)
        layout.addLayout(btn_row)
        layout.addStretch(1)
        if show_input:
            self.name_input.returnPressed.connect(self.action_btn.click)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        bubble_color = QColor(40, 40, 48)
        border_color = QColor(80, 80, 96)
        painter.setBrush(QBrush(bubble_color))
        painter.setPen(border_color)
        rect = self.rect().adjusted(0, 0, 0, -14)
        painter.drawRoundedRect(rect, 18, 18)
        # Draw triangle for bubble tail, aligned with anchor_btn
        btn = self.anchor_btn
        btn_pos = btn.mapToGlobal(btn.rect().center())
        bubble_pos = self.mapToGlobal(self.rect().topLeft())
        local_x = btn_pos.x() - bubble_pos.x()
        arrow_x = max(rect.left()+24, min(local_x, rect.right()-24))
        points = [QPoint(arrow_x-12, rect.bottom()), QPoint(arrow_x+12, rect.bottom()), QPoint(arrow_x, rect.bottom()+14)]
        polygon = QPolygon(points)
        painter.setBrush(QBrush(bubble_color))
        painter.setPen(border_color)
        painter.drawPolygon(polygon)
        painter.end()
    
    def showEvent(self, event):
        super().showEvent(event)
        self.name_input.setFocus()

class TaskBubble(BubbleWidget):
    def __init__(self, parent, anchor_btn, title="Add Task", action_text="Add", initial_desc="", initial_due_date=None):
        super().__init__(parent, title, action_text, anchor_btn, show_input=False)

        # Task description input
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText(translate("Task description"))
        self.desc_input.setText(initial_desc)
        self.desc_input.setStyleSheet("background: #222; color: #f0f0f0; border-radius: 6px; padding: 4px 8px;")
        self.layout().insertWidget(1, self.desc_input)

        # Due date input
        self.due_input = QDateEdit()
        self.due_input.setCalendarPopup(True)
        self.due_input.setDate(initial_due_date or QDate.currentDate())
        self.due_input.setStyleSheet("background: #222; color: #f0f0f0; border-radius: 6px; padding: 4px 8px;")
        self.layout().insertWidget(2, self.due_input)

        # Set focus on description input
        self.desc_input.setFocus()
        self.desc_input.returnPressed.connect(self.action_btn.click)

class TaskWidget(QWidget):
    def __init__(self, description, status, due_date, close_date, creation_date):
        super().__init__()
        layout = QVBoxLayout()

        # Title/Description
        title_label = QLabel(description)
        title_label.setFont(QFont("Arial", 11, QFont.Bold))
        title_label.setStyleSheet("color: #ffffff;")
        layout.addWidget(title_label)

        # Dates and Status
        dates_status_layout = QHBoxLayout()
        dates_status_layout.setContentsMargins(0, 0, 0, 0)  # Reduce padding for this row
        creation_date_label = QLabel(f"{translate('Created')}: {creation_date}")
        creation_date_label.setAlignment(Qt.AlignCenter)
        creation_date_label.setStyleSheet("color: #cccccc; padding: 0px 2px;")
        due_date_label = QLabel(f"{translate('Due')}: {due_date}")
        due_date_label.setAlignment(Qt.AlignCenter)

        # Colorize due date based on on-time or overdue, using the same colors as the status field
        if status == "open":
            due_date_obj = QDate.fromString(due_date, "yyyy-MM-dd")
            if due_date_obj < QDate.currentDate():
                due_date_label.setStyleSheet("color: #ff4444; padding: 0px 2px;")  # Overdue (red)
            else:
                due_date_label.setStyleSheet("color: #ffaa00; padding: 0px 2px;")  # On time (yellow)
        else:
            due_date_label.setStyleSheet("color: #cccccc; padding: 0px 2px;")

        close_date_label = QLabel(f"{translate('Closed')}: {close_date or ''}")
        close_date_label.setAlignment(Qt.AlignCenter)

        # Colorize close date based on adherence to due date if status is complete
        if status == "complete" and close_date:
            close_date_obj = QDate.fromString(close_date, "yyyy-MM-dd")
            due_date_obj = QDate.fromString(due_date, "yyyy-MM-dd")
            if close_date_obj <= due_date_obj:
                close_date_label.setStyleSheet("color: #00ff00; padding: 0px 2px;")  # On time (green)
            else:
                close_date_label.setStyleSheet("color: #ff4444; padding: 0px 2px;")  # Late (red)
        else:
            close_date_label.setStyleSheet("color: #cccccc; padding: 0px 2px;")

        status_label = QLabel(f"{translate('Status')}: {translate(status)}")
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setStyleSheet("color: #00ff00; padding: 0px 2px;" if status == "complete" else "color: #ff4444; padding: 0px 2px;" if status == "cancelled" else "color: #ffaa00; padding: 0px 2px;")
        dates_status_layout.addWidget(creation_date_label)
        dates_status_layout.addWidget(due_date_label)
        dates_status_layout.addWidget(close_date_label)
        dates_status_layout.addWidget(status_label)
        layout.addLayout(dates_status_layout)

        # Separator
        separator = QFrame()
        separator.setStyleSheet("background-color: #cccccc;")
        layout.addWidget(separator)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #333333; border: 1px solid #555555; border-radius: 8px; padding: 10px;")

class TaskFilterWidget(QWidget):
    def __init__(self, on_filter_selected):
        super().__init__()
        # Read configured default filter from config.ini (language-neutral canonical value)
        try:
            cfg = get_config_parser()
            default_filter = cfg.get("General", "default_filter", fallback="Open")
        except Exception:
            default_filter = "Open"
        self.current_filter = default_filter
        layout = QHBoxLayout()
        layout.setSpacing(10)

        self.sort_combo = QComboBox()
        self.sort_combo.addItem(translate("Creation Date"), "creation")
        self.sort_combo.addItem(translate("Due Date"), "due")
        self.sort_combo.addItem(translate("Status"), "status")
        layout.addWidget(self.sort_combo)
        # Try to initialize sort combo from saved config (default_sort)
        try:
            cfg = get_config_parser()
            saved_sort = cfg.get("General", "default_sort", fallback="creation")
            idx = self.sort_combo.findData(saved_sort)
            if idx != -1:
                self.sort_combo.setCurrentIndex(idx)
        except Exception:
            pass

        # Connect changes to the provided callback (reapplies filters/sort on change)
        self.sort_combo.currentTextChanged.connect(on_filter_selected)

        # Filter buttons
        self.buttons: dict[str, QPushButton] = {}
        filters = ["All", "On Time", "Overdue", "Open", "Finished", "Cancelled"]
        for filter_name in filters:
            button = QPushButton(translate(filter_name))
            button.setCheckable(True)
            button.setStyleSheet(self.get_button_style(False))
            button.clicked.connect(lambda checked, name=filter_name: self.on_button_clicked(name, on_filter_selected))
            layout.addWidget(button)
            self.buttons[filter_name] = button

        # Apply provided default filter
        if default_filter in self.buttons:
            self.buttons[default_filter].setChecked(True)
            self.buttons[default_filter].setStyleSheet(self.get_button_style(True))
        else:
            # Fallback to Open
            self.buttons["Open"].setChecked(True)
            self.buttons["Open"].setStyleSheet(self.get_button_style(True))

        self.setLayout(layout)

    def on_button_clicked(self, filter_name, on_filter_selected):
        self.current_filter = filter_name
        # Uncheck all buttons except the selected one
        for name, button in self.buttons.items():
            is_selected = name == filter_name
            button.setChecked(is_selected)
            button.setStyleSheet(self.get_button_style(is_selected))

        # Call the callback with the selected filter
        on_filter_selected()

    def get_button_style(self, is_selected):
        if is_selected:
            return (
                "padding: 5px 10px; border-radius: 5px; "
                "background-color: palette(highlight); color: palette(highlightedText);"
            )
        else:
            return (
                "padding: 5px 10px; border-radius: 5px; "
                "background-color: #444; color: #fff;"
            )

    def get_current_filter(self):
        return self.current_filter
    
    def get_sort_method(self):
        if self.sort_combo:
            return self.sort_combo.currentData()
        return "creation"  # Default sort method
