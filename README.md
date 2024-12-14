# Weather Application

The **Weather Application** is a Python-based project that provides weather updates for specific cities. The application is built using PyQt5 for the graphical user interface (GUI) and leverages the OpenWeatherMap API to fetch real-time weather data.

---

## Features

- **Real-Time Weather Updates**: Fetch weather details such as temperature, humidity, wind speed, and conditions.
- **City Search**: Search for weather data by entering the name of a city.
- **Beautiful GUI**: Designed using PyQt5 with support for light and dark modes.
- **Sunrise & Sunset Timings**: Displays the local sunrise and sunset times.
- **Icons for Weather Conditions**: Shows icons corresponding to weather conditions.

---

## Installation

### Prerequisites

- Python 3.6 or higher
- An OpenWeatherMap API key

### Steps

1. **Clone the Repository**
   git clone https://github.com/yourusername/Weather.git
   cd Weather
   

2. **Install Dependencies**
   Install all required Python packages:
   pip install -r requirements.txt
   

3. **Add Your API Key**
   Create a file named `api_key.txt` in the `src` folder and paste your OpenWeatherMap API key into it.

4. **Run the Application**
   python src/main.py

---

## Project Structure

.
├── icons/               # Contains weather icons
├── LICENSE              # Project license (e.g., MIT)
├── MANIFEST.in          # Specifies additional files to include in the package
├── README.md            # Project documentation
├── requirements.txt     # List of dependencies
├── setup.py             # Packaging script for installation and distribution
├── src/                 # Source code folder
│   ├── api_key.txt      # File storing API key for OpenWeatherMap
│   ├── main.py          # Entry point for the application
│   ├── __pycache__/     # Compiled Python files (ignored in most cases)
│   ├── view.py          # PyQt5 GUI logic
│   └── weather.py       # Weather fetching and processing logic
├── Ui/                  # Contains UI files created with Qt Designer
│   └── view.ui          # Qt Designer UI file


---

## Usage

1. Launch the application.
2. Use the search bar to enter the name of a city.
3. View the weather details, including temperature, humidity, wind speed, and more.
4. Toggle between light and dark modes using the menu options.
5. Toggle between Heavy and Light translucency.

---

## Dependencies

The application depends on the following Python libraries:

- `PyQt5` - For building the GUI
- `requests` - For making HTTP requests to the OpenWeatherMap API
- `geopy` - For geocoding city names

Install all dependencies using the `requirements.txt` file:
    pip install -r requirements.txt


---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [OpenWeatherMap](https://openweathermap.org/) for providing the weather data API.
- [Qt Designer](https://doc.qt.io/qt-5/qtdesigner-manual.html) for creating the UI layout.



