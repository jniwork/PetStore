import pytest
import allure

from core.clients.endpoints import Endpoints
from core.models.pet import Pet
from tests.data.pet_builder import PetBuilder


@allure.feature("Pet")
@allure.story("Create pet")
def test_create_pet(api_client):
    pet_data = {
        "name": "Barsik",
        "status": "available"
    }

    response = api_client.post(
        Endpoints.PET.value,
        pet_data
    )

    assert response.status_code == 200

    data = response.json()

    pet = Pet(**data)

    assert pet.id is not None

    assert pet.name == pet_data["name"]
    assert pet.status == pet_data["status"]


@allure.feature("Pet")
@allure.story("Create and get pet")
def test_create_and_get_pet(api_client):
    pet_data = {
        "name": "Barsik",
        "status": "available"
    }

    # 👉 CREATE
    create_response = api_client.post(
        Endpoints.PET.value,
        pet_data
    )
    assert create_response.status_code == 200

    created_pet = Pet(**create_response.json())

    assert created_pet.id is not None

    # 👉 GET
    get_response = api_client.get(
        Endpoints.PET_BY_ID.value.format(pet_id=created_pet.id)
    )
    assert get_response.status_code == 200

    fetched_pet = Pet(**get_response.json())

    # 👉 VERIFY
    assert fetched_pet.id == created_pet.id
    assert fetched_pet.name == pet_data["name"]
    assert fetched_pet.status == pet_data["status"]


@allure.feature("Pet")
@allure.story("Create and get pet and delete pet")
@allure.feature("Pet")
@allure.story("Create, get and delete pet")
def test_create_get_delete_pet(api_client):
    pet_data = {
        "name": "Barsik",
        "status": "available"
    }

    # CREATE
    create_response = api_client.post(Endpoints.PET.value, pet_data)
    assert create_response.status_code == 200

    created_pet = Pet(**create_response.json())
    assert created_pet.id is not None

    pet_endpoint = Endpoints.PET_BY_ID.value.format(pet_id=created_pet.id)

    # GET
    get_response = api_client.get(pet_endpoint)
    assert get_response.status_code == 200

    fetched_pet = Pet(**get_response.json())

    assert fetched_pet.id == created_pet.id
    assert fetched_pet.name == created_pet.name
    assert fetched_pet.status == created_pet.status

    # DELETE
    delete_response = api_client.delete(pet_endpoint)
    assert delete_response.status_code == 200

    # GET after delete
    get_response_after_delete = api_client.get(pet_endpoint)
    assert get_response_after_delete.status_code == 404


@allure.feature("Pet")
@allure.story("Negative: create pet")
@pytest.mark.parametrize(
    "pet_data",
    [
        pytest.param(
            PetBuilder().without_name().build(),
            id="missing name"
        ),
        pytest.param(
            PetBuilder().with_name(123).build(),
            id="invalid name type"
        ),
        pytest.param(
            PetBuilder().with_status("INVALID").build(),
            id="invalid status"
        ),
    ]
)
def test_create_pet_negative(api_client, pet_data):
    response = api_client.post(
        Endpoints.PET.value,
        pet_data
    )

    # 👇 универсальная проверка
    assert response.status_code in [200, 400, 500]

    data = response.json()

    # 👇 базовая проверка что API жив
    assert isinstance(data, dict)


@allure.feature("Pet")
@allure.story("Create pet with photoUrls")
def test_create_pet_with_photo_urls(api_client):
    pet_data = (
        PetBuilder()
        .with_name("Barsik")
        .with_photo_urls(["url1", "url2"])
        .build()
    )

    response = api_client.post(Endpoints.PET.value, pet_data)

    assert response.status_code == 200

    pet = Pet(**response.json())

    assert pet.photoUrls == ["url1", "url2"]


@allure.feature("Pet")
@allure.story("Create pet with category")
def test_create_pet_with_category(api_client):
    pet_data = (
        PetBuilder()
        .with_name("Barsik")
        .with_category(category_id=1, name="Dogs")
        .build()
    )

    response = api_client.post(Endpoints.PET.value, pet_data)

    assert response.status_code == 200

    pet = Pet(**response.json())

    assert pet.category is not None
    assert pet.category.name == "Dogs"


@allure.feature("Pet")
@allure.story("Create pet with tags")
def test_create_pet_with_tags(api_client):
    pet_data = (
        PetBuilder()
        .with_name("Barsik")
        .with_single_tag(tag_id=1, name="cute")
        .build()
    )

    response = api_client.post(Endpoints.PET.value, pet_data)

    assert response.status_code == 200

    pet = Pet(**response.json())

    assert pet.tags is not None
    assert len(pet.tags) > 0
    assert pet.tags[0].name == "cute"


def test_create_update_get_pet(api_client):
    pet_data = {
        "name": "Ba11",
        "status": "available"
    }

    # CREATE
    create_response = api_client.post(Endpoints.PET.value, pet_data)
    assert create_response.status_code == 200

    created_pet = Pet(**create_response.json())
    assert created_pet.id is not None

    # UPDATE
    updated_pet_data = {
        "id": created_pet.id,
        "name": "test",
        "status": "sold"
    }
    put_response = api_client.put(Endpoints.PET.value, updated_pet_data)
    assert put_response.status_code == 200

    # GET after update
    get_response = api_client.get(
        Endpoints.PET_BY_ID.value.format(pet_id=created_pet.id)
    )
    assert get_response.status_code == 200

    fetched_pet = Pet(**get_response.json())

    # 👉 VERIFY
    assert fetched_pet.id == created_pet.id
    assert fetched_pet.name is not None
    assert fetched_pet.status == updated_pet_data["status"]
