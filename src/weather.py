#!/usr/bin/env python3

from view import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QPixmap
from PyQt5.QtCore import QTimer, QTime
import datetime as dt
import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


class Controller(QMainWindow, Ui_MainWindow):    
    def __init__(self) -> None:
        '''
        Initialize the application, set up UI components, and display weather data.
        :param: None
        :return: None
        '''
        super().__init__()
        self.setupUi(self)

        self.city = {'default': 'Judsonia', 'geo': None}
        self.word_list = []
        self.allow_suggestions = False  # Control suggestions
        self.isTranslucent = True
        self.API_KEY = self.get_api_key()
        # If you decide to hard code your API_KEY
        # self.API_KEY = ""

        # Timer for current time update
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_current_time)
        self.timer.start(60000)  # Update every minute

        self.suggestion_timer = QTimer(self)  # Debouncing API calls
        self.suggestion_timer.setSingleShot(True)
        self.suggestion_timer.timeout.connect(self.suggest_city_name)

        # Data model for list view
        self.model = QStandardItemModel()
        self.listView.setModel(self.model)

        # Initial setup
        self.setup_actions()
        self.get_weather()
        self.display_weather()
        self.show() 


    def setup_actions(self)-> None:
        '''
        Set up actions and event handlers for UI components.
        :param: None
        :return: None
        '''
        self.lineEdit.textChanged.connect(self.on_text_changed)
        self.listView.doubleClicked.connect(self.display_selected_city_weather)
        self.actionChange_Location.triggered.connect(self.toggle_city_editing)

        self.actionHeavyTranslucency.triggered.connect(lambda: self.set_translucency(True))
        self.actionLightTranslucency.triggered.connect(lambda: self.set_translucency(False))
        self.actionDark.triggered.connect(self.dark_mode)
        self.actionLight.triggered.connect(self.light_mode)
        
    def set_translucency(self, enable: bool) -> None:
        '''
        Toggle translucency (Light or Heavy)
        :param enable: Boolean
        :return: None
        
        '''
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
        '''
        Set Theme to Dark Mode
        :param: None
        :return: None
        '''
        self.setStyleSheet("background-color: rgba(36, 31, 49, 120);\ncolor: rgb(246, 245, 244);") 
        self.listView.setStyleSheet("background-color: rgba(36, 31, 49, 120);\ncolor: rgb(246, 245, 244);")
        self.lineEdit.setStyleSheet("background-color: rgba(36, 31, 49, 120);\ncolor: rgb(246, 245, 244);")
        self.menubar.setStyleSheet("background-color: rgba(36, 31, 49, 120);\ncolor: rgb(246, 245, 244);")
        self.label_icon.setStyleSheet("background-color: rgba(36, 31, 49, 120);\ncolor: rgb(246, 245, 244);")

    
    def light_mode(self) -> None:
        '''
        Set Theme to Light Mode
        :param: None
        :return: None        
        '''        
        self.setStyleSheet("background-color: rgba(245, 245, 245, 0.8);\ncolor: rgba(50, 50, 50, 1);")       
        self.listView.setStyleSheet("background-color: rgba(245, 245, 245, 0.8);\ncolor: rgba(50, 50, 50, 1);")
        self.lineEdit.setStyleSheet("background-color: rgba(245, 245, 245, 0.8);\ncolor: rgba(50, 50, 50, 1);")
        self.menubar.setStyleSheet("background-color: rgba(245, 245, 245, 0.8);\ncolor: rgba(50, 50, 50, 1);")
        self.label_icon.setStyleSheet("background-color: rgba(245, 245, 245, 0.8);\ncolor: rgba(50, 50, 50, 1);")

    def on_text_changed(self) -> None:
        '''
        Start a debounce timer for API calls when the text changes in the input box.
        :param: None
        :return: None
        '''
        self.suggestion_timer.start(300)  # 300ms debounce delay

    def get_city_state(self, city_name: str) -> list:
        '''
        Retrieve matching city names based on user input.
        :param city_name: The name of the city entered by the user.
        :return: A list of matching city names or an error message.
        '''
        geolocator = Nominatim(user_agent="Weather app (mail@gmail.com)")

        try:
            # Perform geocoding to find matching cities
            location = geolocator.geocode(city_name, exactly_one=False, language='en')

            if location:
                return [loc.address for loc in location]
            else:
                return ["No matches found."]
        except GeocoderTimedOut:
            return ["Geocoding service timed out. Please try again later."]

    def display_selected_city_weather(self) -> None:
        '''
        Update the weather display based on the selected city from the list.
        :param: None
        :return: None
        '''
        selected_items = self.listView.selectedIndexes()
        if selected_items:
            selected_city = selected_items[0].data()
            self.city_name = selected_city
            self.lineEdit.blockSignals(True)  # Avoid triggering on_text_changed
            self.lineEdit.setText(selected_city)
            self.lineEdit.blockSignals(False)

            self.get_weather()

    def toggle_city_editing(self) -> None:
        '''
        Enable or disable city name editing for weather search.
        :param: None
        :return: None
        '''
        self.lineEdit.clear()
        self.model.clear()

        self.listView.setSelectionMode(QListView.SingleSelection)

        enabled = not self.lineEdit.isEnabled()
        self.lineEdit.setEnabled(enabled)
        self.lineEdit.setFocus()

        self.allow_suggestions = enabled
        if not enabled:  # If disabled, reset city name to 'geo'
            self.lineEdit.setText(self.city['geo'] if self.city['geo'] else self.city['default'])

    def suggest_city_name(self) -> None:
        '''
        Provide city name suggestions in the list view.
        :param: None
        :return: None
        '''
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
        '''
        Retrieve API_KEY
        :param: None
        :return: string of the API_KEY

        Place you API_KEY in api_key.txt file or hard code it
        '''
        try:
            with open('api_key.txt', 'r') as file:
                API_KEY = file.read().strip()
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "API key file not found!")
            return
        return API_KEY

    def get_weather(self) -> None:
        '''
        Fetch and process weather data for the selected city.
        :param: None
        :return: None
        '''
        BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"

        self.city_name = self.lineEdit.text() or self.city['default']
        url = f"{BASE_URL}appid={self.API_KEY}&q={self.city_name}"

        response = requests.get(url)
        if response.status_code != 200:
            return

        response = response.json()

        self.city['geo'] = response['name']
        self.coordinates = f"Longitude: {response['coord']['lon']}, Latitude: {response['coord']['lat']}"
        self.condition = response['weather'][0]['description']
        self.weather = {
            'temp': (response['main']['temp'] - 273.15) * 1.8 + 32,
            'feel like': (response['main']['feels_like'] - 273.15) * 1.8 + 32,
            'Low': (response['main']['temp_min'] - 273.15) * 1.8 + 32,
            'High': (response['main']['temp_max'] - 273.15) * 1.8 + 32,
            'humidity': response['main']['humidity'],
            'icon': response['weather'][0]['icon']
        }
        
        self.icon_path = f'icons/{self.weather["icon"]}.png'
        self.icon_pixmap =QPixmap(self.icon_path)

        self.wind = response['wind']['speed']

        local_timezone = dt.timezone(dt.timedelta(seconds=response['timezone']))
        current_utc_time = dt.datetime.now(dt.timezone.utc)
        self.current_local_time = current_utc_time.astimezone(local_timezone)

        self.sunrise = dt.datetime.fromtimestamp(response['sys']['sunrise'], tz=local_timezone)
        self.sunset = dt.datetime.fromtimestamp(response['sys']['sunset'], tz=local_timezone)
        self.display_weather()

    def format_time(self, time) -> str:
        '''
        Format a datetime object to a string representing time in Hour:Minute format.

        :param time: A datetime object to be formatted.
        :return: A string representing the formatted time in HH:MM format.
        '''
        return time.strftime('%H:%M')
    
    def update_current_time(self) -> None:
        '''
        Update the displayed current local time every minute.
        :param: None
        :return: None
        '''
        self.current_local_time = self.current_local_time + dt.timedelta(seconds=1)
        self.time_label.setText(self.format_time(self.current_local_time))
    

    def display_weather(self) -> None:
        '''
        Display the retrieved weather data in the list view.
        :param: None
        :return: None
        '''
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
            f"Coordinates: {self.coordinates}"
        ]
        
        for detail in weather_details:
            self.model.appendRow(QStandardItem(detail))
        
        self.label_icon.setPixmap(self.icon_pixmap)
        self.label_icon.setScaledContents(True)

        self.listView.setSelectionMode(QListView.NoSelection)
        self.lineEdit.setEnabled(False)

        self.update_current_time()