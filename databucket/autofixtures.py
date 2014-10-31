'''
Created on Oct 25, 2014

@author: lauril
'''
import autofixture

from databucket.models import Firestorm, ObservedDevice,FirestormReading
import databucket



from datetime import datetime
from django.utils import timezone
from autofixture import AutoFixture
from autofixture import generators, register
import random

class CompanyGenerator(generators.Generator):
    all = [
        'Ericsson', 'Nike', 'Fitbit', 'Google', 'Motorola', 'Intel', 'Misubishi',
        'Samsung', 'Apple']
    def __init__(self):
        pass

    def generate(self):
        return random.choice(self.all)
 
class FirestormGenerator(generators.Generator):
    fires = []
    def __init__(self):
        self.fires = Firestorm.objects.all()

    def generate(self):
        return random.choice(self.fires)   

class MACGenerator(generators.Generator):
    prefix = ''
    length = 0
    def __init__(self, lenght=4,prefix = '0x'):
        self.length = lenght
        self.prefix = prefix

    def generate(self):
        ret = self.prefix
        for b in [random.randint(0,255) for r in xrange(self.length)]:
            ret+="%X" % b
            
        return ret 
        
class FirestormAutoFixture(AutoFixture):
    field_values = {
        'local_mac': MACGenerator(),
    }

autofixture.register(Firestorm, FirestormAutoFixture)

class ObservedDeviceAutoFixture(AutoFixture):
    field_values = { 'observer':FirestormGenerator(),
                    'observedMAC': MACGenerator() , 
                    'manufactorer': CompanyGenerator()}

autofixture.register(ObservedDevice, ObservedDeviceAutoFixture)

class FirestormReadingDeviceAutoFixture(AutoFixture):
    field_values = {'firestorm':FirestormGenerator(),
                    'acc_X':generators.IntegerGenerator(min_value=-12000, max_value=12000), 
                    'acc_Y':generators.IntegerGenerator(min_value=-12000, max_value=12000),
                    'acc_Z':generators.IntegerGenerator(min_value=-12000, max_value=12000),
                    'mag_X':generators.IntegerGenerator(min_value=-12000, max_value=12000),
                    'mag_Y':generators.IntegerGenerator(min_value=-12000, max_value=12000),
                    'mag_Z':generators.IntegerGenerator(min_value=-12000, max_value=12000),
                    'light':generators.IntegerGenerator(min_value=700, max_value=1000)
    }

autofixture.register(FirestormReading, FirestormReadingDeviceAutoFixture)
# obsfixture = AutoFixture(ObservedDevice, generate_fk=True)
# observations = autofixture.create(obsfixture, 100)
# firefixture = AutoFixture(FirestormReading, generate_fk=True)
# firestorms = autofixture.create(firefixture, 100)

