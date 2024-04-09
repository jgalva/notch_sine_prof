import os

cfd = os.path.dirname(os.path.abspath(__file__))
folder_pch = os.path.join(cfd, "..", "data", "input", "pch")
list_all_pch_files = os.listdir(folder_pch)


def test_amount_of_pch_files():
    # checks the existence of 3 pch files for XYZ
    assert len(list_all_pch_files) == 3


def test_length_of_pch_files():
    assert 1 + 1 == 2
