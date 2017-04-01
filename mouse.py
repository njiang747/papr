from AppKit import NSScreen
from Quartz.CoreGraphics import CGEventCreateMouseEvent
from Quartz.CoreGraphics import CGEventPost
from Quartz.CoreGraphics import kCGEventMouseMoved
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseUp
from Quartz.CoreGraphics import kCGMouseButtonLeft
from Quartz.CoreGraphics import kCGHIDEventTap

def screensize():
    w = NSScreen.mainScreen().frame().size.width
    h = NSScreen.mainScreen().frame().size.height
    return (w,h)

def mouseEvent(type, posx, posy):
        theEvent = CGEventCreateMouseEvent(
                    None,
                    type,
                    (posx,posy),
                    kCGMouseButtonLeft)
        CGEventPost(kCGHIDEventTap, theEvent)

def mousemove(posx,posy):
        mouseEvent(kCGEventMouseMoved, posx,posy)

def mouseclick(posx,posy):
        # mouseEvent(kCGEventMouseMoved, posx,posy);
        mouseEvent(kCGEventLeftMouseDown, posx,posy)
        mouseEvent(kCGEventLeftMouseUp, posx,posy)

# mousemove(100,130)
# mouseclick(100,130)
# mouseclick(100,130)