from os.path import join, split, abspath

import numpy as np


def atomtype(structure, forcefield, non_atomistic=False):
    """Compare known atomtypes to those generated by foyer.

    Parameters
    ----------
    structure : parmed.Structure
        A parmed structure with `atom.type` attributes.
    forcefield : foyer.Forcefield
        A forcefield to use for atomtyping.

    Raises
    ------
    AssertionError

    """
    known_types = [atom.type for atom in structure.atoms]

    if non_atomistic:
        for atom in structure.atoms:
            atom.element = atom.name

    typed_structure = forcefield.apply(structure)

    generated_opls_types = list()
    for i, atom in enumerate(typed_structure.atoms):
        message = ('Found multiple or no OPLS types for atom {} in {}: {}\n'
                   'Should be atomtype: {}'.format(
            i, structure.title, atom.type, known_types[i]))
        assert atom.type, message
        generated_opls_types.append(atom.type)

    both = zip(generated_opls_types, known_types)

    n_types = np.array(range(len(generated_opls_types)))
    known_types = np.array(known_types)
    generated_opls_types = np.array(generated_opls_types)

    non_matches = np.array([a != b for a, b in both])
    message = "Found inconsistent OPLS types in {}: {}".format(
        structure.title,
        list(zip(n_types[non_matches],
                 generated_opls_types[non_matches],
                 known_types[non_matches])))
    assert not non_matches.any(), message


def get_fn(filename):
    """Gets the full path of the file name for a particular test file.

    Parameters
    ----------
    filename : str
        Name of the file to get

    Returns
    -------
    path: str
        Name of the test file with the full path location
    """
    return join(split(abspath(__file__))[0], 'files', filename)
