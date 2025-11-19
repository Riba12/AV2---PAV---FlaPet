from src.repositories.AnimalRepository import delete_animal, update_animal, add_animal, get_all_animais, get_animal_by_id

def getAllAnimais():
    return get_all_animais()

def getAnimal(animal_id):
    return get_animal_by_id(animal_id)