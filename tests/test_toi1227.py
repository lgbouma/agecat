import os
from os.path import join
from agecat.paths import RAWDIR
from agecat.pipeline_utils import save_status, load_status
from textwrap import dedent

starid = 'TOI-1227'
status_file = join(RAWDIR, f"{starid}.txt")

if not os.path.exists(status_file):

    manual_entries = {
        'pl_name': 'TOI-1227 b',
        'pl_provenance': 'https://ui.adsabs.harvard.edu/abs/2021arXiv211009531M/abstract',
        'pl_status': 'Validated',
        'cluster': 'Sco OB2, LCC, Musca',
        'cluster_age': 11,
        'cluster_age_perr': 2,
        'cluster_age_merr': 2,
        'age_provenance': 'https://ui.adsabs.harvard.edu/abs/2021arXiv211009531M/abstract',
        'age_method': 'LDB, CAMD, Rotn',
        'is_ensemble_age': 1,
        'age_comment': dedent(
            """
            BANYAN-Σ yielded a high probability of ε Cha membership, which was
            not favored by Mann+21.  Instead, TOI-1227's kinematic association
            is with the "B" sub-population of LCC from Kerr+21, or the A0
            sub-group of the Crux Moving Group in Goldman+18.  Mann+21 refer to
            their FriendFinder selected group as "Musca", to be more memorable
            than the former two names.  Figure 8 of Mann+21 yields the
            strongest age constraint for the Musca sub-population, based on
            the existence of a significant drop in the Li levels around M3V
            without a full depletion being observed.
            """
        ).replace('\n',' ')
    }
    save_status(status_file, 'manual_entries', manual_entries)

s = load_status(status_file)

if 'auto_entries' not in s.keys():

    get_auto_entries(status_file)
