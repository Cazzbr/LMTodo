import configparser

class TodoConfigParser:
    """Handles loading and saving configurations."""

    DEFAULTS = {
        "Window": {
            "width": "1280",
            "height": "720",
            "x": "100",
            "y": "100"
        },
        "General": {
            "db_path": "todo.db",
            "default_project": "All Projects",
            "default_filter": "Open"
        },
        "Shortcuts": {
            "add_project": "Ctrl+A",
            "edit_project": "Ctrl+E",
            "delete_project": "Ctrl+D",
            "add_task": "Ctrl+T",
            "edit_task": "Ctrl+Shift+E",
            "remove_task": "Ctrl+Shift+D",
            "mark_completed": "Ctrl+M",
            "mark_canceled": "Ctrl+Shift+M",
            "all_projects": "Ctrl+P",
            "config_panel": "Ctrl+Shift+P",
            "filter_all": "Ctrl+F",
            "on_time": "Ctrl+O",
            "overdue": "Ctrl+Shift+O",
            "filter_active": "Ctrl+Shift+F",
            "filter_completed": "Ctrl+Alt+F",
            "filter_canceled": "Ctrl+Alt+Shift+F",
            "select_project": "Ctrl+L",
            "select_tasks": "Ctrl+Shift+L"
        }
    }

    def __init__(self, config_file="config.ini"):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load_config()
        self.window_settings = self.get_window_settings()
        self.db_path = self.get_db_path()

    def load_config(self):
        """Load the configuration file."""
        self.config.read(self.config_file)

    def get(self, section, option, fallback=None):
        """Get a configuration value with a fallback."""
        return self.config.get(section, option, fallback=fallback)

    def set(self, section, option, value):
        """Set a configuration value."""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][option] = value

    def save(self):
        """Save the configuration to the file."""
        with open(self.config_file, "w") as configfile:
            self.config.write(configfile)

    def get_window_settings(self):
        """Retrieve window size and position, returning defaults if not set."""
        width = int(self.get("Window", "width", fallback=self.DEFAULTS["Window"]["width"]))
        height = int(self.get("Window", "height", fallback=self.DEFAULTS["Window"]["height"]))
        x = int(self.get("Window", "x", fallback=self.DEFAULTS["Window"]["x"]))
        y = int(self.get("Window", "y", fallback=self.DEFAULTS["Window"]["y"]))
        return {"width": width, "height": height, "x": x, "y": y}

    def get_db_path(self):
        """Retrieve the database path, returning default if not set."""
        return self.get("General", "db_path", fallback=self.DEFAULTS["General"]["db_path"])

    def save_window_settings(self, width, height, x, y):
        """Persist the window size and position to the configuration file."""
        self.set("Window", "width", str(width))
        self.set("Window", "height", str(height))
        self.set("Window", "x", str(x))
        self.set("Window", "y", str(y))
        self.save()

    def save_db_path(self, path):
        """Persist the database path to the configuration file."""
        self.set("General", "db_path", path)
        self.save()

    def get_shortcuts(self):
        """Retrieve all shortcuts, returning defaults if not set."""
        shortcuts = {}
        for action, default_shortcut in self.DEFAULTS["Shortcuts"].items():
            shortcuts[action] = self.get("Shortcuts", action, fallback=default_shortcut)
        return shortcuts
