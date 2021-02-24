import pytest

from src.common import Cleaner
from src.services import InviteToken
from tests.helpers import generate_uuid

cleaner = Cleaner()
invite_token_service = InviteToken()


def test_cleaner_is_mapped_pass(pause_notification):
    """
    GIVEN a cleaner instance and contest instance
    WHEN calling the is_mapped method of the cleaner instance on the contest instance
    THEN it should return the contest instance
    """
    invite_token = invite_token_service.create(email=pytest.email, status='active')
    assert cleaner.is_mapped(invite_token) == invite_token


def test_cleaner_is_mapped_fail():
    """
    GIVEN a cleaner instance and junk variable
    WHEN calling the is_mapped method of the cleaner instance on the junk variable
    THEN it should return None
    """
    junk = 1
    assert cleaner.is_mapped(junk) is None

    junk = None
    assert cleaner.is_mapped(junk) == junk


def test_is_id_pass():
    """
    GIVEN a cleaner instance and id variable
    WHEN calling the is_id method of the cleaner instance on the id variable
    THEN it should return the id variable
    """
    random_id = 1
    assert cleaner.is_id(random_id) == random_id

    random_id = 1000
    assert cleaner.is_id(random_id) == random_id


def test_is_id_fail():
    """
    GIVEN a cleaner instance and id variable
    WHEN calling the is_id method of the cleaner instance on the id variable
    THEN it should return the None
    """
    random_id = 1.0
    assert cleaner.is_id(random_id) is None

    random_id = 'one'
    assert cleaner.is_id(random_id) is None

    random_id = 0
    assert cleaner.is_id(random_id) is None

    random_id = generate_uuid()
    assert cleaner.is_id(random_id) is None


def test_is_string_pass():
    """
    GIVEN a cleaner instance and string variable
    WHEN calling the is_string method of the cleaner instance on the string variable
    THEN it should return the string variable
    """
    random_string = 'junk'
    assert cleaner.is_string(random_string) == random_string

    random_string = ''
    assert cleaner.is_string(random_string) == random_string


def test_is_string_fail():
    """
    GIVEN a cleaner instance and string variable
    WHEN calling the is_string method of the cleaner instance on the string variable
    THEN it should return the None
    """
    random_string = 1
    assert cleaner.is_string(random_string) is None

    random_string = ['one']
    assert cleaner.is_string(random_string) is None

    random_string = 'abc' * 1000
    assert cleaner.is_string(random_string) is None


def test_is_text_pass():
    """
    GIVEN a cleaner instance and text variable
    WHEN calling the is_text method of the cleaner instance on the text variable
    THEN it should return the text variable
    """
    random_text = 'junk'
    assert cleaner.is_text(random_text) == random_text

    random_text = 'abc' * 1000
    assert cleaner.is_text(random_text) == random_text

    random_text = ''
    assert cleaner.is_text(random_text) == random_text


def test_is_text_fail():
    """
    GIVEN a cleaner instance and text variable
    WHEN calling the is_text method of the cleaner instance on the text variable
    THEN it should return the None
    """
    random_text = 1
    assert cleaner.is_text(random_text) is None

    random_text = ['junk']
    assert cleaner.is_text(random_text) is None

    random_text = 'abcde' * 1000
    assert cleaner.is_text(random_text) is None


def test_is_int_pass():
    """
    GIVEN a cleaner instance and int variable
    WHEN calling the is_int method of the cleaner instance on the int variable
    THEN it should return the int variable
    """
    random_int = 1
    assert cleaner.is_int(random_int) == random_int

    random_int = -1
    assert cleaner.is_int(random_int) == random_int

    random_int = '1'
    assert cleaner.is_int(random_int) == 1

    random_int = 0
    assert cleaner.is_int(random_int) == random_int

    random_int = 9999999999
    assert cleaner.is_int(random_int) == random_int


def test_is_int_fail():
    """
    GIVEN a cleaner instance and int variable
    WHEN calling the is_int method of the cleaner instance on the int variable
    THEN it should return the None
    """
    random_int = 1.0
    assert cleaner.is_int(random_int) is None

    random_int = 'one'
    assert cleaner.is_int(random_int) is None

    random_int = 99999999999
    assert cleaner.is_int(random_int) is None

    random_int = generate_uuid()
    assert cleaner.is_int(random_int) is None


def test_is_uuid_pass():
    """
    GIVEN a cleaner instance and uuid variable
    WHEN calling the is_uuid method of the cleaner instance on the uuid variable
    THEN it should return the uuid variable
    """
    random_uuid = generate_uuid()
    assert cleaner.is_uuid(random_uuid) == random_uuid


def test_is_uuid_fail():
    """
    GIVEN a cleaner instance and uuid variable
    WHEN calling the is_uuid method of the cleaner instance on the uuid variable
    THEN it should return the None
    """
    random_uuid = 1.0
    assert cleaner.is_uuid(random_uuid) is None

    random_uuid = 'one'
    assert cleaner.is_uuid(random_uuid) is None

    random_uuid = 0
    assert cleaner.is_uuid(random_uuid) is None


def test_is_list_pass():
    """
    GIVEN a cleaner instance and list variable
    WHEN calling the is_list method of the cleaner instance on the list variable
    THEN it should return the list variable
    """
    random_list = []
    assert cleaner.is_list(random_list) == random_list

    random_list = [1, 2, 3]
    assert cleaner.is_list(random_list) == random_list

    random_list = ['1', '2', '3']
    assert cleaner.is_list(random_list) == random_list


def test_is_list_fail():
    """
    GIVEN a cleaner instance and list variable
    WHEN calling the is_list method of the cleaner instance on the list variable
    THEN it should return the None
    """
    random_list = ()
    assert cleaner.is_list(random_list) is None

    random_list = 'one'
    assert cleaner.is_list(random_list) is None

    random_list = 0
    assert cleaner.is_list(random_list) is None


def test_is_dict_pass():
    """
    GIVEN a cleaner instance and dict variable
    WHEN calling the is_dict method of the cleaner instance on the dict variable
    THEN it should return the dict variable
    """
    random_dict = {}
    assert cleaner.is_dict(random_dict) == random_dict

    random_dict = {'junk': 'abc'}
    assert cleaner.is_dict(random_dict) == random_dict

    random_dict = {'junk': ['1', '2', '3']}
    assert cleaner.is_dict(random_dict) == random_dict


def test_is_dict_fail():
    """
    GIVEN a cleaner instance and dict variable
    WHEN calling the is_dict method of the cleaner instance on the dict variable
    THEN it should return the None
    """
    random_dict = ()
    assert cleaner.is_dict(random_dict) is None

    random_dict = 'one'
    assert cleaner.is_dict(random_dict) is None

    random_dict = 0
    assert cleaner.is_dict(random_dict) is None

    random_dict = [0]
    assert cleaner.is_dict(random_dict) is None


def test_is_float_pass():
    """
    GIVEN a cleaner instance and float variable
    WHEN calling the is_float method of the cleaner instance on the float variable
    THEN it should return the float variable
    """
    random_float = 0.0
    assert cleaner.is_float(random_float) == random_float

    random_float = 1.000000000
    assert cleaner.is_float(random_float) == random_float


def test_is_float_fail():
    """
    GIVEN a cleaner instance and float variable
    WHEN calling the is_float method of the cleaner instance on the float variable
    THEN it should return the None
    """
    random_float = -1
    assert cleaner.is_float(random_float) is None

    random_float = 'one'
    assert cleaner.is_float(random_float) is None

    random_float = generate_uuid()
    assert cleaner.is_float(random_float) is None


def test_is_num_pass():
    """
    GIVEN a cleaner instance and num variable
    WHEN calling the is_num method of the cleaner instance on the num variable
    THEN it should return the num variable
    """
    random_num = 0.0
    assert cleaner.is_num(random_num) == random_num

    random_num = 1.000000000
    assert cleaner.is_num(random_num) == random_num

    random_num = 0
    assert cleaner.is_num(random_num) == random_num

    random_num = -1
    assert cleaner.is_num(random_num) == random_num


def test_is_num_fail():
    """
    GIVEN a cleaner instance and num variable
    WHEN calling the is_num method of the cleaner instance on the num variable
    THEN it should return the None
    """
    random_num = '-1'
    assert cleaner.is_num(random_num) is None

    random_num = 'one'
    assert cleaner.is_num(random_num) is None

    random_num = generate_uuid()
    assert cleaner.is_num(random_num) is None
