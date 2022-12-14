import unittest
import valve
from unittest.mock import MagicMock
from unittest.mock import patch
import math
import time

FULLTURNTIME = 120


class TestValveClass(unittest.TestCase):

    def test_defaultposition(self):
        v = valve.Valve()
        self.assertEqual(v.current_position, 10)

    def test_defaultdirection(self):
        currtime = math.trunc(time.time() * 1000)
        v = valve.Valve()
        v.update(currtime)
        self.assertEqual(False, v.Relay_State1)
        self.assertEqual(False, v.Relay_State2)
        self.assertEqual("STOP", v.direction)

    def test_colder_direction(self):
        currtime = math.trunc(time.time() * 1000)
        v = valve.Valve()
        v.switchRelay1On()
        v.update(currtime)
        self.assertEqual(True, v.Relay_State1)
        self.assertEqual(False, v.Relay_State2)
        self.assertEqual("COLDER", v.direction)

    def test_hotter_direction(self):
        currtime = math.trunc(time.time() * 1000)
        v = valve.Valve()
        v.switchRelay2On()
        v.update(currtime)
        self.assertEqual(False, v.Relay_State1)
        self.assertEqual(True, v.Relay_State2)
        self.assertEqual("HOTTER", v.direction)

    def test_invalid_direction(self):
        currtime = math.trunc(time.time() * 1000)
        v = valve.Valve()
        v.switchRelay1On()
        v.switchRelay2On()
        v.update(currtime)
        self.assertEqual(True, v.Relay_State1)
        self.assertEqual(True, v.Relay_State2)
        self.assertEqual("INVALID", v.direction)

    def test_position_hotterfullturn(self):
        currtime = math.trunc(time.time() * 1000)
        nexttime = currtime + FULLTURNTIME * 1000
        v = valve.Valve()
        v.current_position = 0
        v.update(currtime)
        v.switchRelay2On()
        v.update(nexttime)
        self.assertEqual(90, v.current_position)

    def test_position_hotterupperbound(self):
        currtime = math.trunc(time.time() * 1000)
        nexttime = currtime + (FULLTURNTIME + 30) * 1000
        v = valve.Valve()
        v.current_position = 0
        v.update(currtime)
        v.switchRelay2On()
        v.update(nexttime)
        self.assertEqual(90, v.current_position)

    def test_position_hottertensecs(self):
        currtime = math.trunc(time.time() * 1000)
        nexttime = currtime + 10 * 1000
        v = valve.Valve()
        v.current_position = 0
        v.update(currtime)
        v.switchRelay2On()
        v.update(nexttime)
        self.assertEqual(7.5, v.current_position)

    def test_position_colderfullturn(self):
        currtime = math.trunc(time.time() * 1000)
        nexttime = currtime + FULLTURNTIME * 1000
        v = valve.Valve()
        v.current_position = 90
        v.update(currtime)
        v.switchRelay1On()
        v.update(nexttime)
        self.assertEqual(0, v.current_position)

    def test_position_colderlowerbound(self):
        currtime = math.trunc(time.time() * 1000)
        nexttime = currtime + (FULLTURNTIME + 30) * 1000
        v = valve.Valve()
        v.current_position = 90
        v.update(currtime)
        v.switchRelay1On()
        v.update(nexttime)
        self.assertEqual(0, v.current_position)

    def test_position_coldertensecs(self):
        currtime = math.trunc(time.time() * 1000)
        nexttime = currtime + 20 * 1000
        v = valve.Valve()
        v.current_position = 90
        v.update(currtime)
        v.switchRelay1On()
        v.update(nexttime)
        self.assertEqual(75, v.current_position)
