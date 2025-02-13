import pytest
from ossobuco.geometries import *

# List of classes to test
geometries = [
    Keil,
    Flat,
    Sphere,
    Parabola,
    Sinusoidal,
    RandomSurf,
    Fish
]

@pytest.mark.parametrize("geometry", geometries)
def test_geometry_instantiation(geometry):
    """
    Test that each geometry class can be instantiated without errors.
    """
    # Try to create an object of the geometry class
    try:
        geometry_instance = geometry()
    except Exception as e:
        pytest.fail(f"Failed to instantiate {geometry.__name__}: {e}")
    
    # If object creation succeeded, we can assert certain properties (optional)
    assert geometry_instance is not None, f"{geometry.__name__} instance is None"
    
    # Add more assertions here if necessary (e.g., check defaults, parameters, etc.)

