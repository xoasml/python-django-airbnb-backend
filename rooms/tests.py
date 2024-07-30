from rest_framework.test import APITestCase
from . import models


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
