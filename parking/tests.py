from django.test import TestCase
from parking.models import Floor, ParkingSlot

# Create your tests here.
#SQL Lite doesnt care about length https://sqlite.org/faq.html#q9
#MySQL or Postgresql would work
class FloorTestCase(TestCase):
    """Create floor object"""
    def create_floor(self, floor_number="2A"):
        return Floor.objects.create(floor_number=floor_number)
    """Test floor model"""
    def test_create_floor(self):
        testFloor = self.create_floor()
        self.assertTrue(isinstance(testFloor, Floor))
        self.assertEqual(testFloor.__str__(), testFloor.floor_number)

class ParkingSlotTestCase(TestCase):
    def create_parkingslot(self):
        #Create test object
        floor = Floor(floor_number="2A")
        floor.save()
        slot = ParkingSlot(slot_number="11")
        slot.save()
        #Test if ParkingSlot model foreignkey is linked to Floor model
        test_parking = ParkingSlot.objects.get(id=1)
        self.assertEqual(test_parking.floor.floor_number, "2A")