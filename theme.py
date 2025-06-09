APP_STYLE = """
QWidget {
    background-color: qlineargradient(
        spread:pad,
        x1:0, y1:0,
        x2:1, y2:1,
        stop:0 #000000,
        stop:1 #1e1e1e
    );
    color: white;
    font-family: 'Segoe UI';
}

QPushButton {
    background-color: #f0f0f0;
    color: black;
    border: none;
    padding: 10px;
    border-radius: 8px;
    font-size: 14px;
}

QPushButton:hover {
    background-color: #ffffff;
}

QPushButton:pressed {
    background-color: #dddddd;
}
"""
