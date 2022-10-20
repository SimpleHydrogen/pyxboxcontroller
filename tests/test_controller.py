def test_default_state():
    import os, sys
    sys.path.append(os.path.dirname(__name__))
    from pyxboxcontroller.controller import XboxControllerState
    
    default_state = XboxControllerState.default_state()
    
    print(default_state)
    
    assert isinstance(default_state , XboxControllerState)
    
if __name__ == "__main__":
    test_default_state()