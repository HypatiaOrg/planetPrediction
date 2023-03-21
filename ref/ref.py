import os
import toml

repo_nme = "planetPrediction"
# directory information in the Hypatia Database
star_names_dir = os.path.dirname(os.path.realpath(__file__))
try:
    enclosing_dir, _ = star_names_dir.rsplit(repo_nme, 1)
    base_dir = os.path.join(enclosing_dir, repo_nme)
except ValueError:
    base_dir = os.path.dirname(star_names_dir)
    enclosing_dir = os.path.dirname(base_dir)

working_dir = os.path.join(base_dir, "planetpred")
ref_dir = os.path.join(working_dir, "reference")
if not os.path.exists(ref_dir):
    os.mkdir(ref_dir)


# for the simbad Query Class
sb_save_file_name = os.path.join(ref_dir, "simbad_query_data.pkl")
sb_save_coord_file_name = os.path.join(ref_dir, "simbad_coord_data.pkl")
sb_bad_star_name_ignore = os.path.join(ref_dir, "bad_starname_ignore.csv")
sb_main_ref_file_name = os.path.join(ref_dir, "simbad_main_ref_data.csv")


# for the Tess Input Catalog
tic_ref_filename = os.path.join(ref_dir, "tic_ref.csv")

# for the name correction files
annoying_names_filename = os.path.join(ref_dir, "annoying_names.csv")
popular_names_filename = os.path.join(ref_dir, "popular_names.csv")
name_correction_filename = os.path.join(ref_dir, "name_correction.psv")

# for the exoplanet archive
exoplanet_archive_filename = os.path.join(ref_dir, "nasaexoplanets.csv")

sb_ref_file_name = os.path.join(ref_dir, "simbad_ref_data.txt")
sb_desired_names = {
    "2mass", 'gaia dr3', "gaia dr2", "gaia dr1", "hd", "cd", "tyc", "hip", "gj", "hr", "bd", "ids", "tres", "gv",
    "ngc", "bps", "ogle", "xo", 'kepler', "k2", "*", "**", "v*", "name", 'wds', 'hats'
}

nea_exo_star_name_columns = {
    "hd_name",
    "hip_name",
    'hostname'
}

nea_might_be_zero = {
    "hostname",
    "pl_letter",
    "discoverymethod",
    "pl_pnum",
    "pl_orbeccen",
    "pl_orbincl",
}

nea_unphysical_if_zero_params = {
    "sy_dist",
    "st_mass",
    "st_masserr1",
    "st_masserr2",
    "st_rad",
    "st_raderr1",
    "st_raderr2",
    "pl_radj",
    "pl_radjerr1",
    "pl_radjerr2",
    "pl_bmassj",
    "pl_bmassjerr1",
    "pl_bmassjerr2",
    "pl_orbsmax",
    "pl_orbsmaxerr1",
    "pl_orbsmaxerr2",
    "pl_orbeccenerr1",
    "pl_orbeccenerr2",
    "pl_orbinclerr1",
    "pl_orbinclerr2"
}

nea_requested_data_types_default = [
    "hostname",
    "pl_letter",
    "sy_pnum",
    "gaia_id",
    'tic_id',
    "discoverymethod",
    "pl_orbper",
    "pl_orbpererr1",
    "pl_orbpererr2",
    "pl_orbsmax",
    "pl_orbsmaxerr1",
    "pl_orbsmaxerr2",
    "pl_orbeccen",
    "pl_orbeccenerr1",
    "pl_orbeccenerr2",
    "pl_orbincl",
    "pl_orbinclerr1",
    "pl_orbinclerr2",
    "pl_bmassj",
    "pl_bmassjerr1",
    "pl_bmassjerr2",
    "pl_radj",
    "pl_radjerr1",
    "pl_radjerr2",
    "pl_ratdor",
]


# write the user toml for the autostar package
autostar_toml = {'reference_data_dir': ref_dir,
                 'sb_bad_star_name_ignore_filename': sb_bad_star_name_ignore,
                 'sb_main_ref_filename': sb_main_ref_file_name,
                 'sb_save_filename': sb_save_file_name,
                 'sb_save_coord_filename': sb_save_coord_file_name,
                 'sb_ref_filename': sb_ref_file_name,
                 'tic_ref_filename': tic_ref_filename,
                 'annoying_names_filename': annoying_names_filename,
                 'popular_names_filename': popular_names_filename,
                 'exoplanet_archive_filename': exoplanet_archive_filename,
                 'name_correction_filename': name_correction_filename,
                 'sb_desired_names': sb_desired_names,
                 'nea_exo_star_name_columns': nea_exo_star_name_columns,
                 'nea_might_be_zero': nea_might_be_zero,
                 'nea_unphysical_if_zero_params': nea_unphysical_if_zero_params,
                 'nea_requested_data_types_default': nea_requested_data_types_default
                 }

ref_module_dir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(ref_module_dir, "user.toml"), 'w') as f:
    toml.dump(autostar_toml, f)
