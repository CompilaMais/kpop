import pytest
from numpy.testing import assert_almost_equal

from kpop import Population, Individual


#
# Test rendering and attributes
#
def test_population_attributes(popA):
    assert popA.is_biallelic
    assert popA.num_alleles == 2
    assert popA.ploidy == 2
    assert popA.num_loci == 5
    assert popA.size == 8
    assert popA.label == 'A'
    assert popA.populations == [popA]


def test_population_frequencies(popA):
    assert_almost_equal(popA.freqs_vector, [1.0, 0.0, 0.75, 0.25, 0.5])
    assert_almost_equal(popA.freqs_matrix, [
        (1.0, 0), (0.0, 1), (0.75, 0.25), (0.25, 0.75), (0.5, 0.5)
    ])
    assert popA.freqs == [
        {1: 1.00, 2: 0.00},
        {1: 0.00, 2: 1.00},
        {1: 0.75, 2: 0.25},
        {1: 0.25, 2: 0.75},
        {1: 0.50, 2: 0.50}
    ]


def test_create_individual_labels(popA):
    assert popA[0].label == 'A1'


def test_render_population(popA):
    assert popA.render() == '''
A1: 11 22 12 12 12
A2: 11 22 11 22 21
A3: 11 22 11 22 21
A4: 11 22 11 21 12
A5: 11 22 21 21 21
A6: 11 22 21 22 21
A7: 11 22 11 12 12
A8: 11 22 21 22 12
'''.strip()


#
# Test evolution and creation of new offspring
#
def test_create_offspring(popA):
    ind3 = popA.random_individual()
    ind2 = popA.new_offspring(label='Achild')
    ind1 = popA.new(label='Arandom')

    for ind in ind1, ind2, ind3:
        print(ind)
        assert ind.population is popA
        assert ind.label is not None
        assert ind[0, 0] == 1
        assert ind[1, 0] == 2


def test_fill_population_uses_the_correct_frequencies(popA):
    popA.fill(10)

    # These are fixed alleles
    assert popA[9][0, 0] == 1
    assert popA[9][0, 1] == 1
    assert popA[9][1, 0] == 2
    assert popA[9][1, 1] == 2


def test_population_genetic_drift(popA):
    # Frequencies do not change with evolution of zero generations
    pop2 = popA.genetic_drift(0, sample_size=0)
    assert popA.freqs == pop2.freqs

    # Genetic drift
    pop2 = popA.genetic_drift(10, sample_size=0)
    assert popA.freqs != pop2.freqs
    print(popA.freqs_vector)
    print(pop2.freqs_vector)

    # Fixed alleles do not change
    assert popA.freqs[0] == pop2.freqs[0]
    assert popA.freqs[1] == pop2.freqs[1]

    # Non-fixed alleles should always change
    for i in range(2, 5):
        assert popA.freqs[i] != pop2.freqs[i]


def test_make_random_population():
    pop = Population.make_random(30, 20)
    assert pop.size == 30
    assert pop.num_loci == 20
    delta = pop.freqs_vector - pop.empirical_freqs(as_matrix=True)[:, 0]
    assert abs(delta).mean() < 0.15


def test_add_remove_individual(popA):
    popA.add(popA.new_offspring())
    popA.remove()
