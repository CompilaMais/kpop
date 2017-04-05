import pytest

from kpop import Population, Individual


#
# Example population
#
@pytest.fixture
def popA_data():
    return [
        '11 22 12 12 12',
        '11 22 11 22 21',
        '11 22 11 22 21',
        '11 22 11 21 12',
        '11 22 21 21 21',
        '11 22 21 22 21',
        '11 22 11 12 12',
        '11 22 21 22 12',
    ]


@pytest.fixture
def popB_data():
    return [
        '22 22 22 12 22',
        '22 12 11 22 21',
        '22 12 11 12 21',
        '22 22 22 21 12',
    ]


@pytest.fixture
def popA(popA_data):
    return Population([Individual(x) for x in popA_data], label='A')


@pytest.fixture
def popB(popB_data):
    return Population([Individual(x) for x in popB_data], label='B')


#
# Random populations
#
@pytest.fixture
def num_loci():
    return 20


@pytest.fixture
def popA_random(num_loci):
    return Population.make_random(5, num_loci, label='A', min_prob=0.1)


@pytest.fixture
def popB_random(num_loci):
    return Population.make_random(5, num_loci, label='B', min_prob=0.9)


@pytest.fixture
def popAB(popA_random, popB_random):
    return popA + popB
