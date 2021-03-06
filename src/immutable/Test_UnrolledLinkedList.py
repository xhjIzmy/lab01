import unittest

from hypothesis import given
import hypothesis.strategies as st

from immutable.UnrolledLinkedList import *


class TestUnrolledLinkedList(unittest.TestCase):
    def test_size(self):
        self.assertEqual(size(None), 0)
        self.assertEqual(size(cons(cons(cons(None, 1), 2), 3)), 3)
        self.assertEqual(size(cons(cons(cons(cons(cons(cons(None, 1), 2), 3), 4), 5), 6)), 6)

    def test_getter(self):
        self.assertRaises(IndexError, lambda: getter(Node(5), 1))
        node = Node(5)
        cons(cons(cons(cons(cons(node, 1), 2), 3), 4), 5)
        self.assertEqual(getter(node, 1), 2)

    def test_setter(self):
        self.assertRaises(IndexError, lambda: setter(Node(5), 1, 2))
        node = Node(5)
        cons(cons(cons(node, 1), 3), 3)
        self.assertEqual(to_list(setter(node, 1, 3)), [1, 3, 3])

    def test_cons(self):
        self.assertEqual(cons(None, 1), cons(Node(3), 1))
        self.assertEqual(to_list(cons(cons(cons(None, 1), 2), 3)), [1, 2, 3])
        self.assertEqual(to_list(cons(cons(cons(cons(cons(cons(None, 1), 2), 3), 4), 5), 6)), [1, 2, 3, 4, 5, 6])
        node = Node(5)
        self.assertEqual(to_list(cons(cons(node, None), 1)), [None, 1])
        x = cons(cons(cons(cons(cons(cons(None, 1), 2), 3), None), "123"), 6)
        self.assertEqual(to_list(x), [1, 2, 3, None, "123", 6])

    @given(st.lists(st.integers()))
    def test_cons2(self, a):
        node = Node(5)
        for item in a:
            cons(node, item)
        self.assertEqual(to_list(node), a)

    def test_remove(self):
        self.assertRaises(IndexError, lambda: remove(cons(None, 1), 2))
        self.assertEqual(to_list(remove(cons(cons(cons(None, 1), 2), 3), 2)), [1, 2])
        x = cons(cons(cons(cons(cons(cons(None, 1), 2), 3), 4), 5), 6)
        x = remove(x, 3)

    def test_to_list(self):
        self.assertEqual(to_list(None), [])
        self.assertEqual(to_list(cons(cons(cons(None, 1), 2), 3)), [1, 2, 3])

    @given(st.lists(st.integers()))
    def test_to_list2(self, a):
        node = Node(5)
        for item in a:
            cons(node, item)
        self.assertEqual(to_list(node), a)

    def test_from_list(self):
        self.assertEqual(from_list([]), Node(5))
        node = Node(5)
        cons(cons(cons(node, 1), 2), 3)
        self.assertEqual(from_list([1, 2, 3]), node)

    @given(st.lists(st.integers()))
    def test_from_list2(self, a):
        node = Node(5)
        for item in a:
            cons(node, item)
        self.assertEqual(to_list(from_list(a)), to_list(node))

    def test_reverse(self):
        self.assertEqual(reverse(Node(5)), Node(5))
        self.assertEqual(reverse(cons(cons(cons(None, 1), 2), 3)), cons(cons(cons(None, 3), 2), 1))

    @given(st.lists(st.integers()))
    def test_reverse2(self, a):
        x = from_list(a)
        self.assertEqual(to_list(reverse(x)), a[::-1])

    def test_mconcat(self):
        self.assertEqual(mconcat(Node(5), None), Node(5))
        self.assertEqual(to_list(mconcat(cons(None, 1), cons(None, 2))), [1, 2])
        self.assertEqual(to_list(mconcat(cons(cons(cons(None, 1), 2), 3),
                                         cons(cons(cons(None, 4), 5), 6))), [1, 2, 3, 4, 5, 6])

    @given(st.lists(st.integers()))
    def test_monoid_identity(self, lst):
        self.assertEqual(to_list(mconcat(mempty(), from_list(lst))), to_list(from_list(lst)))

    def test_map(self):
        self.assertEqual(to_list(map(Node(5), str)), [])
        self.assertEqual(to_list(map(cons(cons(cons(None, 1), 2), 3), str)), ['1', '2', '3'])
        self.assertEqual(to_list(map(cons(cons(cons(None, 1), 2), 3), lambda x: x+1)), [2, 3, 4])

    def test_reduce(self):
        self.assertEqual(reduce(Node(5), lambda state, e: state + e, 0), 0)
        self.assertEqual(reduce(Node(5), lambda state, e: state + e, 1), 1)
        self.assertEqual(reduce(cons(cons(cons(None, 1), 2), 3), lambda state, e: state + e, 0), 6)

    def test_find(self):
        self.assertEqual(find(Node(5), 1), False)
        self.assertEqual(find(cons(cons(cons(None, 1), 2), 3), 2), True)
        self.assertEqual(find(cons(cons(cons(cons(cons(cons(None, 1), 2), 3), 4), 5), 6), 5), True)

    def test_iterator(self):
        x = [1, 2, 3]
        lst = from_list(x)
        tmp = []
        try:
            get_next = iterator(lst)
            while True:
                tmp.append(get_next())
        except StopIteration:
            pass
        self.assertEqual(x, tmp)
        self.assertEqual(to_list(lst), tmp)

        get_next = iterator(None)
        self.assertRaises(StopIteration, lambda: get_next())

    def test_filter(self):
        def is_even(n):
            return n % 2 == 0
        self.assertEqual(filter(cons(cons(cons(cons(cons(cons(None, 1), 2), 3), 4), 5), 6), lambda x: is_even(x)),
                         cons(cons(cons(None, 2), 4), 6))
        self.assertEqual(filter(cons(cons(cons(cons(cons(cons(None, 1), 2), 3), 4), 5), 6), lambda x: x % 2 == 0),
                         cons(cons(cons(None, 2), 4), 6))

    @given(st.lists(st.integers()))
    def test_from_list_to_list_equality(self, a):
        self.assertEqual(to_list(from_list(a)), a)

    @given(st.lists(st.integers()), st.lists(st.integers()), st.lists(st.integers()))
    def test_monoid_identity(self, lst1, lst2, lst3):
        a = from_list(lst1)
        b = from_list(lst2)
        c = from_list(lst3)
        self.assertEqual(mconcat(mempty(), a), a)
        self.assertEqual(mconcat(a, mempty()), a)
        self.assertEqual(mconcat(mconcat(mempty(), a), b), mconcat(mempty(), mconcat(a, b)))

        self.assertEqual(mconcat(mconcat(a, b), c), mconcat(a, mconcat(b, c)))


if __name__ == '__main__':
    unittest.main()
