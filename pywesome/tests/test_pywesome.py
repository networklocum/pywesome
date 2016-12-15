from pywesome import pywesome as _
from pywesome.collection import Pywesome
import unittest
import json
from collections import namedtuple
import copy


class TestCollectutilsMethods(unittest.TestCase):

    def test_map(self):
        col = [1, 2, 3, 4]
        mapped_col = _.map(col, lambda n: n + 1)
        self.assertEqual(mapped_col, [2, 3, 4, 5])

        col = [{'id': 1, 'name': 'Name'}, {'id': 2, 'name': 'Name'}]
        mapped_col = _.map(col, lambda o: o['id'])
        self.assertEqual(mapped_col, [1, 2])

    def test_reduce(self):
        col = [1, 2, 3, 4]
        self.assertEqual(_.reduce(col, lambda t, n: t + n), 10)

        # Test with a function
        def concat(a, b):
            return a + b
        col = ['a', 'b', 'c', 'd', 'e']
        self.assertEqual(_.reduce(col, concat, 'z'), 'zabcde')

        # Test with more complex operations
        def json_merge(json_list, obj):
            d = json.loads(json_list)
            d.append(obj)
            return json.dumps(d)

        col = [{'id': 1, 'name': 'Name'}, {'id': 2, 'name': 'Name'}, {'id': 3, 'name': 'Name'}]
        self.assertEqual(
            json.loads(_.reduce(col, json_merge, json.dumps([]))),
            json.loads(json.dumps(col))
        )

        col = [1]
        self.assertEqual(_.reduce(col, lambda t, n: t + n), 1)

    def test_filter(self):
        col = [1, 2, 3, 4]
        filtered_col = _.filter(col, lambda n: n < 3)
        self.assertEqual(filtered_col, [1, 2])

        col = [{'id': 1, 'name': 'Name'}, {'id': 2, 'name': 'Name', 'prop': 'value'}]
        filtered_col = _.filter(col, lambda o: 'prop' in o)
        self.assertEqual(filtered_col, [{'id': 2, 'name': 'Name', 'prop': 'value'}])

    def test_reject(self):
        col = [1, 2, 3, 4]
        filtered_col = _.reject(col, lambda n: n < 3)
        self.assertEqual(filtered_col, [3, 4])

        col = [{'id': 1, 'name': 'Name'}, {'id': 2, 'name': 'Name', 'prop': 'value'}]
        filtered_col = _.reject(col, lambda o: 'prop' in o)
        self.assertEqual(filtered_col, [{'id': 1, 'name': 'Name'}])

    def test_contains(self):
        col = [1, 2, 3, 4]
        self.assertTrue(_.contains(col, 2))
        self.assertFalse(_.contains(col, 8))

        col = [{'id': 1, 'name': 'Name'}, {'id': 2, 'name': 'Name', 'prop': 'value'}]
        self.assertTrue(_.contains(col, lambda o: 'prop' in o))
        self.assertFalse(_.contains(col, lambda o: 'noprop' in o))

    def test_search(self):
        col = [1, 2, 3, 4]
        self.assertEqual(_.search(col, 3), 2)
        self.assertEqual(_.search(col, lambda n: n > 2), 2)
        self.assertEqual(_.search(col, 8), False)

        col = [{'id': 1, 'name': 'Name'}, {'id': 2, 'name': 'Name', 'prop': 'value'}]
        self.assertEqual(_.search(col, {'id': 1, 'name': 'Name'}), 0)

    def test_random(self):
        col = [1, 2, 3, 4]
        # Test 10 times
        for i in range(10):
            self.assertTrue(_.random(col) in col)
        self.assertEqual(len(_.random(col, 2)), 2)

    def test_only(self):
        col = [{'id': 1, 'name': 'Name'}, {'id': 2, 'name': 'Name', 'prop': 'value'}]
        self.assertEqual(_.only(col, 'id'), [1, 2])

    def test_chunk(self):
        col = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(_.chunk(col, 3), [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10]])

    def test_merge(self):
        first = [0, 1, 2, 3]
        second = [4, 5, 6]
        self.assertEqual(_.merge(first, second),  [0, 1, 2, 3, 4, 5, 6])

        # We could test with 5 but it would be overkilled :)
        first = [0, 1, 2, 3]
        second = [4, 5, 6]
        third = [0, 1, 2, 3]
        fourth = [1, 2, 3]
        self.assertEqual(_.merge(first, second, third, fourth),  [0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 1, 2, 3])

    def test_collapse(self):
        col = [[0, 1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.assertEqual(_.collapse(col),  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_sort(self):
        col = [3, 4, 0, 1, 2, 1, 5]
        self.assertEqual(_.sort(col), [0, 1, 1, 2, 3, 4, 5])
        self.assertEqual(_.sort(col, True), [5, 4, 3, 2, 1, 1, 0])

    def test_sort_by(self):
        col = [{'id': 2}, {'id': 1}, {'id': 3}, {'id': 5},{'id': 4}]
        self.assertEqual(_.sort_by(col, 'id'), [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 4}, {'id': 5}])
        self.assertEqual(_.sort_by(col, 'id', True), [{'id': 5}, {'id': 4}, {'id': 3}, {'id': 2}, {'id': 1}])
    
    def test_where(self):
        col = [{'id': 2}, {'id': 1}, {'id': 3}, {'id': 5},{'id': 4}]
        self.assertEqual(_.where(col, 'id', 1), [{'id': 1}])

    def test_where_in(self):
        col = [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 5},{'id': 4}]
        self.assertEqual(_.where_in(col, 'id', [1,3]), [{'id': 1}, {'id': 2}, {'id': 3}])


class TestAccessValueMethods(unittest.TestCase):
    def test_first(self):
        self.assertEqual(_.first([1, 2, 3]), 1)

    def test_get(self):
        self.assertEqual(_.get([1, 2, 3], 1), 2)

    def test_last(self):
        self.assertEqual(_.last([1, 2, 3]), 3)

    def test_iter(self):
        self.assertEqual(
            [i for i in Pywesome([1, 2, 3])],
            [1, 2, 3]
        )


class TestOperationsMethods(unittest.TestCase):

    def test_sum(self):
        col = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(_.sum(col), 55)

        col = [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 4}, {'id': 5}]
        self.assertEqual(_.sum(col, 'id'), 15)

    def test_avg(self):
        col = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(_.avg(col), 5)

        col = [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 4}, {'id': 5}]
        self.assertEqual(_.avg(col, 'id'), 3)


class TestGroupingMethods(unittest.TestCase):
    Entity = namedtuple('Entity', ['id', 'name'])

    def setUp(self):
        self.entity1 = self.Entity(id=1, name="a")
        self.entity2 = self.Entity(id=2, name="b")
        self.entity3 = self.Entity(id=3, name="a")

    def test_group_by_unique(self):
        self.collection = Pywesome([self.entity1, self.entity2])
        result = self.collection.group_by(
            'id',
            key_is_unique=True
        )
        self.assertEqual(
            result,
            {1: self.entity1, 2: self.entity2}
        )

    def test_group_by_not_unique(self):
        self.collection = Pywesome([self.entity1, self.entity2, self.entity3])
        result = self.collection.group_by(
            'name',
            value_list_transformation_function=
            lambda a: sorted(a, key=lambda e: e.id)
        )
        self.assertEqual(
            result,
            {'a': [self.entity1, self.entity3], 'b': [self.entity2]}
        )

    def test_group_by_custom_get_method(self):
        self.collection = Pywesome([{'id': 1}, {'id': 2}])
        result = self.collection.group_by(
            'id',
            key_is_unique=True,
            get_method=dict.get
        )
        self.assertEqual(
            result,
            {1: {'id': 1}, 2: {'id': 2}}
        )

    def test_group_by_transform_everything(self):
        self.collection = Pywesome([self.entity1, self.entity2, self.entity3])

        def change_entity(entity):
            return self.Entity(id=entity.id, name=entity.name + 'z')

        result = self.collection.group_by(
            'name',
            value_list_transformation_function=
            lambda a: sorted(a, key=lambda e: e.id),
            key_transformation_function=lambda a: a + 'y',
            value_transformation_function=change_entity
        )
        changed_entity_1 = change_entity(self.entity1)
        changed_entity_2 = change_entity(self.entity2)
        changed_entity_3 = change_entity(self.entity3)
        self.assertEqual(
            result,
            {
                'ay': [changed_entity_1, changed_entity_3],
                'by': [changed_entity_2]
            }
        )


class TestFormattingMethods(unittest.TestCase):

    def test_join(self):
        col = [0, 1, 2, 3, 4, 5]
        self.assertEqual(_.join(col), '0,1,2,3,4,5')

        col = [{'id': 1}, {'id': 2}]
        self.assertEqual(_.join(col, '-'), "{'id': 1}-{'id': 2}")

    def test_json(self):
        col = [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 4}, {'id': 5}]
        self.assertEqual(_.json(col), json.dumps(col))


class TestHelpersMethods(unittest.TestCase):

    def test_random_number(self):
        for i in range(10):
            i = _.random_number(0, 6)
            self.assertTrue(i >= 0 and i <= 6)


class TestPywesomeWrapperMethods(unittest.TestCase):

    def test_forwarding(self):
        col = Pywesome.collect([0, 1, 2, 3, 4, 5])
        self.assertEqual(col.reduce(lambda s,n: s + n), 15)
        self.assertEqual(col.reduce(lambda s,n: s + n, 10), 25)
        self.assertEqual(col.map(lambda n: n + 1).to_list(), [1, 2, 3, 4, 5, 6])

    def test_append(self):
        col = Pywesome.collect([0, 1, 2])
        col.append(3)
        self.assertEqual(col.last(), 3)

    def test_prepend(self):
        col = Pywesome.collect([0, 1, 2])
        col.prepend(3)
        self.assertEqual(col.first(), 3)

    def test_pop(self):
        col = Pywesome.collect([0, 1, 2])
        self.assertEqual(col.pop(2), 2)
        self.assertEqual(col.to_list(), [0, 1])
        self.assertEqual(col.pop(), 1)

    def test_count(self):
        col = Pywesome.collect([0, 1, 2])
        self.assertEqual(col.count(), 3)

    def test_to_list(self):
        col = Pywesome.collect([0, 1, 2])
        self.assertEqual(col.to_list(), [0, 1, 2])

    def test_to_json(self):
        col = Pywesome.collect([0, 1, 2])
        self.assertEqual(col.to_json(), "[0, 1, 2]")
        

if __name__ == '__main__':
    unittest.main()
