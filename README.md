# pyside2-custom-widgets
A PySide2 custom widgets library.

![test](https://github.com/Electronya/pyside2-custom-widgets/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/gh/Electronya/pyside2-custom-widgets/branch/main/graph/badge.svg?token=r1uzdaQ5US)](https://codecov.io/gh/Electronya/pyside2-custom-widgets)

## Usage
Simply copy the desired widget folder in your project and import the base class
and the color class if needed. Also make sure to install PySide2 5..15.2 or newer.

### Demo Apps
A demo apps are provided as code samples. To run them, simply do the following:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python ./src/demoApps/<widget>/demoApp.py
```

### Tests
To run the test, simply do the following:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest
```

## Widgets List
### 1. LedIndicator
- A simple led indicator widget. Base on the [nlamprian](https://github.com/nlamprian) PyQt5 [project](https://github.com/nlamprian/pyqt5-led-indicator-widget).
- [Demo App](src/demoApps/)
