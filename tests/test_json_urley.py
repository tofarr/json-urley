from datetime import datetime
from unittest import TestCase

import tests
from json_urley import query_str_to_json_obj, json_obj_to_query_str, JsonUrleyError


class TestJsonUrley(TestCase):
    def test_empty_params(self):
        json_obj = {}
        query_str = json_obj_to_query_str(json_obj)
        result = query_str_to_json_obj(query_str)
        self.assertEqual(json_obj, result)

    def test_rule_2_str(self):
        query_str = "a~s=b"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"a": "b"}
        self.assertEqual(expected_json_obj, json_obj)
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual("a=b", query_str)

    def test_rule_2_float(self):
        query_str = "a~f=1"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"a": 1.0}
        self.assertEqual(expected_json_obj, json_obj)
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual("a=1.0", query_str)

    def test_rule_2_float_invalid(self):
        query_str = "a~f=a"
        with self.assertRaises(JsonUrleyError):
            query_str_to_json_obj(query_str)

    def test_rule_2_int(self):
        query_str = "a~i=1"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"a": 1}
        self.assertEqual(expected_json_obj, json_obj)
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual("a=1", query_str)

    def test_rule_2_int_invalid(self):
        query_str = "a~i=a"
        with self.assertRaises(JsonUrleyError):
            query_str_to_json_obj(query_str)

    def test_rule_2_bool(self):
        query_str = "a~b=1"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"a": True}
        self.assertEqual(expected_json_obj, json_obj)
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual("a=true", query_str)

    def test_rule_2_null(self):
        query_str = "a~n="
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"a": None}
        self.assertEqual(expected_json_obj, json_obj)
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual("a=null", query_str)
        with self.assertRaises(JsonUrleyError):
            query_str_to_json_obj("a~n=none")

    def test_rule_2_array(self):
        query_str = "a~a="
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"a": []}
        self.assertEqual(expected_json_obj, json_obj)
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual("a~a=", query_str)
        with self.assertRaises(JsonUrleyError):
            query_str_to_json_obj("a~a=1")

    def test_rule_2_obj(self):
        query_str = "a~o="
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"a": {}}
        self.assertEqual(expected_json_obj, json_obj)
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual("a~o=", query_str)
        with self.assertRaises(JsonUrleyError):
            query_str_to_json_obj("a~o=1")

    def test_rule_2_int_unknown(self):
        query_str = "a~x=a"
        with self.assertRaises(JsonUrleyError):
            query_str_to_json_obj(query_str)

    def test_rule_3(self):
        query_str = "a~b=1"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"a": True}
        self.assertEqual(expected_json_obj, json_obj)
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual("a=true", query_str)
        self.assertEqual(expected_json_obj, query_str_to_json_obj(query_str))
        with self.assertRaises(JsonUrleyError):
            query_str_to_json_obj("a~b=2")

    def test_rule_4(self):
        query_str = "a~b=0"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"a": False}
        self.assertEqual(expected_json_obj, json_obj)
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual("a=false", query_str)
        self.assertEqual(expected_json_obj, query_str_to_json_obj(query_str))
        with self.assertRaises(JsonUrleyError):
            query_str_to_json_obj("a~b=flase")

    def test_string_bool_true(self):
        query_str = "a~s=true"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"a": "true"}
        self.assertEqual(expected_json_obj, json_obj)
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual("a~s=true", query_str)

    def test_string_bool_false(self):
        query_str = "a~s=false"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"a": "false"}
        self.assertEqual(expected_json_obj, json_obj)
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual("a~s=false", query_str)

    def test_rule_5(self):
        query_str = "a~n="
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"a": None}
        self.assertEqual(expected_json_obj, json_obj)
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual("a=null", query_str)
        self.assertEqual(expected_json_obj, query_str_to_json_obj(query_str))
        with self.assertRaises(JsonUrleyError):
            query_str_to_json_obj("a~b=None")

    def test_string_null(self):
        query_str = "a~s=null"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"a": "null"}
        self.assertEqual(expected_json_obj, json_obj)
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual("a~s=null", query_str)

    def test_rule_7_infer_null(self):
        query_str = "a=null"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"a": None}
        self.assertEqual(expected_json_obj, json_obj)
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual("a=null", query_str)

    def test_rule_7_infer_true(self):
        query_str = "a=true"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"a": True}
        self.assertEqual(expected_json_obj, json_obj)
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual("a=true", query_str)

    def test_rule_7_infer_false(self):
        query_str = "a=false"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"a": False}
        self.assertEqual(expected_json_obj, json_obj)
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual("a=false", query_str)

    def test_rule_7_infer_int(self):
        query_str = "a=101"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"a": 101}
        self.assertEqual(expected_json_obj, json_obj)
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual("a=101", query_str)

    def test_rule_7_infer_float(self):
        query_str = "a=1.23"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"a": 1.23}
        self.assertEqual(expected_json_obj, json_obj)
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual("a=1.23", query_str)

    def test_string_int(self):
        query_str = "a~s=1"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"a": "1"}
        self.assertEqual(expected_json_obj, json_obj)
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual("a~s=1", query_str)

    def test_string_float(self):
        query_str = "a~s=1.0"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"a": "1.0"}
        self.assertEqual(expected_json_obj, json_obj)
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual("a~s=1.0", query_str)

    def test_string(self):
        query_str = "foo~s=bar"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"foo": "bar"}
        self.assertEqual(expected_json_obj, json_obj)
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual("foo=bar", query_str)
        json_obj = query_str_to_json_obj(query_str)
        self.assertEqual(expected_json_obj, json_obj)

    def test_rule_8(self):
        query_str = "foo=1&foo=2"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"foo": [1, 2]}
        self.assertEqual(expected_json_obj, json_obj)
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual("foo=1&foo=2", query_str)
        json_obj = query_str_to_json_obj(query_str)
        self.assertEqual(expected_json_obj, json_obj)

    def test_rule_8_different_types(self):
        query_str = "foo~b=1&foo~i=2"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"foo": [True, 2]}
        self.assertEqual(expected_json_obj, json_obj)
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual("foo=true&foo=2", query_str)
        json_obj = query_str_to_json_obj(query_str)
        self.assertEqual(expected_json_obj, json_obj)

    def test_rule_9(self):
        query_str = "foo.flag=false&foo.value=2&foo.title=bar"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"foo": {"flag": False, "value": 2, "title": "bar"}}
        self.assertEqual(expected_json_obj, json_obj)
        result = json_obj_to_query_str(json_obj)
        self.assertEqual(query_str, result)

    def test_rule_9_invalid_types(self):
        query_str = "foo.bar~s.zap=1"
        with self.assertRaises(JsonUrleyError):
            query_str_to_json_obj(query_str)

    def test_rule_10_example_1(self):
        query_str = "foo=a&foo=b"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"foo": ["a", "b"]}
        self.assertEqual(expected_json_obj, json_obj)
        result = json_obj_to_query_str(json_obj)
        self.assertEqual(query_str, result)

    def test_rule_10_example_2(self):
        query_str = "foo~a.n=a&foo~a.n=b"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"foo": ["a", "b"]}
        self.assertEqual(expected_json_obj, json_obj)
        query_str = json_obj_to_query_str(json_obj)
        self.assertEqual("foo=a&foo=b", query_str)
        json_obj = query_str_to_json_obj(query_str)
        self.assertEqual(expected_json_obj, json_obj)

    def test_rule_10_example_3(self):
        query_str = "foo~a.n.c=a&foo~a.n.c=b"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"foo": [{"c": "a"}, {"c": "b"}]}
        self.assertEqual(expected_json_obj, json_obj)
        result = json_obj_to_query_str(json_obj)
        expected_query_str = "foo~a.n.c=a&foo.n.c=b"
        self.assertEqual(expected_query_str, result)
        self.assertEqual(expected_json_obj, query_str_to_json_obj(result))

    def test_rule_10_example_4(self):
        query_str = "foo~a=&foo.n.c=a&foo.n.c=b"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"foo": [{"c": "a"}, {"c": "b"}]}
        self.assertEqual(expected_json_obj, json_obj)
        result = json_obj_to_query_str(json_obj)
        expected_query_str = "foo~a.n.c=a&foo.n.c=b"
        self.assertEqual(expected_query_str, result)

    def test_rule_10_example_5(self):
        query_str = "foo~a.n.c=a&foo.e.d=b"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"foo": [{"c": "a", "d": "b"}]}
        self.assertEqual(expected_json_obj, json_obj)
        result = json_obj_to_query_str(json_obj)
        self.assertEqual(query_str, result)

    def test_rule_10_example_6(self):
        query_str = "foo~a.e.c=a&foo.e.d=b"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"foo": [{"c": "a", "d": "b"}]}
        self.assertEqual(expected_json_obj, json_obj)
        result = json_obj_to_query_str(json_obj)
        expected_result = "foo~a.n.c=a&foo.e.d=b"
        self.assertEqual(expected_result, result)

    def test_rule_10_example_7(self):
        query_str = "foo~a.e.c=a&foo.e.c=b"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"foo": [{"c": ["a", "b"]}]}
        self.assertEqual(expected_json_obj, json_obj)
        result = json_obj_to_query_str(json_obj)
        expected_result = "foo~a.n.c=a&foo.e.c=b"
        self.assertEqual(expected_result, result)

    def test_rule_10_example_8(self):
        query_str = "foo~a.e~a.e~a.e=1"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"foo": [[[1]]]}
        self.assertEqual(expected_json_obj, json_obj)
        result = json_obj_to_query_str(json_obj)
        expected_result = "foo~a.n~a.n~a.n=1"
        self.assertEqual(expected_result, result)

    def test_rule_10_example_9(self):
        query_str = "foo~a.n~a.n~a.n=1&foo~a.n~a.n~a.n=2&foo~a.e~a.e~a.e=3"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"foo": [[[1]], [[2, 3]]]}
        self.assertEqual(expected_json_obj, json_obj)
        result = json_obj_to_query_str(json_obj)
        expected_result = "foo~a.n~a.n~a.n=1&foo.n~a.n~a.n=2&foo.e.e.n=3"
        self.assertEqual(expected_result, result)
        json_obj_2 = query_str_to_json_obj(result)
        self.assertEqual(expected_json_obj, json_obj_2)

    def test_rule_11_example_1(self):
        query_str = "a~a=&a.b=1"
        with self.assertRaises(JsonUrleyError):
            query_str_to_json_obj(query_str)

    def test_rule_11_example_2(self):
        query_str = "a~a=&a.foo=1"
        with self.assertRaises(JsonUrleyError):
            query_str_to_json_obj(query_str)

    def test_rule_12_example_1(self):
        query_str = "a~~a=1"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"a~a": 1}
        self.assertEqual(expected_json_obj, json_obj)
        result = json_obj_to_query_str(json_obj)
        self.assertEqual(query_str, result)

    def test_rule_12_example_2(self):
        query_str = "a~~~b=1"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"a~": True}
        self.assertEqual(expected_json_obj, json_obj)
        result = json_obj_to_query_str(json_obj)
        expected_result = "a~~=true"
        self.assertEqual(expected_result, result)
        self.assertEqual(expected_json_obj, query_str_to_json_obj(result))

    def test_rule_12_example_3(self):
        query_str = "a~~~.b=1"
        json_obj = query_str_to_json_obj(query_str)
        expected_json_obj = {"a~.b": 1}
        self.assertEqual(expected_json_obj, json_obj)
        result = json_obj_to_query_str(json_obj)
        self.assertEqual(query_str, result)

    def test_non_json(self):
        with self.assertRaises(JsonUrleyError):
            json_obj_to_query_str({"foo": datetime.now()})

    def test_geometry(self):
        json_obj = {
            "name": "geometry",
            "points": [[1, 2], [3, 4]],
            "linestring": [1, 2, 3, 4],
        }
        query_str = json_obj_to_query_str(json_obj)
        expected_query_str = (
            "name=geometry"
            "&points~a.n~a.n=1&points.e.n=2&points.n~a.n=3&points.e.n=4"
            "&linestring=1&linestring=2&linestring=3&linestring=4"
        )
        self.assertEqual(expected_query_str, query_str)
        result = json_obj_to_query_str(json_obj)
        self.assertEqual(query_str, result)
        resulting_json_obj = query_str_to_json_obj(result)
        self.assertEqual(json_obj, resulting_json_obj)

    def test_error_path_1(self):
        query_str = "foo~a.b.c=1"
        with self.assertRaises(JsonUrleyError):
            query_str_to_json_obj(query_str)

    def test_error_path_2(self):
        query_str = "value=1&value.child=2"
        with self.assertRaises(JsonUrleyError):
            query_str_to_json_obj(query_str)

    def test_error_path_3(self):
        query_str = "value=1&value.child.grandchild=2"
        with self.assertRaises(JsonUrleyError):
            query_str_to_json_obj(query_str)
