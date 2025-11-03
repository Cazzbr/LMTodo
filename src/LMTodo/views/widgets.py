from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QSizePolicy, QDateEdit, QFrame, QComboBox, QTextEdit
from PySide6.QtGui import QPainter, QBrush, QColor, QPolygon, QFont
from PySide6.QtCore import Qt, QPoint, QDate, QRect
from views.translations import translate
from models.parser import get_config_parser


class BubbleWidget(QWidget):
    
    def __init__(self, parent, label_text, button_text, anchor_btn, initial_text="", show_input=True, cancel_text=None, warning_text=None, minWidth=240, minHeight=170):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumWidth(minWidth)
        self.setMinimumHeight(minHeight)
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
        # Expose the button row so subclasses (like TaskBubble) can add widgets to the same row
        self.btn_row = QHBoxLayout()
        self.btn_row.addWidget(self.action_btn)
        if cancel_text:
            self.cancel_btn = QPushButton(translate(cancel_text))
            self.cancel_btn.setStyleSheet("background: #444; color: #f0f0f0; border-radius: 6px; padding: 4px 12px;")
            self.btn_row.addWidget(self.cancel_btn)
        layout.addLayout(self.btn_row)
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
    def __init__(self, parent, anchor_btn, title="Add Task", action_text="Add", initial_desc="", initial_due_date=None, projects=None, selected_project_id=None):
        super().__init__(parent, title, action_text, anchor_btn, show_input=False, minWidth=550)
        # Task description input
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText(translate("Task description"))
        self.desc_input.setText(initial_desc)
        self.desc_input.setStyleSheet("background: #222; color: #f0f0f0; border-radius: 6px; padding: 4px 8px;")
        self.desc_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.layout().insertWidget(1, self.desc_input)
        # Due date input
        self.due_input = QDateEdit()
        self.due_input.setCalendarPopup(True)
        self.due_input.setDate(initial_due_date or QDate.currentDate())
        self.due_input.setStyleSheet("background: #222; color: #f0f0f0; border-radius: 6px; padding: 4px 8px;")
        self.due_input.setMaximumWidth(140)
        self.btn_row.insertWidget(0, self.due_input)
        # Projects
        self.project_combo = QComboBox()
        self.project_combo.setMinimumWidth(150)
        if projects:
            for pid, name in projects:
                self.project_combo.addItem(name, pid)
            # select the provided project id, or fallback to first
            if selected_project_id is not None:
                idx = self.project_combo.findData(selected_project_id)
                if idx != -1:
                    self.project_combo.setCurrentIndex(idx)
        self.btn_row.insertWidget(1, self.project_combo)
        # add a stretch so buttons stay to the right
        self.btn_row.insertStretch(2, 1)

        # Set focus on description input
        self.desc_input.setFocus()
        self.desc_input.returnPressed.connect(self.action_btn.click)


class CommentBubble(BubbleWidget):
    def __init__(self, parent, anchor_btn, title="Comments", initial_text="", on_close=None):
        # Use a wider and slightly shorter bubble for comments as requested
        # Double width of previous 420 -> 840; reduce height by one third: 260 * 2/3 ~= 173
        super().__init__(parent, title, "", anchor_btn, show_input=False, minWidth=840, minHeight=173)

        # Add a multiline text edit for comments
        self.comment_edit = QTextEdit()
        self.comment_edit.setPlainText(initial_text or "")
        self.comment_edit.setStyleSheet("background: #222; color: #f0f0f0; border-radius: 6px; padding: 6px;")
        # Insert before the button row
        self.layout().insertWidget(1, self.comment_edit)
        self._on_close = on_close

    def closeEvent(self, event):
        # When the bubble is closed (including clicking outside), persist via callback
        try:
            if callable(self._on_close):
                self._on_close(self.comment_edit.toPlainText())
        except Exception:
            pass
        super().closeEvent(event)


class TaskWidget(QWidget):
    def __init__(self, task_id, description, status, due_date, close_date, creation_date, comments=None, on_save_comments=None):
        super().__init__()
        layout = QVBoxLayout()

        # Title/Description row with comment button at the end
        title_row = QHBoxLayout()
        title_label = QLabel(description)
        title_label.setFont(QFont("Arial", 11, QFont.Bold))
        title_label.setStyleSheet("color: #ffffff;")
        title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        title_row.addWidget(title_label)

        # Comments button (opens CommentBubble)
        comment_btn = QPushButton("💬")
        comment_btn.setToolTip(translate("Comments"))
        comment_btn.setMaximumWidth(36)
        title_row.addWidget(comment_btn)
        layout.addLayout(title_row)

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
        

        # Wire comment button to open bubble
        def _open_comments():
            def _save_and_refresh(text):
                try:
                    if callable(on_save_comments):
                        on_save_comments(task_id, text)
                except Exception:
                    pass

            # Build content as a QLayout (required by BubbleWidgetV2)
            content_layout = QVBoxLayout()
            comment_edit = QTextEdit()
            comment_edit.setPlainText(comments or "")
            comment_edit.setStyleSheet("background: #222; color: #f0f0f0; border-radius: 6px; padding: 6px;")
            content_layout.addWidget(comment_edit)

            # Create the new bubble variant using the layout content. Use top-right anchor
            # to match prior placement (bubble's top-right aligns with button top-right).
            cb = BubbleWidgetV2(self, content_layout, comment_btn, anchor_point='top-right', minWidth=840, minHeight=173, on_close=_save_and_refresh)
            # Ensure bubble has the requested size before computing position
            try:
                cb.resize(cb.minimumWidth(), cb.minimumHeight())
            except Exception:
                pass
            cb.show()
        comment_btn.clicked.connect(_open_comments)      


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


class BubbleWidgetV2(QWidget):
    """
    BubbleWidgetV2: a flexible bubble that accepts arbitrary content and an anchor point.

    Args:
        parent: parent widget
        content: QLayout containing the bubble contents
        anchor_btn: widget used as anchor/reference for positioning
        anchor_point: one of 'top-right','top-center','top-left','bottom-left','bottom-center','bottom-right'
        minWidth/minHeight: minimum geometry for bubble
    """
    def __init__(self, parent, content, anchor_btn, anchor_point='bottom-right', minWidth=240, minHeight=170, on_close=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumWidth(minWidth)
        self.setMinimumHeight(minHeight)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.anchor_btn = anchor_btn
        self._anchor_point: str = anchor_point.lower()

        self._tail_size = 10
        self._tail_offset = 16

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(10)

        container = QWidget()
        container.setLayout(content)
        main_layout.addWidget(container)

        main_layout.addStretch(1)
        # store on_close callback
        self._on_close = on_close

    def closeEvent(self, event):
        # If an on_close callback was provided, try to extract a QTextEdit from
        # the bubble contents and pass its text to the callback.
        try:
            if callable(self._on_close):
                # find the first QTextEdit child
                te = self.findChild(QTextEdit)
                if te is not None:
                    self._on_close(te.toPlainText())
        except Exception:
            pass
        super().closeEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        bubble_color = QColor(40, 40, 48)
        border_color = QColor(80, 80, 96)
        painter.setBrush(QBrush(bubble_color))
        painter.setPen(border_color)
        tail_on_top = self._anchor_point.startswith('top')
        # Reserve equal vertical space for the tail at both top and bottom so margins are symmetric.
        # Keep left/right as-is; only push the top and bottom in by tail_size.
        match self._anchor_point.split('-')[0]:
            case 'top':
                rect = self.rect().adjusted(0, self._tail_size, 0, 0)
            case 'bottom':
                rect = self.rect().adjusted(0, 0, 0, -self._tail_size)
            case 'left':
                rect = self.rect().adjusted(self._tail_size, 0, 0, 0)
            case 'right':
                rect = self.rect().adjusted(0, 0, -self._tail_size, 0)
            case _:
                rect = self.rect()
        
        painter.drawRoundedRect(rect, 12, 12)

        target_pt = self._global_anchor_point(self._anchor_point.split('-')[0])

        # Use the adjusted rect's top-left when converting to global coordinates so
        # the arrow local_x is computed with the same coordinate space as `rect`.
        bubble_pos = self.mapToGlobal(rect.topLeft())
        local_x = target_pt.x() - bubble_pos.x()
        arrow_x = max(rect.left() + self._tail_offset, min(local_x, rect.right() - self._tail_offset))

        if tail_on_top:
            # Triangle pointing upwards, base attached to the top edge of rect
            points = [QPoint(arrow_x - self._tail_offset / 2, rect.top()), QPoint(arrow_x + self._tail_offset / 2, rect.top()), QPoint(arrow_x, rect.top() - self._tail_size)]
        else:
            # Triangle pointing downwards, base attached to the bottom edge of rect
            points = [QPoint(arrow_x - self._tail_offset / 2, rect.bottom()), QPoint(arrow_x + self._tail_offset / 2, rect.bottom()), QPoint(arrow_x, rect.bottom() + self._tail_size)]

        polygon = QPolygon(points)
        painter.setBrush(QBrush(bubble_color))
        painter.setPen(border_color)
        painter.drawPolygon(polygon)
        painter.end()

    def show(self):
        anchor_pos = self._global_anchor_point(self._anchor_point.split('-')[0])
        
        if self._anchor_point.startswith('top'):
            y = anchor_pos.y()
        else:
            y = anchor_pos.y() - self.height()
        
        if self._anchor_point.endswith('right'):
            x = anchor_pos.x() - self.width() + self._tail_offset
        elif self._anchor_point.endswith('center'):
            x = anchor_pos.x() - (self.width() // 2)
        else:
            x = anchor_pos.x() - self._tail_offset

        self.move(int(x), int(y))
        
        print(self.will_fit())

        super().show()
    
    def _global_anchor_point(self, side: str) -> QPoint:
        match side:
            case 'top':
                return self.anchor_btn.mapToGlobal(QPoint(self.anchor_btn.rect().center().x(), self.anchor_btn.rect().bottom()))
            case    'bottom':
                return self.anchor_btn.mapToGlobal(QPoint(self.anchor_btn.rect().center().x(), self.anchor_btn.rect().top()))
            case    'right':
                return self.anchor_btn.mapToGlobal(QPoint(self.anchor_btn.rect().left(), self.anchor_btn.rect().center().y()))
            case    'left':
                return self.anchor_btn.mapToGlobal(QPoint(self.anchor_btn.rect().right(), self.anchor_btn.rect().center().y()))
            case _:
                raise ValueError("Invalid side for anchor_point")

    def will_fit(self) -> bool:
        """Return True if the bubble placed using the current `self._anchor_point`
        at `anchor_global_point` would be fully inside the application window.

        This is a simple check: it computes the bubble rectangle using the bubble's
        current size (or minimum size) and the anchor point orientation stored in
        `self._anchor_point`, then checks whether that rect is contained inside the
        top-level window geometry (or primary screen available geometry).
        """
        frame_rect = self.frameGeometry()
        print(f"Frame rect: {frame_rect}")

        # Get the top-level window's frame geometry (also global)
        top_window_rect = self.window().frameGeometry()
        print(f"Top window rect: {top_window_rect}")

        # Check if the top-level window's rectangle contains the widget's rectangle
        return top_window_rect.contains(frame_rect)