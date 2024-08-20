import unittest
from json_urley import query_str_to_json_obj, json_obj_to_query_str, JsonUrleyError

class TestJsonUrleyAdditional(unittest.TestCase):

    def test_nested_object_with_array(self):
        json_obj = {"user": {"name": "John", "scores": [85, 90, 95]}}
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual(query_str, "user.name=John&user.scores=85&user.scores=90&user.scores=95")
        result = query_str_to_json_obj(query_str)
        self.assertEqual(result, json_obj)

    def test_array_of_objects(self):
        json_obj = {"users": [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]}
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual(query_str, "users~a.n.name=John&users.e.age=30&users.n.name=Jane&users.e.age=25")
        result = query_str_to_json_obj(query_str)
        self.assertEqual(result, json_obj)

    def test_empty_string_values(self):
        json_obj = {"name": "", "description": ""}
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual(query_str, "name=&description=")
        result = query_str_to_json_obj(query_str)
        self.assertEqual(result, json_obj)

    def test_unicode_characters(self):
        json_obj = {"name": "José", "city": "São Paulo"}
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual(query_str, "name=José&city=São%20Paulo")
        result = query_str_to_json_obj(query_str)
        self.assertEqual(result, json_obj)

    def test_deeply_nested_structure(self):
        json_obj = {"a": {"b": {"c": {"d": {"e": [1, 2, 3]}}}}}
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual(query_str, "a.b.c.d.e=1&a.b.c.d.e=2&a.b.c.d.e=3")
        result = query_str_to_json_obj(query_str)
        self.assertEqual(result, json_obj)

    def test_mixed_types_in_array(self):
        json_obj = {"mixed": [1, "two", True, None, 3.14]}
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual(query_str, "mixed=1&mixed=two&mixed=true&mixed=null&mixed=3.14")
        result = query_str_to_json_obj(query_str)
        self.assertEqual(result, json_obj)

    def test_invalid_type_hint(self):
        with self.assertRaises(JsonUrleyError):
            query_str_to_json_obj("key~z=value")

    def test_conflicting_types(self):
        with self.assertRaises(JsonUrleyError):
            query_str_to_json_obj("key=value&key~i=123")

if __name__ == '__main__':
    unittest.main()
