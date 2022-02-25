"""
Given a set of manually entered keys (e.g., the planet name), populate as many
fields as possible for the catalog entry.
"""

import numpy as np
import os
from os.path import join
from textwrap import dedent

from astrobase.services.identifiers import simbad_to_tic, tic_to_gaiadr2

from agecat.paths import RAWDIR
from agecat.pipeline_utils import save_status, load_status

from cdips.utils import today_YYYYMMDD
from cdips.utils.catalogs import (
    get_nasa_exoplanet_archive_pscomppars,
    get_exofop_toi_catalog
)

##########
# CONFIG #
##########

COLS = [
    'star_info_provenance', 'pl_name', 'hostname', 'pl_letter', 'hostname', 'gaia_id', 'tic_id', 'ra',
    'dec', 'discoverymethod', 'disc_year', 'disc_facility', 'pl_orbper', 'pl_orbsmax',
    'pl_rade', 'pl_radeerr1', 'pl_radeerr2', 'pl_radjerr1', 'pl_radjerr2',
    'pl_radj', 'pl_bmasse', 'pl_bmasseerr1', 'pl_bmasseerr2', 'pl_bmassj',
    'pl_bmassjerr1', 'pl_bmassjerr2', 'pl_orbeccen', 'pl_imppar', 'pl_insol',
    'pl_insolerr1', 'pl_insolerr2', 'pl_eqt', 'pl_eqt_2', 'pl_eqt_3',
    'st_teff', 'st_rad', 'st_mass', 'st_met', 'st_logg', 'st_rotp', 'sy_dist',
    'sy_disterr1', 'sy_disterr2', 'sy_plx', 'sy_plxerr1', 'sy_plxerr2',
    'sy_vmag', 'sy_tmag', 'tran_flag', 'rv_flag', 'ima_flag', 'st_age', 'st_ageerr1', 'st_ageerr2'
]

DEFAULTDICT = {c:np.nan for c in COLS}

def get_auto_entries(status_file):

    s = load_status(status_file)

    # e.g., HIP 67522 b, TOI-1227 b
    pl_name = s['manual_entries']['pl_name']

    # e.g., HIP 67522, TOI-1227
    st_name = ' '.join(pl_name.split(' ')[:-1])

    # Try pulling the NASA exoplanet archive information.
    VER = today_YYYYMMDD()
    ea_df = get_nasa_exoplanet_archive_pscomppars(VER)
    mdf = ea_df.loc[ea_df['pl_name'] == pl_name]

    # pull Exoplanet Archive columns.
    if len(mdf) > 0:
        star_info_provenance = 'NASA Exoplanet Archive (pscomppars)'
        outdict = mdf.to_dict(orient='index')
        outdict['star_info_provenance'] = star_info_provenance
        outdict = outdict[COLS]
        save_status(status_file, 'auto_entries', outdict)
        return 1

    # if TOI (not in NEA), pull ExoFOP-TESS columns, trying with simbad
    is_toi = st_name.startswith("TOI")

    if is_toi:

        ex_df = get_exofop_toi_catalog(ver=TODAYSTR, returnpath=False)
        import IPython; IPython.embed()
        assert 0
        #FIXME FIXME TODO TODO IMPLEMENT!

        # default identifier is based on planet name.
        star_id = s['manual_entries']['pl_name'].split(' ')[0]

        tic_id = simbad_to_tic(star_id)
        gaiadr2_id = tic_to_gaiadr2(tic_id)

        star_info_provenance = 'TOI Catalog (ExoFOP-TESS) / TIC8'

    import IPython; IPython.embed()



        save_status(status_file, 'manual_entries', manual_entries)
