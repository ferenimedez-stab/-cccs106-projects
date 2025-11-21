"""Weather Application using Flet v0.28.3 """

import flet as ft
from weather_service import WeatherService
from config import Config
from datetime import datetime
import json
from pathlib import Path
import httpx
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO
import base64
import asyncio
import pytz


class WeatherApp:
    """Main Weather Application class."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.weather_service = WeatherService()
        self.current_city = ""
        self.current_weather_data = None
        self.history_file = Path("mod6_labs/search_history.json")
        self.search_history = self.load_history()
        self.preferences_file = Path("mod6_labs/user_preferences.json")
        self.load_preferences()
        self.setup_page()
        self.build_ui()

        # Start the live clock
        self.page.run_task(self.update_clock)

        # Start location detection
        self.page.run_task(self.get_current_location_weather)

    def setup_page(self):
        """Configure page settings."""
        self.page.title = Config.APP_TITLE
        self.page.fonts = {"Kana_Regular": "D:/3rd Year/SEM1/Finals/AppDET/weather_app/assets/kana-sans/Kana Sans Regular.ttf",
                           "Kana_Bold": "D:/3rd Year/SEM1/Finals/AppDET/weather_app/assets/kana-sans/Kana Sans Bold.ttf",
                           "Kana_Italic": "D:/3rd Year/SEM1/Finals/AppDET/weather_app/assets/kana-sans/Kana Sans Italic.ttf",
                           "Kana_Medium": "D:/3rd Year/SEM1/Finals/AppDET/weather_app/assets/kana-sans/Kana Sans Medium.ttf",
                           "Kana_MediumItalic": "D:/3rd Year/SEM1/Finals/AppDET/weather_app/assets/kana-sans/Kana Sans Medium Italic.ttf"
                           }

        self.page.theme = ft.Theme(font_family = "Kana_Regular",
                                   scrollbar_theme = ft.ScrollbarTheme(radius = 3,
                                                                       thickness = 6,
                                                                       main_axis_margin = -8,
                                                                       cross_axis_margin = -3))
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20
        self.page.window.width = Config.APP_WIDTH
        self.page.window.height = Config.APP_HEIGHT
        self.page.window.resizable = False
        self.page.scroll = ft.ScrollMode.ADAPTIVE
        self.page.window.minimizable = False
        self.page.window.maximizable = False
        self.page.window.center()

    def build_ui(self):
        """Build the user interface."""
        # Title
        self.title = ft.Text("Weather App",
                            size = 32,
                            font_family = "Kana_Bold",
                            weight = ft.FontWeight.BOLD,
                            color = ft.Colors.BLUE_700)

        self.theme_toggle = ft.IconButton(icon = ft.Icons.DARK_MODE if self.theme_mode == ft.ThemeMode.LIGHT else ft.Icons.LIGHT_MODE,
                                          tooltip = "Toggle Theme",
                                          on_click = self.toggle_theme)

        self.unit_toggle = ft.TextButton(text = "°F" if self.current_unit == "imperial" else "°C",
                                         on_click = self.toggle_units,
                                         tooltip = "Toggle Temperature Unit",
                                         style = ft.ButtonStyle(color = ft.Colors.BLUE_GREY_500,
                                                                bgcolor = ft.Colors.BLUE_GREY_50,
                                                                shape = ft.CircleBorder(),
                                                                padding = ft.Padding(5, 0, 9, 0)))

        self.toggle_row = ft.Row([self.theme_toggle,
                                  self.unit_toggle],
                                  alignment = ft.MainAxisAlignment.END,
                                  spacing = 0)

        self.title_row = ft.Row(controls = [self.title,
                                            self.toggle_row],
                                alignment = ft.MainAxisAlignment.SPACE_BETWEEN)

        self.search_bar_list = ft.ListView(height = 250,
                                           spacing = 0,
                                           padding = 5)

        self.city_input = ft.SearchBar(bar_hint_text = "Enter city name...",
                                       view_hint_text = "Search city",
                                       view_header_text_style = ft.TextStyle(color = ft.Colors.BLACK),
                                       bar_text_style = ft.TextStyle(color = ft.Colors.BLACK),
                                       bar_shape = ft.RoundedRectangleBorder(radius = 10),
                                       view_shape = ft.RoundedRectangleBorder(radius = 10),
                                       bar_border_side= ft.BorderSide(1, ft.Colors.BLUE_200),
                                       bar_elevation = 0,
                                       view_elevation = 1,
                                       bar_bgcolor = ft.Colors.WHITE,
                                       view_bgcolor = ft.Colors.WHITE,
                                       view_size_constraints = ft.BoxConstraints(max_height = 210),
                                       on_change = self.on_input_change,
                                       on_tap = self.open_search_history,
                                       on_submit = self.on_search,
                                       controls = [self.search_bar_list],
                                       full_screen = False,
                                       expand = True)

        # Create live clock
        self.timezone_global = None
        self.city_global = None

        self.clock = ft.Text("00:00:00",
                            size = 14,
                            text_align = ft.TextAlign.CENTER,
                            color = ft.Colors.GREY_900)

        # Search button
        self.search_button = ft.IconButton(icon = ft.Icons.SEARCH,
                                           on_click = self.on_search,
                                           style = ft.ButtonStyle(color = ft.Colors.BLUE_600),
                                           tooltip = "Search")

        self.location_button = ft.IconButton(icon = ft.Icons.MY_LOCATION,
                                             style = ft.ButtonStyle(color = ft.Colors.BLUE_600,
                                                                    ),
                                             tooltip = "Use my location",
                                             on_click = lambda e: self.page.run_task(self.get_current_location_weather))


        self.clear_history_btn = ft.IconButton(icon = ft.Icons.DEBLUR_OUTLINED,
                                               tooltip = "Clear history",
                                               on_click = self.clear_history,
                                               visible = len(self.search_history) > 0,
                                               style = ft.ButtonStyle(color = ft.Colors.BLUE_600,))


        self.search_cont = ft.Column(controls = [ft.Row(controls = [self.city_input,
                                                                    self.search_button,
                                                                    self.location_button,
                                                                    self. clear_history_btn],),
                                                    ],
                                      spacing = 5)

        # Loading indicator
        self.loading = ft.ProgressRing(visible = False,
                                       color = ft.Colors.BLUE_600,
                                       semantics_label = "Loading...",
                                       stroke_cap = ft.StrokeCap.BUTT
                                       )

        # Error message
        self.error_message = ft.Text("",
                                     color = ft.Colors.WHITE)

        self.error_column = ft.Row([ft.Icon(ft.Icons.INFO_OUTLINE,
                                            color = ft.Colors.WHITE),
                                       self.error_message])

        self.error_msg_cont = ft.Row([ft.Container(content = self.error_column,
                                                bgcolor = ft.Colors.BLUE_400,
                                                expand_loose = True,
                                                padding = 20,
                                                border_radius = 10,
                                                alignment = ft.alignment.center)],
                                    alignment = ft.MainAxisAlignment.CENTER,
                                    visible = False)
        # Current weather column
        self.weather_row = ft.Row(spacing = 10,
                                  alignment = ft.MainAxisAlignment.CENTER,
                                  vertical_alignment = ft.CrossAxisAlignment.CENTER,
                                  wrap = True)

        self.forecast_column = ft.Column(spacing = 10)

        self.forecast_row = ft.Row(spacing = 10,
                                   scroll = ft.ScrollMode.AUTO,
                                   wrap = False)

        self.current_weather_tab_content = ft.Container(content = ft.Column([self.weather_row],
                                                                            scroll = ft.ScrollMode.AUTO),
                                                        bgcolor = ft.Colors.BLUE_50,
                                                        border_radius = 10,
                                                        padding = 20)

        self.current_weather_tab = ft.Tab(text = "Current",
                                        icon = ft.Icons.WB_SUNNY,
                                        content = self.current_weather_tab_content)

        self.forecast_tab_content = ft.Container(content = ft.Column([self.forecast_column],
                                                                            scroll = ft.ScrollMode.AUTO),
                                                            bgcolor = ft.Colors.BLUE_50,
                                                            border_radius = 10,
                                                            padding = 20)

        self.forecast_tab = ft.Tab(text = "Forecasts",
                                    icon = ft.Icons.CALENDAR_MONTH,
                                    content = self.forecast_tab_content)

        # Tabs for Current and Forecast
        self.tabs = ft.Tabs(visible = False,
                            selected_index = 0,
                            animation_duration = 300,
                            height = Config.APP_HEIGHT - 250,
                            scrollable = True,
                            expand = True,
                            tab_alignment = ft.TabAlignment.CENTER,
                            tabs = [self.current_weather_tab,
                                    self.forecast_tab])

        # Add all components to page
        self.page.add(ft.Column([self.title_row,
                                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                                self.search_cont,
                                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                                self.loading,
                                self.error_msg_cont,
                                self.tabs],
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                            spacing = 10))


    def load_preferences(self):
        """Load user preferences."""
        if self.preferences_file.exists():
            try:
                with open(self.preferences_file, 'r') as f:
                    prefs = json.load(f)
                    self.current_unit = prefs.get('unit', 'metric')
                    theme = prefs.get('theme', 'light')
                    self.theme_mode = ft.ThemeMode.DARK if theme == 'dark' else ft.ThemeMode.LIGHT
            except:
                self.current_unit = Config.UNITS
                self.theme_mode = ft.ThemeMode.LIGHT
        else:
            self.current_unit = Config.UNITS
            self.theme_mode = ft.ThemeMode.LIGHT

    def save_preferences(self):
        """Save user preferences."""
        try:
            prefs = {
                'unit': self.current_unit,
                'theme': 'dark' if self.theme_mode == ft.ThemeMode.DARK else 'light'
            }
            with open(self.preferences_file, 'w') as f:
                json.dump(prefs, f)
        except Exception as e:
            print(f"Error saving preferences: {e}")

    def toggle_theme(self, e):
        """Toggle between light and dark theme."""
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.theme_mode = ft.ThemeMode.DARK
            self.theme_toggle.icon = ft.Icons.LIGHT_MODE
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.theme_mode = ft.ThemeMode.LIGHT
            self.theme_toggle.icon = ft.Icons.DARK_MODE

        self.save_preferences()
        self.page.update()

    def toggle_units(self, e):
        """Toggle between Celsius and Fahrenheit."""
        if self.current_unit == Config.UNITS:
            self.current_unit = "imperial"
            self.unit_toggle.text = "°F"
        else:
            self.current_unit = Config.UNITS
            self.unit_toggle.text = "°C"

        self.save_preferences()

        # Redisplay current weather if available
        if self.current_weather_data:
            self.weather_row.controls.clear()
            self.forecast_column.controls.clear()
            self.display_weather(self.current_weather_data)
            # Refetch forecast with new units
            self.page.run_task(self.refresh_forecast)

        self.page.update()

    async def refresh_forecast(self):
        """Refresh forecast with current units."""
        if self.current_city:
            try:
                forecast_data = await self.weather_service.get_forecast(self.current_city)
                if forecast_data:
                    self.display_forecast(forecast_data)
                self.page.update()
            except:
                pass

    async def update_clock(self):
        """Update live clock every second using self.timezone_global if available."""
        while True:
            try:
                # Get current time with timezone from API if available
                if self.timezone_global:
                    try:
                        # If timezone_global is string, try to resolve it via pytz
                        if isinstance(self.timezone_global, str):
                            tz = pytz.timezone(self.timezone_global)
                            now = datetime.now(tz)
                        else:
                            # Expect numeric minute offset for FixedOffset
                            # pytz.FixedOffset expects minutes east of UTC
                            minutes = int(self.timezone_global)
                            tz = pytz.FixedOffset(minutes)
                            now = datetime.now(tz)
                    except Exception:
                        # Invalid timezone -> fallback to local time
                        now = datetime.now()
                else:
                    now = datetime.now()

                # Update clock text control if existing
                if hasattr(self, "clock") and self.clock:
                    # 12-hour format
                    self.clock.value = now.strftime("%I:%M:%S %p").lstrip('0')

                if hasattr(self, "page") and self.page:
                    self.page.update()

            except Exception:
                pass

            await asyncio.sleep(1)

    def open_search_history(self, e):
        """Open search history view only if there's history."""
        if len(self.search_history) > 0:
            # Populate with all recent searches
            self.search_bar_list.controls.clear()
            for city in self.search_history[:5]:
                self.search_bar_list.controls.append(
                    ft.ListTile(title = ft.Text(city,
                                                color = ft.Colors.BLACK),
                                leading = ft.Icon(ft.Icons.HISTORY),
                                data = city,
                                on_click = self.select_from_history))
            self.city_input.update()
            self.city_input.open_view()

    def on_input_change(self, e):
        """Filter search history based on input."""
        query = e.data.lower()

        filtered = ([c for c in self.search_history if query in c.lower()] if query else self.search_history)

        filtered = filtered[:5]     # Limit to 5 results

        self.search_bar_list.controls.clear()

        for city in filtered:
            self.search_bar_list.controls.append(
                ft.ListTile(title = ft.Text(city),
                            leading = ft.Icon(ft.Icons.HISTORY,
                                              size = 18,
                                              color = ft.Colors.BLACK),
                            height = 250,
                            data = city,
                            on_click = self.select_from_history))

        self.city_input.update()

    def select_from_history(self, e):
        """Select city from search history."""
        city = e.control.data

        # Set value BEFORE closing
        self.city_input.value = city

        # Close view with the city name (this preserves the value)
        self.city_input.close_view(city)

        # Update
        self.page.update()

        # Trigger search
        self.page.run_task(self.get_weather_data)

    async def get_current_location_weather(self):
        """Get weather for current location using IP."""
        self.loading.visible = True
        self.page.update()

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://ipapi.co/json/")
                data = response.json()
                city = data.get('city', '')

                # ipapi.co returns a timezone string like 'America/Los_Angeles'
                tz_name = data.get('timezone')
                if tz_name:
                    self.timezone_global = tz_name

                if city:
                    self.city_input.value = city
                    self.page.update()
                    await self.get_weather_data()
                else:
                    self.show_error("Could not detect your location")
        except Exception as e:
            self.show_error("Could not detect your location")
        finally:
            self.loading.visible = False
            self.page.update()

    def load_history(self):
        """Load search history from file."""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_history(self):
        """Save search history to file."""
        try:
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.history_file, 'w') as f:
                json.dump(self.search_history, f, indent = 2)
        except Exception as e:
            print(f"Error saving history: {e}")

    def add_to_history(self, city: str):
        """Add city to history."""
        if city in self.search_history:
            self.search_history.remove(city)

        self.search_history.insert(0, city)
        self.search_history = self.search_history[:10]
        self.save_history()
        self.clear_history_btn.visible = len(self.search_history) > 0
        self.page.update()

    def clear_history(self, e):
        """Clear search history."""
        self.search_history.clear()
        if self.history_file.exists():
            self.history_file.unlink()
        self.clear_history_btn.visible = False
        self.page.update()

    def on_search(self, e):
        """Handle search button click or enter key press."""
        self.page.update()
        self.page.run_task(self.get_weather_data)

    async def get_weather_data(self):
        """Fetch and display weather and forecast data."""
        city = (self.city_input.value or "").strip()

        if not city:
            self.show_error("Please enter a city name")
            return

        self.loading.visible = True
        self.error_msg_cont.visible = False
        self.tabs.visible = False
        self.page.update()

        try:
            self.current_city = city

            # Fetch with current units
            weather_data = await self.weather_service.get_weather(city)
            forecast_data = await self.weather_service.get_forecast(city)

            # If the weather API provides a timezone offset in seconds, store
            # it as minutes (to be compatible with pytz.FixedOffset).
            # OpenWeatherMap current weather typically includes 'timezone' (seconds).
            if isinstance(weather_data, dict):
                tz_val = weather_data.get('timezone')
                if tz_val is not None:
                    try:
                        tz_seconds = int(tz_val)
                        self.timezone_global = int(tz_seconds / 60)
                    except Exception:
                        # ignore if transforming fails
                        pass

            self.current_weather_data = weather_data

            self.weather_row.controls.clear()
            self.forecast_column.controls.clear()

            self.display_weather(weather_data)

            if forecast_data:
                self.display_forecast(forecast_data)

            self.add_to_history(city)
            self.tabs.visible = True
            self.error_msg_cont.visible = False

        except Exception as e:
            self.show_error(str(e))

        finally:
            self.loading.visible = False
            self.page.update()

    def get_weather_color(self, condition: str):
        """Get background gradient based on weather condition."""
        condition = condition.lower()
        if 'clear' in condition or 'sunny' in condition:
            return ft.LinearGradient(
                begin = ft.alignment.top_right,
                end = ft.alignment.bottom_left,
                colors = [ft.Colors.AMBER_200, ft.Colors.ORANGE_50, ft.Colors.YELLOW_50])
        elif 'cloud' in condition:
            return ft.LinearGradient(
                begin = ft.alignment.top_right,
                end = ft.alignment.bottom_left,
                colors = [ft.Colors.BLUE_GREY_300, ft.Colors.BLUE_GREY_50, ft.Colors.WHITE])

        elif 'rain' in condition or 'drizzle' in condition:
            return ft.LinearGradient(
                begin = ft.alignment.top_right,
                end = ft.alignment.bottom_left,
                colors = [ft.Colors.BLUE_200, ft.Colors.LIGHT_BLUE_50, ft.Colors.CYAN_50])

        elif 'snow' in condition:
            return ft.LinearGradient(
                begin = ft.alignment.top_right,
                end = ft.alignment.bottom_left,
                colors = [ft.Colors.LIGHT_BLUE_100, ft.Colors.CYAN_50, ft.Colors.WHITE])

        elif 'thunder' in condition or 'storm' in condition:
            return ft.LinearGradient(
                begin = ft.alignment.top_right,
                end = ft.alignment.bottom_left,
                colors = [ft.Colors.DEEP_PURPLE_100, ft.Colors.PURPLE_50, ft.Colors.INDIGO_50])

        elif 'mist' in condition or 'fog' in condition:
            return ft.LinearGradient(
                begin = ft.alignment.top_right,
                end = ft.alignment.bottom_left,
                colors = [ft.Colors.GREY_200, ft.Colors.GREY_100, ft.Colors.WHITE])

        else:
            return ft.LinearGradient(
                begin = ft.alignment.top_left,
                end = ft.alignment.bottom_right,
                colors = [ft.Colors.BLUE_50, ft.Colors.LIGHT_BLUE_50, ft.Colors.WHITE])

    def convert_temp(self, temp_celsius: float):
        """Convert temperature based on current unit."""
        if self.current_unit == "imperial":
            return (temp_celsius * 9/5) + 32
        return temp_celsius

    def get_unit_symbol(self):
        """Get temperature unit symbol."""
        return "°F" if self.current_unit == "imperial" else "°C"

    def display_weather(self, data: dict):
        """Display current weather information."""
        city_name = data.get("name", "Unknown")
        country = data.get("sys", {}).get("country", "")
        temp = self.convert_temp(data.get("main", {}).get("temp", 0))
        feels_like = self.convert_temp(data.get("main", {}).get("feels_like", 0))
        humidity = data.get("main", {}).get("humidity", 0)
        description = data.get("weather", [{}])[0].get("description", "").title()
        icon_code = data.get("weather", [{}])[0].get("icon", "01d")
        wind_speed = data.get("wind", {}).get("speed", 0)

        # Ensure high and low temps are available (use current temp as fallback)
        high = self.convert_temp(data.get("main", {}).get("temp_max", data.get("main", {}).get("temp", 0)))
        low = self.convert_temp(data.get("main", {}).get("temp_min", data.get("main", {}).get("temp", 0)))

        # Get weather-based color
        bg_color = self.get_weather_color(description)

        # Update tab background (use gradient property for LinearGradient)
        self.current_weather_tab_content.gradient = bg_color
        self.forecast_tab_content.gradient = bg_color

        unit = self.get_unit_symbol()

        # Build location + date + clock block. Date will respect timezone_global when available.
        try:
            if self.timezone_global:
                if isinstance(self.timezone_global, str):
                    tz = pytz.timezone(self.timezone_global)
                    now_local = datetime.now(tz)
                else:
                    minutes = int(self.timezone_global)
                    tz = pytz.FixedOffset(minutes)
                    now_local = datetime.now(tz)
            else:
                now_local = datetime.now()
        except Exception:
            now_local = datetime.now()

        date_text = now_local.strftime("%A, %b %d %Y  |  ")

        self.weather_row.controls.extend([ft.Container(content = ft.Column([ft.Row([ft.Icon(ft.Icons.LOCATION_ON,
                                                                                            color =  ft.Colors.BLUE_900),

                                                                                    ft.Text(f"{city_name}, {country}",
                                                                                            size = 24,
                                                                                            font_family = "Kana_Bold",
                                                                                            weight = ft.FontWeight.BOLD,
                                                                                            color = ft.Colors.BLUE_700)],
                                                                            alignment = ft.MainAxisAlignment.CENTER),

                                                                            ft.Row([ft.Text(date_text,
                                                                                            size = 14,
                                                                                            text_align = ft.TextAlign.CENTER,
                                                                                            color = ft.Colors.GREY_900),
                                                                                    self.clock],
                                                                                   alignment = ft.MainAxisAlignment.CENTER,
                                                                                   spacing = 0)],

                                                                            horizontal_alignment = ft.CrossAxisAlignment.CENTER),
                                                                            margin = ft.Margin(0, 10, 0, 0)),

                                            ft.Row([ft.Container(content = ft.Column([ft.Text(f"{temp:.1f}{unit}",
                                                                                      size = 48,
                                                                                      font_family = "Kana_Bold",
                                                                                      color = ft.Colors.BLUE_900),

                                                                                    ft.Text(f"Feels like {feels_like:.1f}{unit}",
                                                                                            size = 14,
                                                                                            color = ft.Colors.GREY_700),

                                                                                    ft.Row([ft.Text(f"↑ {high:.1f}{unit}",
                                                                                                    size = 13,
                                                                                                    weight = ft.FontWeight.BOLD,
                                                                                                    color = ft.Colors.GREY_700),

                                                                                            ft.Text(f"↓ {low:.1f}{unit}",
                                                                                                    size = 13,
                                                                                                    weight = ft.FontWeight.BOLD,
                                                                                                    color = ft.Colors.GREY_700)],

                                                                                    alignment = ft.MainAxisAlignment.SPACE_EVENLY)],
                                                                                    spacing = 5,
                                                                                    horizontal_alignment = ft.CrossAxisAlignment.CENTER),
                                                        padding = ft.Padding(0, 15, 0, 10)
                                                        ),

                                                    ft.Container(height = 130,
                                                                margin = 0,
                                                                padding = 0,
                                                                content = ft.Column([ft.Image(src = f"https://openweathermap.org/img/wn/{icon_code}@2x.png",
                                                                                                width = 130,
                                                                                                height = 100,
                                                                                                fit = ft.ImageFit.CONTAIN),

                                                                                    ft.Text(description,
                                                                                            size = 16,
                                                                                            font_family = "Kana_MediumItalic",
                                                                                            text_align = ft.TextAlign.CENTER,
                                                                                            color = ft.Colors.GREY_700)],

                                                                                    spacing = 0,
                                                                                    horizontal_alignment = ft.CrossAxisAlignment.CENTER))],
                                                    alignment = ft.MainAxisAlignment.CENTER)])

        self.weather_row.controls.append(ft.Container(ft.Row([self.create_info_card(ft.Icons.WATER_DROP,
                                                                       ft.Colors.BLUE_600,
                                                                       "Humidity",
                                                                       f"{humidity}%"),

                                                        self.create_info_card(ft.Icons.AIR,
                                                                            ft.Colors.LIGHT_BLUE_ACCENT_200,
                                                                            "Wind Speed",
                                                                            f"{wind_speed} m/s"),

                                                        self.create_info_card(ft.Icons.COMPRESS,
                                                                            ft.Colors.PURPLE_ACCENT_400,
                                                                            "Pressure",
                                                                            f"{data.get('main', {}).get('pressure', 0)} hPa"),

                                                        self.create_info_card(ft.Icons.WB_CLOUDY,
                                                                            ft.Colors.GREY_300,
                                                                            "Cloudiness",
                                                                            f"{data.get('clouds', {}).get('all', 0)}%")],

                                                        alignment = ft.MainAxisAlignment.CENTER,
                                                        wrap = True),

                                            margin = ft.Margin(0, 10, 0, 0)))

    def display_forecast(self, data: dict):
        """Display 5-day forecast with charts."""
        if not data or "list" not in data:
            return

        city_name = data.get("city", {}).get("name", self.current_city)
        unit = self.get_unit_symbol()

        # Build chart container first (24-hour chart)S
        chart_container = self.add_forecast_charts(data, city_name, unit)

        # Group forecast data by day
        daily_forecasts = {}

        for item in data["list"]:
            dt = datetime.fromtimestamp(item["dt"])
            date_key = dt.strftime("%Y-%m-%d")
            day_name = dt.strftime("%A")

            if date_key not in daily_forecasts:
                daily_forecasts[date_key] = {
                    "day_name": day_name,
                    "date": dt.strftime("%b %d"),
                    "temps": [],
                    "conditions": [],
                    "icons": [],
                    "humidity": [],
                    "wind_speed": []
                }

            daily_forecasts[date_key]["temps"].append(item["main"]["temp"])
            daily_forecasts[date_key]["conditions"].append(
                item["weather"][0]["description"]
            )
            daily_forecasts[date_key]["icons"].append(
                item["weather"][0]["icon"]
            )
            daily_forecasts[date_key]["humidity"].append(item["main"]["humidity"])
            daily_forecasts[date_key]["wind_speed"].append(item["wind"]["speed"])

        # Clear previous forecast cards
        self.forecast_row.controls.clear()

        for date_key in sorted(daily_forecasts.keys())[:5]:
            day_data = daily_forecasts[date_key]

            high_temp = self.convert_temp(max(day_data["temps"]))
            low_temp = self.convert_temp(min(day_data["temps"]))

            most_common_condition = max(set(day_data["conditions"]),
                                    key = day_data["conditions"].count)
            most_common_icon = max(set(day_data["icons"]),
                                key = day_data["icons"].count)

            avg_humidity = sum(day_data["humidity"]) / len(day_data["humidity"])
            avg_wind = sum(day_data["wind_speed"]) / len(day_data["wind_speed"])

            self.forecast_row.controls.append(self.create_forecast_card(day_data["day_name"],
                                                                        day_data["date"],
                                                                        high_temp,
                                                                        low_temp,
                                                                        most_common_condition,
                                                                        most_common_icon,
                                                                        avg_humidity,
                                                                        avg_wind,
                                                                        unit))

        # Create the 5-day cards container
        cards_wrapper = ft.Container(content = self.forecast_row,
                                     alignment = ft.alignment.center)

        # Title for 5-day cards (will be grouped with the cards below)
        fiveday_title = ft.Text(f"What to expect over the next 5 days",
                                size = 22,
                                font_family = "Kana_Regular",
                                color = ft.Colors.BLUE_GREY_900,
                                text_align = ft.TextAlign.CENTER)

        five_day_cont = ft.Container(content = ft.Column([fiveday_title,
                                                          cards_wrapper],
                                    spacing = 10,
                                    horizontal_alignment = ft.CrossAxisAlignment.CENTER),
                                    gradient = ft.LinearGradient(
                                        begin = ft.alignment.top_right,
                                        end = ft.alignment.bottom_left,
                                        colors = [ft.Colors.BLUE_50,
                                                  ft.Colors.LIGHT_BLUE_50,
                                                  ft.Colors.WHITE]),
                                    border_radius = 10,
                                    shadow = ft.BoxShadow(blur_radius = 8,
                                                           color = ft.Colors.GREY_400),
                                    padding = 15,
                                    margin = ft.Margin(15, 0, 15, 0),
                                    alignment = ft.alignment.center)

        # Parent container: stack chart (24h) above the 5-day container
        parent = ft.Container(content = ft.Column([chart_container,
                                                   five_day_cont],
                                                   spacing = 15),
                                                   expand = True)

        self.forecast_column.controls.append(parent)

    def add_forecast_charts(self, data: dict, city_name: str, unit: str):
        """Add charts to the forecast tab using matplotlib."""
        # Extract data for 24-hour chart
        timestamps = []
        temps = []
        feels_like_temps = []

        for item in data["list"][:8]:  # Next 24 hours (3-hour intervals)
            dt = datetime.fromtimestamp(item["dt"])
            timestamps.append(dt)
            temps.append(self.convert_temp(item["main"]["temp"]))
            feels_like_temps.append(self.convert_temp(item["main"]["feels_like"]))

        # Add title
        chart_title = ft.Text(f"Today's Temperature Trend in {city_name}",
                               size = 22,
                               font_family = "Kana_Regular",
                               color = ft.Colors.BLUE_GREY_900,
                               text_align = ft.TextAlign.CENTER)

        # Create matplotlib figure
        fig, ax = plt.subplots(figsize = (11, 5.5))
        fig.patch.set_facecolor('#FAFAFA')
        fig.patch.set_alpha(0.0)

        # Set styling
        ax.set_facecolor("#F8FCFF00")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#BBDEFB')
        ax.spines['bottom'].set_color('#BBDEFB')
        ax.spines['left'].set_linewidth(1.5)
        ax.spines['bottom'].set_linewidth(1.5)

        # Plot temperature line with gradient fill
        line1 = ax.plot(timestamps, temps,
                        marker = 'o',
                        linewidth = 3.5,
                        markersize = 10,
                        label = f'Temperature ({unit})',
                        color = '#FF6B35',
                        markerfacecolor = '#FF6B35',
                        markeredgecolor = 'white',
                        markeredgewidth = 2.5,
                        zorder = 3)

        # Add gradient fill under temperature line
        ax.fill_between(timestamps, temps,
                        alpha = 0.3,
                        color = '#FF6B35',
                        zorder = 1)

        # Plot feels like line
        ax.plot(timestamps, feels_like_temps,
                linestyle = '--',
                linewidth = 2.5,
                marker = 's',
                markersize = 7,
                label = 'Feels Like',
                color = '#7B68EE',
                markerfacecolor = '#7B68EE',
                markeredgecolor = 'white',
                markeredgewidth = 2,
                alpha = 0.85,
                zorder = 2)

        # Labels with modern styling
        ax.set_xlabel('Time',
                    fontsize = 12,
                    fontweight = '600',
                    color = '#424242',
                    labelpad = 10)

        ax.set_ylabel(f'Temperature ({unit})',
                    fontsize = 12,
                    fontweight = '600',
                    color = '#424242',
                    labelpad = 10)

        legend = ax.legend(loc = 'lower left',
                        fontsize = 11,
                        framealpha = 0.95,
                        edgecolor = '#E3F2FD',
                        fancybox = True,
                        shadow = True,
                        frameon = True)

        legend.get_frame().set_facecolor('#FFFFFF')
        legend.get_frame().set_linewidth(1.5)

        # GRid lines
        ax.grid(True,
            alpha = 0.25,
            linestyle = '-',
            linewidth = 1,
            color = '#90CAF9',
            zorder = 0)

        ax.set_axisbelow(True)

        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))
        plt.setp(ax.xaxis.get_majorticklabels(),
                rotation = 45,
                ha = 'right',
                fontsize = 10,
                color = '#616161')

        plt.setp(ax.yaxis.get_majorticklabels(),
                fontsize = 10,
                color = '#616161')

        # Add subtle annotations on data points
        for i, (x, y) in enumerate(zip(timestamps, temps)):
            if i % 2 == 0:  # Annotate every other point
                ax.annotate(f'{y:.0f}°',
                        xy = (x, y),
                        xytext = (0, 10),
                        textcoords = 'offset points',
                        ha = 'center',
                        fontsize = 9,
                        color = '#FF6B35',
                        fontweight = 'bold',
                        bbox = dict(boxstyle = 'round,pad=0.3',
                                    facecolor = 'white',
                                    edgecolor = '#FF6B35',
                                    alpha = 0.8,
                                    linewidth = 1))


        # Save with higher quality
        buf = BytesIO()

        plt.savefig(buf,
                format = 'png',
                dpi = 120,
                bbox_inches = 'tight',
                facecolor = 'white',
                edgecolor = 'none',
                pad_inches = 0.01)

        buf.seek(0)
        plt.close()

        # Convert to base64 for display
        img_base64 = base64.b64encode(buf.read()).decode()

        # Add chart
        chart_image = ft.Container(content = ft.Image(src_base64 = img_base64,
                                                      fit = ft.ImageFit.CONTAIN),
                                   height = 350,
                                   border_radius = 15,
                                   padding = 10,
                                   margin = ft.margin.only(bottom = 10),
                                   alignment = ft.alignment.center)

        # Wrap title + chart in a container
        chart_container = ft.Container(content = ft.Column([chart_title,
                                                            chart_image],
                                                 spacing = 10,
                                                 horizontal_alignment = ft.CrossAxisAlignment.CENTER),
                                       bgcolor = ft.Colors.TRANSPARENT,
                                       border_radius = 10,
                                       padding = 15,
                                       margin = ft.Margin(10, 0, 10, 10),
                                       alignment = ft.alignment.center)

        return chart_container

    def create_forecast_card(self, day, date, high, low, condition, icon, humidity, wind, unit):
        """Create a forecast card for a single day."""
        return ft.Container(content = ft.Column([ft.Row([ft.Column([ft.Text(day,
                                                                            size = 16,
                                                                            font_family = "Kana_Medium",
                                                                            color = ft.Colors.BLUE_900),

                                                                            ft.Text(
                                                                                date,
                                                                                size = 12,
                                                                                color = ft.Colors.GREY_700)],
                                                                        spacing = 2),

                                                        ft.Image(src = f"https://openweathermap.org/img/wn/{icon}.png",
                                                                 width = 50,
                                                                 height = 50)],
                                                        alignment = ft.MainAxisAlignment.SPACE_BETWEEN),

                                        ft.Text(condition.title(),
                                                size = 14,
                                                italic = True,
                                                color = ft.Colors.GREY_800),

                                        ft.Row([ft.Row([ft.Icon(ft.Icons.WATER_DROP,
                                                                size = 16,
                                                                color = ft.Colors.BLUE_600),

                                                        ft.Text(f"{humidity:.0f}%",
                                                                size = 12,
                                                                color = ft.Colors.GREY_700)],
                                                        spacing = 5),

                                                ft.Row([ft.Icon(ft.Icons.AIR,
                                                                size = 16,
                                                                color = ft.Colors.BLUE_600),

                                                        ft.Text(f"{wind:.1f} m/s",
                                                                size = 12,
                                                                color = ft.Colors.GREY_700)],
                                                        spacing = 5)],
                                                alignment = ft.MainAxisAlignment.SPACE_AROUND),

                                        ft.Row([ft.Text(f"↑ {high:.1f}{unit}",
                                                        size = 12,
                                                        weight = ft.FontWeight.BOLD,
                                                        color = ft.Colors.RED_700),

                                                ft.Text(f"↓ {low:.1f}{unit}",
                                                        size = 12,
                                                        weight = ft.FontWeight.BOLD,
                                                        color = ft.Colors.BLUE_700)],
                                                spacing = 10,
                                                alignment = ft.MainAxisAlignment.SPACE_EVENLY)],
                                        spacing = 10),
                            bgcolor = ft.Colors.WHITE,
                            border_radius = 10,
                            padding = 15,
                            border = ft.border.all(1, ft.Colors.BLUE_200))

    def create_info_card(self, icon, color, label, value):
        """Create an info card for weather details."""
        return ft.Container(content = ft.Column([ft.Icon(icon,
                                                        size = 30,
                                                        color = color),

                                                ft.Text(label,
                                                        size = 12,
                                                        color = ft.Colors.GREY_700,
                                                        font_family = "Open Sans",
                                                        weight = ft.FontWeight.BOLD),

                                                ft.Text(
                                                    value,
                                                    size = 16,
                                                    font_family = "Kana_Medium",
                                                    color = ft.Colors.BLUE_900)],
                                                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                                spacing = 5),
                                bgcolor = ft.Colors.WHITE,
                                border_radius = 10,
                                padding = 15,
                                width = 150)

    def show_error(self, message: str):
        """Display error message."""
        self.error_message.value = f"{message}"
        self.error_msg_cont.visible = True
        self.tabs.visible = False

        self.page.update()

def main(page: ft.Page):
    """Main entry point."""
    WeatherApp(page)

if __name__ == "__main__":
    ft.app(target = main)