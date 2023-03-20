from api import PetFriends
from settings import valid_email, valid_password, not_valid_email, not_valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    print(status)
    print(result)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскинs', animal_type='двортерьерs',
                                     age='4s', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_Add_photo_of_pet(pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить фото с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    print(pet_id)

    # Добавляем питомца
    status, result = pf.Add_photo_of_pet(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200


def test_Add_information_about_new_pet_without_photo(name='name', animal_type="Сиамская", age='5'):
    """Проверяем что можно добавить питомца с корректными данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.Add_information_about_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

def test_negative_Add_information_about_new_pet_without_photo_for_null_in_animal_type(name='namek', animal_type='', age = '5'):
    """Проверяем что можно добавить питомца с корректными данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.Add_information_about_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

def test_negative_Add_information_about_new_pet_without_photo_for_null_in_name(name='', animal_type='Сиамская', age = '5'):
    """Проверяем что можно добавить питомца с корректными данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.Add_information_about_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


def test_get_api_key_for_not_valid_user(email=not_valid_email, password=not_valid_password):
    """ Проверяем что запрос api ключа возвращает статус 403"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403

def test_get_all_pets_with_not_valid_key(filter=''):
    """Подменяем ключ не существующим и проверяем сможем ли получить список всех
    питомцев без авторизации"""
    auth_key1 = {'key': 'dbdda166376746c2400d072f4f23005eb4e96efd4bf8aa1gb0db09b5'}
    status, result = pf.get_list_of_pets(auth_key1, filter)

    assert status == 403
    print(status)


def test_get_my_pets_with_valid_key(filter='my_pets'):
    """ Проверяем что запрос моих питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список моих питомцев и проверяем что список не пустой."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_successful_delete_self_pet_not_valid_pet_id():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    id ={'id': 'e2be44ad-c0aa-4c45-8d50-376753950426'}
    # Берём id выдуманного питомца и отправляем запрос на удаление
    pet_id = id['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()
    #По итогу мы получили код 200 за удаление не существующего питомца я думаю это не критичный баг.

def test_negative_Add_photo_of_pet(pet_photo='images/name.csv'):
    """Проверяем что можно добавить файл с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']

    # Добавляем питомца
    status, result = pf.Add_photo_of_pet(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 500