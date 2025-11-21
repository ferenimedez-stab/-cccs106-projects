# Weather Application - Module 6 Lab

## Student Information
- **Name**: Fernanne Hannah A. Enimedez
- **Student ID**: 231002274
- **Course**: CCCS 106
- **Section**: A

## Project Overview
This is a modern desktop weather app built with Python and Flet. It shows real-time conditions, feels-like temperature, daily highs and lows, and extra details like humidity, wind, pressure, and cloudiness. The interface shifts based on the weather, with clean OpenWeatherMap icons and smooth gradients. It also includes a 5-day outlook with daily ranges, humidity and wind summaries, and a 24-hour temperature trend chart.

It supports auto-location, quick city search with autocomplete, and a history of up to ten recent places. You can switch units, toggle light or dark mode, and keep your preferences saved. There’s also a live clock tied to the city’s timezone, all wrapped in a simple, scrollable layout with clear tabs and helpful indicators.

## Features Implemented

### Base Features
- [x] City search functionality
- [x] Current weather display
- [x] Temperature, humidity, wind speed
- [x] Weather icons
- [x] Error handling
- [x] Modern UI with Material Design

### Enhanced Features
1. **Theme Toggle**
   - **Description**: An icon button for switching the window theme between Light Mode and Dark Mode, providing a moon icon for dark mode and sun icon for light mode.
   - **Reason for choosing this feature**: To provide users with control over the visual appearance they prefer in terms of comfort and readability, especially for use in different lighting conditions.
   - **Challenges and Solution**: None. In the last app we developed, this feature was already implemented, so it became easy for me to add to the page. The theme preference is also saved to a JSON file so it persists between sessions.

2. **Temperature Unit Toggle**
   - **Description**: A circular text button toggle that switches between Celsius (°C) and Fahrenheit (°F), automatically converting all displayed temperatures throughout the app.
   - **Reason for choosing this feature**: To provide users control over which unit they prefer the temperature is in, taking into account which measurement system they are more accustomed to seeing (metric vs imperial).
   - **Challenges and Solution**: I struggled a little with the logic for how to convert temperatures dynamically without re-fetching data from the API. I solved this by writing a `convert_temp()` method that handles the conversion based on the current unit setting, and a `refresh_forecast()` method that re-fetches and displays the forecast data with the new units when toggled.

3. **Auto-Locate/Auto-Locate Button**
   - **Description**: A location pin button that automatically detects the user's current city based on their IP address and fetches weather data for that location.
   - **Reason for choosing this feature**: To provide convenience for users who want to quickly check their local weather without manually typing their city name.
   - **Challenges and Solution**: The location didn't work at first because I was using the wrong API endpoint. I solved this by using the ipapi.co service which provides reliable IP-based geolocation, and added proper error handling for cases where the location cannot be detected, or the user denies location access.

4. **Search History w/ Clear History Button**
   - **Description**: A searchable dropdown that stores the last 10 searched cities and allows users to quickly re-search previous locations. Includes a clear button to delete all history.
   - **Reason for choosing this feature**: To improve user experience by reducing repetitive typing for frequently checked locations and providing quick access to recent searches.
   - **Challenges and Solution**: How to display the search history properly was the main challenge. The logic was more doable, but the UI was difficult. I tried different methods: using a Container for a list, `ListView`, and Cards - all of which had the same issue: the list was updating correctly, but it wasn't visually appealing or functional. Then, I discovered Flet's `SearchBar` component, which was perfect for this use case. I used SearchBar with a ListView inside it, configured to show only 5 items at a time with a fixed height (250px) to prevent the blank white space issue. The history is persisted in a JSON file and updates dynamically as users search for new cities.

5. **Date and Live Clock**
   - **Description**: A real-time clock display showing the current date and time that updates automatically every second.
   - **Reason for choosing this feature**: To provide users with time context while checking the weather, making the app more informative and helping users correlate weather conditions with specific times.
   - **Challenges and Solution**: The clock wasn't updating in real-time initially—it would only refresh when the page reloaded due to other actions. I solved this by switching from the basic datetime module to using pytz for proper timezone handling. The `update_clock()` method now checks if self.timezone_global is available and handles it intelligently: if it's a string, it resolves it as a timezone name via `pytz.timezone()`; if it's numeric, it treats it as a minute offset using `pytz.FixedOffset()`. This ensures the clock displays accurate time for the user's location based on data from the weather API. If no timezone is available or an error occurs, it gracefully falls back to local system time. The clock updates every second without needing to restart the window.

6. **Tabs for Current and Forecasted Weather**
   - **Description**: A tabbed interface with two sections: "Current" for present weather conditions and "Forecasts" for 24-hour and 5-day predictions.
   - **Reason for choosing this feature**: To organize different types of weather information clearly and prevent the interface from being cluttered, allowing users to focus on what they need at the moment.
   - **Challenges and Solution**: None. Creating the tabs was easy with the Flet documentation. I used `ft.Tabs` with icon indicators and configured the height and scrolling properties to fit the window dimensions properly.

7. **Cloudiness and Pressure Information**
   - **Description**: Additional weather metrics displayed as cards showing atmospheric pressure (in hPa) and cloud coverage percentage, complementing the existing humidity and wind speed data.
   - **Reason for choosing this feature**: To provide a more comprehensive weather overview for users who want detailed atmospheric conditions, such as those with weather sensitivity or outdoor activity planning needs.
   - **Challenges and Solutions**: None. I applied the same logic as in the existing code for humidity and wind speed cards, extracting the data from the OpenWeatherMap API response using `data.get('main', {}).get('pressure', 0)` and `data.get('clouds', {}).get('all', 0)`, then creating info cards with appropriate icons.

8. **24-hour Forecast Chart**
   - **Description**: An interactive line graph showing temperature trends over the next 24 hours (in 3-hour intervals) with both actual temperature and "feels like" temperature lines, gradient fills, and data point annotations.
   - **Reason for choosing this feature**: To provide users with a visual understanding of temperature trends throughout the day, making it easier to plan activities and see patterns at a glance rather than reading numbers.
   - **Challenges and Solution**: How to create a chart using matplotlib was the main challenge. Since I already had reference ode for extracting data through the API, presenting it in a chart format was the next hurdle. I used matplotlib because I had prior experience with it. I then had to learn how to customize the chart styling - adding gradient fills, removing unnecessary borders, formatting the x-axis to show times properly, and converting the matplotlib figure to a base64-encoded image that could be displayed in Flet. The biggest challenge was making it look modern and professional, which I solved by researching matplotlib styling options like `fill_between()` for gradients, custom color schemes, and proper annotations.

9. **5-day Foreecast Cards**
   - **Description**: Horizontally scrollable cards displaying daily weather summaries for the next 5 days, showing day name, date, high/low temperatures, weather conditions, humidity, and wind speed for each day.
   - **Reason for choosing this feature**: To give users a quick overview of the week ahead, helping them plan activities and prepare for changing weather conditions over multiple days.
   - **Challenges and Solution**: Since I already had a basis for the information to be displayed on the forecast cards, I only needed to add the day names and dates. For that, I used the `datetime` module and `strftime()` to format the timestamps from OpenWeatherMap's API response. It was, however, a challenge to fix the UI to achieve a horizontally scrollable container with cards arranged side-by-side. What I did was create a `ft.Row` with `scroll = ft.ScrollMode.AUTO` and wrap = False to contain the forecast cards, then added this row to the forecast column. I also had to group the API data by date using a dictionary to aggregate multiple readings per day (since the API returns 3-hourly data) and calculate daily highs, lows, and averages. The final challenge was centering everything properly, which I solved by adding `horizontal_alignment = ft.CrossAxisAlignment.CENTER` to the forecast column.

10. **Error Message Boxes**
   - **Description**: Styled alert boxes that display error messages in a visually distinct format, providing clear feedback when issues occur (such as API failures or invalid inputs).
   - **Reason for choosing this feature**: To present error messages in a cleaner, more emphasized way.
   - **Challenges and Solution**: The main challenge was centering the container that holds the error text within the UI. I solved this by using Flet's alignment properties—specifically setting `horizontal_alignment = ft.CrossAxisAlignment.CENTER` on the parent column container to ensure the error message box appeared centered on the screen, creating a balanced and professional appearance.

## Screenshots
**Main page of the Weather App**
-
This is what the app looks like when ran. It automatically gets the weather data in your location (not accurate).

It loads in the <i>Current Weather</i> tab.

![Landing page of the desktop weather app: window has a fixed dimension](assets\screenshots\image-1.png)

**Forecast Tab**
-
The Forecast tab contains the 24-hour temperature forecast chart and the 5-day weather predictions.

![Forecast Tab - 24-hour](assets\screenshots\image-2.png)
![Forecast Tab - 24-hour](assets\screenshots\image-3.png)

**Search Bar & Search History | Custom weather-informed background colors**
-

1. Shows the city search bar with real-time suggestions and the search history storing up to ten recent locations.

2. Has custom gradient backgrounds that adjusts to match the city’s weather conditions.


![Search Bar & Search History](assets\screenshots\image-5.png)


**Dark Theme | Temperature Unit Switching**
1. Displays the window in its Dark Mode via its toggle.
2. Displays the temperature in Fahrenheit via the button next to the theme toggle.

![Dark Theme and Temperature Unit Change](assets\screenshots\image-6.png)
## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions
```bash
# Clone the repository
git https://github.com/ferenimedez-stab/-cccs106-projects.git
cd -cccs106-projects/mod6_labs

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Add your OpenWeatherMap API key to .env
API_KEY = "3f26673a36c3a2493b8fdd2293be2cd8"