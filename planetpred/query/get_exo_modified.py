import os
from copy import copy

from autostar.table_read import row_dict, ClassyReader
from autostar.exo_archive import AllExoPlanets

from ref.ref import base_dir


# user options
refresh_data = False  # if True, will refresh the data from the internet, False will use the local data
verbose = True  # if True, will print out the progress of the code
hypatia_data_path = os.path.join(base_dir, "hypatia.csv") # path to the local copy of the Hypatia data

# get Hypatia data from a local copy
hypatia_all = ClassyReader(filename=hypatia_data_path)
# remove the star name column from the list of data keys
hypatia_data_keys = copy(hypatia_all.keys)
hypatia_data_keys.remove('f_preferred_name')

# fetch the NASA exoplanet archive data
all_exo = AllExoPlanets(refresh_data=refresh_data, verbose=verbose)
# get all the exoplanet data keys
exo_data_keys = all_exo.requested_data_types

# to make the header of the combined data CSV file
combined_data_keys = ['star_name', 'planet_letters'] + hypatia_data_keys + exo_data_keys

cutoff_mass = 0.095

class NoPlanet:
    def __init__(self):
        self.host_star = 'nan'

    class PlanetLetters():
        def __init__(self):
            self.planet_letters='nan'
    class PlanetParams():
        def __init__(self):
            self.planet_params = 'nan'
            self.exo_key = 'nan'

# start writing the combined data CSV file
with open(os.path.join(base_dir, "combined_data_test.csv"), "w") as combined_data_file:
    # write the CSV file header
    combined_data_file.write(",".join(combined_data_keys) + "\n")
    # iterate ove all the stars in the Hypatia data
    count = 0
    for star_name, *data_tuple in zip(*[hypatia_all.__getattribute__(column_name) for column_name in hypatia_all.keys]):
        # get the exoplanet data for this star
        exo_data_this_star = all_exo.get_data_from_star_name(star_name=star_name)

        # make a dictionary of hypatia to use for all the planets for this star (or system of stars)
        hypatia_data_dict = {column_name: data_value for column_name, data_value in zip(hypatia_data_keys, data_tuple)}
        
        if exo_data_this_star is None:
            # no exoplanet data for this star, so we skip these rows from the combined data CSV file
            exo_data_this_star = NoPlanet().PlanetLetters()
            exo_planet = NoPlanet().PlanetParams()

            # make a dictionary of exoplanet data for this planet
            planet_data_dict = {
                exo_key: (exo_planet.exo_key if exo_key in exo_planet.planet_params else "")
                for exo_key in exo_data_keys
            }

            planet_letter = ''

            # put all the data in one combined dictionary
            combined_data_dict = {'star_name': star_name, 'planet_letters': planet_letter} |\
                                 hypatia_data_dict | planet_data_dict
            # convert the combined data dictionary to a list of strings, in the order of the combined data keys
            write_values = [str(combined_data_dict[key]) for key in combined_data_keys]
            # write the data to the combined data CSV file
            combined_data_file.write(",".join(write_values) + "\n")
        else:    
        # iterate over all the planets for this star
            for planet_letter in sorted(exo_data_this_star.planet_letters):
                count += 1
                # get the exoplanet data for this planet
                exo_planet = exo_data_this_star.__getattribute__(planet_letter)

                if ((hasattr(exo_planet,'pl_bmassj') == False) or (exo_planet.pl_bmassj < cutoff_mass)):
                    continue
                # make a dictionary of exoplanet data for this planet
                planet_data_dict = {
                    exo_key: (exo_planet.__getattribute__(exo_key) if exo_key in exo_planet.planet_params else "")
                    for exo_key in exo_data_keys
                }

                # put all the data in one combined dictionary
                combined_data_dict = {'star_name': star_name, 'planet_letters': planet_letter} |\
                                     hypatia_data_dict | planet_data_dict
                # convert the combined data dictionary to a list of strings, in the order of the combined data keys
                write_values = [str(combined_data_dict[key]) for key in combined_data_keys]
                # write the data to the combined data CSV file
                combined_data_file.write(",".join(write_values) + "\n")
