#!/usr/bin/env python3

from .view import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QPixmap
from PyQt5.QtCore import QTimer, QTime, Qt
import datetime as dt
import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import os


class Controller(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        """
        Initialize the application, set up UI components, and display weather data.
        """
        super().__init__()
        self.setupUi(self)

        self.city = {'default': 'Judsonia', 'geo': None}
        self.word_list = []
        self.allow_suggestions = False  # Control suggestions
        self.isTranslucent = True
        self._tz_offset = 0  # seconds offset from API

        # Load API key from file (no hardcoding here)
        self.API_KEY = self.get_api_key()
        if not self.API_KEY:
            # Fail gracefully if missing
            #self.API_KEY = ""
            self.API_KEY = "426dc8e49c84d6c1ac6b39c3dcdd78f6"
            
        # Timer: update clock label every minute
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_current_time)
        self.timer.start(60_000)  # 60 seconds

        # Debounce for city suggestions
        self.suggestion_timer = QTimer(self)
        self.suggestion_timer.setSingleShot(True)
        self.suggestion_timer.timeout.connect(self.suggest_city_name)

        # Data model for list view
        self.model = QStandardItemModel()
        self.listView.setModel(self.model)

        # Wire up actions & show
        self.setup_actions()
        self.get_weather()  # populates and calls display_weather()
        self.show()

        # Periodic weather refresh (every 10 minutes)
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.get_weather)
        self.refresh_timer.start(10 * 60 * 1000)

    def setup_actions(self) -> None:
        """
        Set up actions and event handlers for UI components.
        """
        self.lineEdit.textChanged.connect(self.on_text_changed)
        self.listView.doubleClicked.connect(self.display_selected_city_weather)
        self.actionChange_Location.triggered.connect(self.toggle_city_editing)

        self.actionHeavyTranslucency.triggered.connect(lambda: self.set_translucency(True))
        self.actionLightTranslucency.triggered.connect(lambda: self.set_translucency(False))
        self.actionDark.triggered.connect(self.dark_mode)
        self.actionLight.triggered.connect(self.light_mode)

    def set_translucency(self, enable: bool) -> None:
        """
        Toggle translucency (Light or Heavy)
        """
        if enable:
            self.setAttribute(Qt.WA_TranslucentBackground, True)
            self.listView.setAttribute(Qt.WA_TranslucentBackground, True)
            self.lineEdit.setAttribute(Qt.WA_TranslucentBackground, True)
            self.menubar.setAttribute(Qt.WA_TranslucentBackground, True)
            self.label_icon.setAttribute(Qt.WA_TranslucentBackground, True)
        else:
            self.setAttribute(Qt.WA_TranslucentBackground, False)
            self.listView.setAttribute(Qt.WA_TranslucentBackground, False)
            self.lineEdit.setAttribute(Qt.WA_TranslucentBackground, False)
            self.menubar.setAttribute(Qt.WA_TranslucentBackground, False)
            self.label_icon.setAttribute(Qt.WA_TranslucentBackground, False)
            self.setAttribute(Qt.WA_NoSystemBackground, False)

    def dark_mode(self) -> None:
        """
        Set Theme to Dark Mode
        """
        self.setStyleSheet("background-color: rgba(36, 31, 49, 120);\ncolor: rgb(246, 245, 244);")
        self.listView.setStyleSheet("background-color: rgba(36, 31, 49, 120);\ncolor: rgb(246, 245, 244);")
        self.lineEdit.setStyleSheet("background-color: rgba(36, 31, 49, 120);\ncolor: rgb(246, 245, 244);")
        self.menubar.setStyleSheet("background-color: rgba(36, 31, 49, 120);\ncolor: rgb(246, 245, 244);")
        self.label_icon.setStyleSheet("background-color: rgba(36, 31, 49, 120);\ncolor: rgb(246, 245, 244);")

    def light_mode(self) -> None:
        """
        Set Theme to Light Mode
        """
        self.setStyleSheet("background-color: rgba(245, 245, 245, 0.8);\ncolor: rgba(50, 50, 50, 1);")
        self.listView.setStyleSheet("background-color: rgba(245, 245, 245, 0.8);\ncolor: rgba(50, 50, 50, 1);")
        self.lineEdit.setStyleSheet("background-color: rgba(245, 245, 245, 0.8);\ncolor: rgba(50, 50, 50, 1);")
        self.menubar.setStyleSheet("background-color: rgba(245, 245, 245, 0.8);\ncolor: rgba(50, 50, 50, 1);")
        self.label_icon.setStyleSheet("background-color: rgba(245, 245, 245, 0.8);\ncolor: rgba(50, 50, 50, 1);")

    def on_text_changed(self) -> None:
        """
        Start a debounce timer for API calls when the text changes in the input box.
        """
        self.suggestion_timer.start(300)  # 300ms debounce

    def get_city_state(self, city_name: str) -> list:
        """
        Retrieve matching city names based on user input.
        """
        geolocator = Nominatim(user_agent="Weather app (mail@gmail.com)")
        try:
            location = geolocator.geocode(city_name, exactly_one=False, language='en')
            if location:
                return [loc.address for loc in location]
            return ["No matches found."]
        except GeocoderTimedOut:
            return ["Geocoding service timed out. Please try again later."]

    def display_selected_city_weather(self) -> None:
        """
        Update the weather display based on the selected city from the list.
        """
        selected_items = self.listView.selectedIndexes()
        if selected_items:
            selected_city = selected_items[0].data()
            self.city_name = selected_city
            self.lineEdit.blockSignals(True)
            self.lineEdit.setText(selected_city)
            self.lineEdit.blockSignals(False)
            self.get_weather()

    def toggle_city_editing(self) -> None:
        """
        Enable or disable city name editing for weather search.
        """
        self.lineEdit.clear()
        self.model.clear()

        self.listView.setSelectionMode(QListView.SingleSelection)

        enabled = not self.lineEdit.isEnabled()
        self.lineEdit.setEnabled(enabled)
        self.lineEdit.setFocus()

        self.allow_suggestions = enabled
        if not enabled:  # If disabled, reset city name to 'geo' or default
            self.lineEdit.setText(self.city['geo'] if self.city['geo'] else self.city['default'])

    def suggest_city_name(self) -> None:
        """
        Provide city name suggestions in the list view.
        """
        if not self.allow_suggestions:
            return

        city_name = self.lineEdit.text().strip()
        if not city_name:
            self.model.clear()
            return

        self.word_list = self.get_city_state(city_name)
        self.model.clear()
        for word in self.word_list:
            self.model.appendRow(QStandardItem(word))

    def get_api_key(self) -> str:
        """
        Retrieve API_KEY from api_key.txt next to this file.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        api_key_path = os.path.join(current_dir, 'api_key.txt')
        try:
            with open(api_key_path, 'r') as file:
                return file.read().strip()
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "API key file not found!")
            return ""

    def get_weather(self) -> None:
        """
        Fetch and process weather data for the selected city.
        """
        if not self.API_KEY:
            return

        BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
        self.city_name = self.lineEdit.text() or self.city['default']
        url = f"{BASE_URL}appid={self.API_KEY}&q={self.city_name}"

        try:
            resp = requests.get(url, timeout=8)
        except requests.RequestException:
            QMessageBox.warning(self, "Weather", "Network error while fetching weather data.")
            return

        if resp.status_code != 200:
            QMessageBox.warning(self, "Weather", f"Could not fetch weather data ({resp.status_code}).")
            return

        response = resp.json()

        self.city['geo'] = response.get('name', self.city_name)
        self.coordinates = f"Longitude: {response['coord']['lon']}, Latitude: {response['coord']['lat']}"
        self.condition = response['weather'][0]['description']
        self.weather = {
            'temp': (response['main']['temp'] - 273.15) * 1.8 + 32,
            'feel like': (response['main']['feels_like'] - 273.15) * 1.8 + 32,
            'Low': (response['main']['temp_min'] - 273.15) * 1.8 + 32,
            'High': (response['main']['temp_max'] - 273.15) * 1.8 + 32,
            'humidity': response['main']['humidity'],
            'icon': response['weather'][0]['icon'],
        }

        # Store timezone offset for clock updates
        self._tz_offset = int(response.get('timezone', 0))

        # Icon path (as in your original)
        self.icon_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'icons',
            f'{self.weather["icon"]}.png'
        )
        self.icon_pixmap = QPixmap(self.icon_path)

        self.wind = response['wind']['speed']

        local_timezone = dt.timezone(dt.timedelta(seconds=self._tz_offset))
        current_utc_time = dt.datetime.now(dt.timezone.utc)
        self.current_local_time = current_utc_time.astimezone(local_timezone)

        self.sunrise = dt.datetime.fromtimestamp(response['sys']['sunrise'], tz=local_timezone)
        self.sunset = dt.datetime.fromtimestamp(response['sys']['sunset'], tz=local_timezone)

        self.display_weather()

    def format_time(self, time: dt.datetime) -> str:
        """
        Format a datetime object to 'HH:MM'.
        """
        return time.strftime('%H:%M')

    def update_current_time(self) -> None:
        """
        Update the displayed current local time every minute (no drift).
        """
        tz = dt.timezone(dt.timedelta(seconds=self._tz_offset))
        now_local = dt.datetime.now(dt.timezone.utc).astimezone(tz)
        self.time_label.setText(self.format_time(now_local))

    def display_weather(self) -> None:
        """
        Display the retrieved weather data in the list view.
        """
        self.lineEdit.setText(self.city_name)

        self.model.clear()

        weather_details = [
            f"City: {self.city['geo']}",
            f"Condition: {self.condition.upper()}",
            f"Temperature: {int(self.weather['temp'])} F",
            f"Feels like: {int(self.weather['feel like'])} F",
            f"Low: {int(self.weather['Low'])} F, High: {int(self.weather['High'])} F",
            f"Humidity: {self.weather['humidity']}%",
            f"Wind: {self.wind} MPH",
            f"Sunrise: {self.format_time(self.sunrise)}",
            f"Sunset: {self.format_time(self.sunset)}",
            f"Coordinates: {self.coordinates}",
        ]

        for detail in weather_details:
            self.model.appendRow(QStandardItem(detail))

        self.label_icon.setPixmap(self.icon_pixmap)
        self.label_icon.setScaledContents(True)

        self.listView.setSelectionMode(QListView.NoSelection)
        self.lineEdit.setEnabled(False)

        # Update the clock immediately after display
        self.update_current_time()
