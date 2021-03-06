from src.dataGenerators.PetDataGenerator import PetDataGenerator
from test.pet.BasePet import BasePet
import pytest
@pytest.mark.addPet
class PostPetTests(BasePet):

    def test_addPet(self):
        payloadJson = PetDataGenerator().getNewPet()
        
        response = self.client.post(self.path, payloadJson).assertStatus(200).getJson()
        self.commonAssertions.compareDictionaries(payloadJson, response)
