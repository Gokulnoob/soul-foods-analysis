import dash
from dash.testing.application_runners import import_app
from dash.testing.browser import Browser
import pytest
import time

# Test fixture with 5 second timeout
@pytest.fixture
def app():
    app = import_app("app")
    app.config.suppress_callback_exceptions = True
    return app

# Utility function to wait for elements
def wait_for_element(dash_duo, selector, timeout=5):
    for _ in range(timeout * 10):
        if dash_duo.find_elements(selector):
            return True
        time.sleep(0.1)
    return False

# Test 1: Verify header exists with correct text
def test_header_present(dash_duo, app):
    dash_duo.start_server(app)
    
    # Wait for header to load
    assert wait_for_element(dash_duo, "h1"), "Header not found"
    
    header = dash_duo.find_element("h1")
    assert header.text == "Soul Foods Pink Morsel Sales Dashboard", \
        f"Header text mismatch. Expected 'Soul Foods...', got '{header.text}'"

# Test 2: Verify visualization exists and renders data
def test_visualization_present(dash_duo, app):
    dash_duo.start_server(app)
    
    # Wait for chart to load
    assert wait_for_element(dash_duo, "#sales-chart"), "Chart not found"
    
    # Verify chart has traces (data lines)
    dash_duo.wait_for_element("#sales-chart .js-plotly-plot", timeout=5)
    assert len(dash_duo.find_elements("#sales-chart .js-plotly-plot .trace")) > 0, \
        "Chart is not rendering any data"

# Test 3: Verify region picker exists with all options
def test_region_picker_present(dash_duo, app):
    dash_duo.start_server(app)
    
    # Wait for radio items to load
    assert wait_for_element(dash_duo, "#region-radio"), "Region picker not found"
    
    # Verify all options exist
    options = dash_duo.find_elements("#region-radio input[type='radio']")
    assert len(options) == 5, f"Expected 5 radio options, found {len(options)}"
    
    # Verify option labels
    expected_labels = ["All Regions", "North", "East", "South", "West"]
    actual_labels = [el.text for el in dash_duo.find_elements("#region-radio label")]
    
    for expected in expected_labels:
        assert expected in actual_labels, f"Missing option: {expected}"

# Test 4: Verify region filtering works
def test_region_filter_functionality(dash_duo, app):
    dash_duo.start_server(app)
    
    # Click North region option
    dash_duo.find_element("#region-radio input[value='north']").click()
    
    # Wait for chart update
    time.sleep(2)  # Allow time for callback
    
    # Verify only North data is shown (assuming your app filters properly)
    traces = dash_duo.find_elements("#sales-chart .js-plotly-plot .trace")
    assert len(traces) == 1, "Filtering not working - should show only one region"