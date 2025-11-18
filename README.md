Русский (Russian)

Odoo Geo Leaflet Map Widget
Краткое описание: Модуль предоставляет настраиваемый виджет поля (field widget) для Odoo, позволяющий пользователям визуально выбирать географические координаты на карте Leaflet, а также устанавливать маркер по введенным координатам и выполнять обратное геокодирование (получение адреса по координатам) с использованием сервиса Nominatim (OpenStreetMap) через библиотеку geopy.

Основные функции
1. Интерактивный выбор координат:
     Пользователь может кликнуть на карте, чтобы установить маркер. Координаты (map_latitude и map_longitude) автоматически           заполняются в форме Odoo.

2. Визуализация введенных координат:
     Включает кнопку Use entered coordinates, которая устанавливает маркер на карте по значениям, введенным вручную в поля            широты и долготы. Это позволяет визуально проверить местоположение по координатам, полученным из любого другого источника.

3. Обратное геокодирование (Backend):
    Кнопка Apply address запускает серверный метод, который использует выбранные или введенные координаты для получения полного      почтового адреса (улица, город, страна) и заполняет соответствующие поля в форме.

- Технические детали
    Odoo Version: 19.0
    Технологии: Leaflet (JS), OWL (JS), Python (geopy)
    Лицензия: LGPL-3

- Установка и использование
    Зависимости Python: Установите внешнюю библиотеку geopy в окружении Odoo:

    Bash
      pip install geopy
      Применение виджета: В вашем XML-представлении используйте виджет geo_leaflet_map_viewer для поля-плейсхолдера:
    
    XML
      <field name="map_canvas" nolabel="1" widget="geo_leaflet_map_viewer"/>

  
Английский (English)

Odoo Geo Leaflet Map Widget
Short Description: This module provides a customizable field widget for Odoo, enabling users to visually select geographical coordinates on a Leaflet map, set the marker based on entered coordinates, and perform reverse geocoding (getting an address from coordinates) using the Nominatim (OpenStreetMap) service via the geopy library.

Main Features
  1. Interactive Coordinate Selection:
       The user can click on the map to set a marker. The coordinates (map_latitude and map_longitude) are automatically                populated in the Odoo form.

  2. Coordinate Input Visualization:
       Includes a Use entered coordinates button which sets the map marker based on manually entered latitude and longitude             values. This allows users to visually verify the location using coordinates obtained from any external source.

  3. Reverse Geocoding (Backend):
      The Apply address button triggers a server method that uses the selected or entered coordinates to retrieve a full postal        address (street, city, country) and populates the corresponding fields on the form.

- Technical Details
    Odoo Version: 19.0
    Technologies: Leaflet (JS), OWL (JS), Python (geopy)
    License: LGPL-3

- Installation and Usage
    Python Dependencies: Install the external Python library geopy in your Odoo environment:

    Bash
      pip install geopy
      Widget Application: In your XML view, use the geo_leaflet_map_viewer widget on a placeholder field:
    
    XML
      <field name="map_canvas" nolabel="1" widget="geo_leaflet_map_viewer"/>
