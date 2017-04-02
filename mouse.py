from AppKit import NSScreen
from Quartz.CoreGraphics import CGEventCreateMouseEvent
from Quartz.CoreGraphics import CGEventCreateScrollWheelEvent
from Quartz.CoreGraphics import CGEventPost
from Quartz.CoreGraphics import kCGEventMouseMoved
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseUp
from Quartz.CoreGraphics import kCGEventLeftMouseDragged
from Quartz.CoreGraphics import kCGMouseButtonLeft
from Quartz.CoreGraphics import kCGHIDEventTap
import time

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

def mousedown(posx,posy):
    mouseEvent(kCGEventLeftMouseDown, posx,posy)

def mouseup(posx,posy):
    mouseEvent(kCGEventLeftMouseUp, posx,posy)

def mouseclick(posx,posy):
    mouseEvent(kCGEventLeftMouseDown, posx, posy)
    mouseEvent(kCGEventLeftMouseUp, posx, posy)

def mousedrag(posx,posy):
    drag = CGEventCreateMouseEvent(None, kCGEventLeftMouseDragged, (posx, posy), 0)
    CGEventPost(kCGHIDEventTap, drag)

def scrolldown(speed):
    scroll = CGEventCreateScrollWheelEvent(None, 0, 1, -speed)
    CGEventPost(kCGHIDEventTap, scroll)

def scrollup(speed):
    scroll = CGEventCreateScrollWheelEvent(None, 0, 1, speed)
    CGEventPost(kCGHIDEventTap, scroll)
