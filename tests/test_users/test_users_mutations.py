import shutil
from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from factories import UserFactory, faker
from users.models import User


def test_create_user_with_image(file_client):
    mutation = """mutation createNewUser($image: Upload!){
          createUser(input: {
            email:"ramzi@admin.com",
            username: "ramziTest",
            password:"1234",
            confirmPassword: "1234",
            image: $image
          }){
            success,
            user{
              id
            }
          }
        }
    """
    with open("../fixtures/img.png", "rb") as img:
        image = SimpleUploadedFile(
            name="image.png", content_type="image/png", content=img.read()
        )
    response = file_client.query(
        mutation,
        op_name="createNewUser",
        files={"image": image},
    )
    assert response.status_code == 200
    data = response.json()["data"]
    content = data["createUser"]
    assert content["success"] is True
    images_path = Path("./images")
    if images_path.exists():
        shutil.rmtree(images_path)


def test_create_user_passwords_mismatch(client):
    mutation = """mutation createUserPasswordsMismatch {
                 createUser(input: {
                   email:"ramzi@admin.com",
                   username: "ramziTest",
                   password:"1234",
                   confirmPassword: "12345"
                 }){
                   success
                 }
             }
           """
    data = client.query(mutation, op_name="createUserPasswordsMismatch").json()
    assert data["errors"][0]["message"] == "password and confirm_password must match"


def test_update_existing_user(client):
    user = UserFactory()
    email = "test@admin.com"
    username = "test user"
    update_mutation = """mutation updateExistingUser($email: String!, $username: String!) {
                          updateUser(input: { email: $email, username: $username }) {
                            success
                            user {
                              email
                              username
                            }
                          }
                        }
                    """
    response = client.authenticated_query(
        user,
        update_mutation,
        op_name="updateExistingUser",
        variables={"email": email, "username": username},
    )
    data = response.json()["data"]["updateUser"]
    assert data["success"] is True
    assert data["user"]["email"] == email
    assert data["user"]["username"] == username
    updated_user = User.objects.get(id=user.id)
    assert updated_user.email == email
    assert updated_user.username == username


def test_user1_follows_user2(client):
    user1 = UserFactory()
    user2 = UserFactory(email=faker.email(), username=faker.name())
    follow_mutation = """mutation followProfile($username: String!){
                          followProfile(input: {username:$username}){
                            success
                          }
                        } 
                    """
    response = client.authenticated_query(
        user1, follow_mutation, variables={"username": user2.username}
    )
    data = response.json()["data"]["followProfile"]
    assert data["success"] is True
