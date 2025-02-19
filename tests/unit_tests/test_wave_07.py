import pytest
from swap_meet.vendor import Vendor
from swap_meet.clothing import Clothing
from swap_meet.decor import Decor
from swap_meet.electronics import Electronics

### OG test code:
# def test_age_condition_same_across_classes():
#     items = [
#         Clothing(age=5),
#         Decor(age=5),
#         Electronics(age=5)
#     ]
#     five_age_description = items[0].age_description()
#     assert isinstance(five_age_description, str)
#     for item in items:
#         assert item.age_description() == five_age_description

#     items[0].age = 1
#     one_age_description = items[0].age_description()
#     assert isinstance(one_age_description, str)

#     for item in items:
#         item.age = 1
#         assert item.age_description() == one_age_description

#     assert one_age_description != five_age_description

### Refactored test plus additional tests:

def test_age_condition_same_across_classes():
    items = [
        Clothing(age=5),
        Decor(age=5),
        Electronics(age=5)
    ]

    clothing_age_description = items[0].age_description()

    decor_age_description = items[1].age_description()

    electronics_age_description = items[2].age_description()

    assert all(type(item) == str for item in [clothing_age_description, decor_age_description, electronics_age_description])
    ### OG test code:
    # assert type(clothing_age_description) == str
    # assert type(decor_age_description) == str
    # assert type(electronics_age_description) == str
    assert clothing_age_description == decor_age_description 
    assert decor_age_description == electronics_age_description

def test_age_description_expected_result():
    items = [
        Clothing(age=1),
        Decor(age=.5),
        Electronics(age=10),
        Clothing(age=100),
        Decor(age=0)
    ]

    one_year_old = items[0].age_description()

    less_than_one_year_old = items[1].age_description()

    ten_years_old = items[2].age_description()

    one_hundred_years_old = items[3].age_description()

    brand_new_item = items[4].age_description()

    assert one_year_old == "This item is 1 year old."
    assert less_than_one_year_old == "This item is less than 1 year old."
    assert ten_years_old == "This item is 10 years old."
    assert one_hundred_years_old == "This item is 100 years old."
    assert brand_new_item == "This item is brand new."

def test_none_age_gives_unknown_condition_description():
    item = Clothing(condition=3)

    none_age_description = item.age_description()

    assert none_age_description == "The age of this item is unknown. Please judge it by its condition."


# @pytest.mark.skip
def test_get_newest_item():
    item_a = Clothing(age=25.0)
    item_b = Decor(age=13.0)
    item_c = Clothing(age=4.0)
    item_d = Decor(age=10.0)
    item_e = Clothing(age=8.0)
    tai = Vendor(
        inventory=[item_a, item_b, item_c, item_d, item_e]
    )

    newest_item = tai.get_newest_item()

    assert newest_item == item_c


# @pytest.mark.skip
def test_get_newest_item_unknown_age_is_none():
    item_a = Decor(condition=2.0)
    item_b = Decor(condition=2.0)
    item_c = Decor(condition=4.0)
    tai = Vendor(
        inventory=[item_a, item_b, item_c]
    )

    newest_item = tai.get_newest_item()

    assert newest_item is None


# @pytest.mark.skip
def test_get_newest_item_with_duplicates():
    # Arrange
    item_a = Clothing(age=1.0)
    item_b = Clothing(age=1.0)
    item_c = Clothing(age=4.0)
    tai = Vendor(
        inventory=[item_a, item_b, item_c]
    )

    # Act
    newest_item = tai.get_newest_item()

    # Assert
    assert newest_item is item_a


# @pytest.mark.skip
def test_get_newest_item_with_duplicates_shuffle_order():
    # Arrange
    item_a = Clothing(age=10.0)
    item_b = Clothing(age=1.0)
    item_c = Clothing(age=1.0)
    tai = Vendor(
        inventory=[item_a, item_b, item_c]
    )

    # Act
    newest_item = tai.get_newest_item()

    # Assert
    assert newest_item is item_b


# @pytest.mark.skip
def test_get_newest_item_some_ages_unknown_ignores_unknowns():
    # Arrange
    item_a = Clothing(age=1.0)
    item_b = Clothing()
    item_c = Clothing(age=4.0)
    item_d = Decor()
    item_e = Electronics(age=0.5)
    tai = Vendor(
        inventory=[item_a, item_b, item_c, item_d, item_e]
    )

    # Act
    newest_item = tai.get_newest_item()

    # Assert
    assert newest_item is item_e


# @pytest.mark.skip
def test_swap_by_newest():
    # Arrange
    item_a = Decor(condition=2.0, age=1)
    item_b = Electronics(condition=4.0, age=3)
    item_c = Decor(condition=4.0, age=5)
    tai = Vendor(
        inventory=[item_c, item_b, item_a]
    )

    item_d = Clothing(condition=2.0, age=6)
    item_e = Decor(condition=4.0, age=2)
    item_f = Clothing(condition=4.0, age=15)
    jesse = Vendor(
        inventory=[item_f, item_e, item_d]
    )

    # Act
    result = tai.swap_by_newest(jesse)
    # Assert
    assert result
    assert len(tai.inventory) == 3
    assert len(jesse.inventory) == 3
    ### Refactoring
    # assert item_e and item_b and item_c in tai.inventory
    assert all(item in tai.inventory for item in [item_e, item_b, item_c])
    # assert item_a and item_d and item_f in jesse.inventory
    assert all(item in jesse.inventory for item in [item_a, item_d, item_f])
    assert item_a not in tai.inventory
    assert item_e not in jesse.inventory


# @pytest.mark.skip
def test_swap_by_newest_self_empty_inventory_returns_false():
    # Arrange
    tai = Vendor(
        inventory=[]
    )

    item_d = Clothing(condition=2.0, age=6)
    item_e = Decor(condition=4.0, age=2)
    item_f = Clothing(condition=4.0, age=15)
    jesse = Vendor(
        inventory=[item_f, item_e, item_d]
    )

    # Act
    result = tai.swap_by_newest(jesse)
    # Assert
    assert not result
    assert len(jesse.inventory) == 3
    assert len(tai.inventory) == 0
    assert all(item in jesse.inventory for item in [item_e, item_d, item_f])
    # assert item_e and item_d and item_f in jesse.inventory


# @pytest.mark.skip
def test_swap_by_newest_other_empty_inventory_returns_false():
        # Arrange
    item_a = Decor(condition=2.0, age=1)
    item_b = Electronics(condition=4.0, age=3)
    item_c = Decor(condition=4.0, age=5)
    tai = Vendor(
        inventory=[item_c, item_b, item_a]
    )

    jesse = Vendor(
        inventory=[]
    )

    # Act
    result = tai.swap_by_newest(jesse)

    # Assert
    assert not result
    assert len(tai.inventory) == 3
    assert len(jesse.inventory) == 0
    assert all(item in tai.inventory for item in [item_a, item_b])
    # assert item_a and item_b and item_c in tai.inventory


# @pytest.mark.skip
def test_swap_by_newest_all_items_age_unknown_returns_false():
    # Arrange
    item_a = Decor(condition=2.0)
    item_b = Electronics(condition=4.0)
    item_c = Decor(condition=4.0)
    tai = Vendor(
        inventory=[item_c, item_b, item_a]
    )

    item_d = Clothing(condition=2.0)
    item_e = Decor(condition=4.0)
    item_f = Clothing(condition=4.0)
    jesse = Vendor(
        inventory=[item_f, item_e, item_d]
    )

    # Act
    result = tai.swap_by_newest(jesse)

    # Assert

    assert not result
    assert len(tai.inventory) == 3
    assert len(jesse.inventory) == 3
    assert all(item in tai.inventory for item in [item_a, item_b, item_c])
    # assert item_d and item_e and item_f in jesse.inventory
    assert all(item in jesse.inventory for item in [item_d, item_e, item_f])


# @pytest.mark.skip
def test_swap_by_newest_self_items_age_unknown_returns_false():
    # Arrange
    item_a = Decor(condition=2.0)
    item_b = Electronics(condition=4.0)
    item_c = Decor(condition=4.0)
    tai = Vendor(
        inventory=[item_c, item_b, item_a]
    )

    item_d = Clothing(condition=2.0, age=1)
    item_e = Decor(condition=4.0, age=4)
    item_f = Clothing(condition=4.0, age=100)
    jesse = Vendor(
        inventory=[item_f, item_e, item_d]
    )

    # Act
    result = tai.swap_by_newest(jesse)

    # Assert

    assert not result
    assert len(tai.inventory) == 3
    assert len(jesse.inventory) == 3
    # assert item_a and item_b and item_c in tai.inventory
    # assert item_d and item_e and item_f in jesse.inventory
    assert all(item in jesse.inventory for item in [item_d, item_e, item_f])
    assert all(item in tai.inventory for item in [item_a, item_b, item_c])



# @pytest.mark.skip
def test_swap_by_newest_other_items_age_unknown_returns_false():
    # Arrange
    item_a = Decor(condition=2.0, age=4)
    item_b = Electronics(condition=4.0, age=7)
    item_c = Decor(condition=4.0, age=6)
    tai = Vendor(
        inventory=[item_c, item_b, item_a]
    )

    item_d = Clothing(condition=2.0)
    item_e = Decor(condition=4.0)
    item_f = Clothing(condition=4.0)
    jesse = Vendor(
        inventory=[item_f, item_e, item_d]
    )

    # Act
    result = tai.swap_by_newest(jesse)

    # Assert

    assert not result
    assert len(tai.inventory) == 3
    assert len(jesse.inventory) == 3
    # assert item_a and item_b and item_c in tai.inventory
    # assert item_d and item_e and item_f in jesse.inventory
    assert all(item in jesse.inventory for item in [item_d, item_e, item_f])
    assert all(item in tai.inventory for item in [item_a, item_b, item_c])
