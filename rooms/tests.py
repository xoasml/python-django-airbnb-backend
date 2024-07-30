from rest_framework.test import APITestCase
from . import models
from users.models import User


class TestAmenities(APITestCase):

    NAME = "Amenity Test"
    DESC = "Amenity Desc"

    URL = "/api/v1/rooms/amenities/"

    # Test DB 세팅 : 아래 Test Code 가 실행 되기 전 Test DB 세팅
    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    # Test Code amenities put
    def test_all_amenities(self):

        # API 에 요청
        response = self.client.get(self.URL)
        data = response.json()

        # 응답 코드 200 확인
        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )

        # 응답 데이터 리스트 타입인지 확인
        self.assertIsInstance(
            data,
            list,
            "response data is not list",
        )

        # 응답 데이터 리스트 랭스 확인
        self.assertEqual(
            len(data),
            1,
        )

        # 응답 데이터 name 컬럼 확인
        self.assertEqual(
            data[0]["name"],
            self.NAME,
        )

        # 응답 데이터 description 컬럼 확인
        self.assertEqual(
            data[0]["description"],
            self.DESC,
        )

    # Test Code amenities post
    def test_create_amenity(self):

        new_amenity_name = "New Amenity"
        new_amenity_desc = "New Amenity desc"

        # API 요청 200 의도
        response = self.client.post(
            self.URL,
            data={
                "name": new_amenity_name,
                "description": new_amenity_desc,
            },
        )
        data = response.json()

        # 응답 코드 200 확인
        self.assertEqual(
            response.status_code,
            200,
            "Not 200 status code",
        )

        # insert data와 요청 data 비교 : 동일한 data 기대
        self.assertEqual(
            data["name"],
            new_amenity_name,
        )
        # insert data와 요청 data 비교 : 동일한 data 기대
        self.assertEqual(
            data["description"],
            new_amenity_desc,
        )

        # API 요청 400 의도 : data 추가 하지 않았음
        response = self.client.post(self.URL)
        data = response.json()

        # 응답 코드 400 확인
        self.assertEqual(
            response.status_code,
            400,
        )

        # name field 존재 확인
        self.assertIn("name", data)


class TestAmenity(APITestCase):

    NAME = "TEST Amenity"
    DESC = "TEST Desc"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_get_amenity_not_found(self):
        response = self.client.get("/api/v1/rooms/amenities/2/")

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_get_amenity(self):
        response = self.client.get("/api/v1/rooms/amenities/1/")
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertEqual(
            data["name"],
            self.NAME,
        )
        self.assertEqual(
            data["description"],
            self.DESC,
        )

    def test_put_amenity(self):

        change_name = "Change Name"
        change_desc = "Change Desc"

        response = self.client.put(
            "/api/v1/rooms/amenities/1/",
            data={
                "name": change_name,
                "description": change_desc,
            },
        )
        data = response.json()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            data["name"],
            change_name,
        )

        self.assertEqual(
            data["description"],
            change_desc,
        )

        response = self.client.put(
            "/api/v1/rooms/amenities/1/",
            data={
                "name": "",
                "description": change_desc,
            },
        )

        self.assertEqual(response.status_code, 400)

        response = self.client.put(
            "/api/v1/rooms/amenities/1/",
            data={
                "name": "1123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890"
            },
        )

        self.assertEqual(response.status_code, 400, "max_len 보다 큰 값")

    def test_delete_amenity(self):
        response = self.client.delete("/api/v1/rooms/amenities/1/")
        self.assertEqual(response.status_code, 204)


class TestRoom(APITestCase):

    def setUp(self):
        # 테스트 유저 아이디 생성
        user = User.objects.create(
            username="test",
        )
        user.set_password("123")
        user.save()
        self.user = user

    def test_create_room(self):

        # 로그인 하지 않고 호출 테스트
        response = self.client.post("/api/v1/rooms/")

        self.assertEqual(response.status_code, 403)

        # 로그인
        self.client.force_login(self.user)

        # 로그인 하고 테스트
        response = self.client.post("/api/v1/rooms/")
        print(response.json())
