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
hypatia_data_keys.remove('star_name')

# fetch the NASA exoplanet archive data
all_exo = AllExoPlanets(refresh_data=refresh_data, verbose=verbose)
# get all the exoplanet data keys
exo_data_keys = all_exo.requested_data_types

# to make the header of the combined data CSV file
combined_data_keys = ['star_name', 'planet_letters'] + hypatia_data_keys + exo_data_keys + ['Exo']

# cutoff_mass_j = 0.095
# previous_mass = 0
cutoff_radius_e = 3.5

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

# put all the data in one combined dictionary
def combine_data(star_name, planet_letter, hypatia_data_dict, planet_data_dict):

    combined_data_dict = {'star_name': star_name, 'planet_letters': planet_letter} |\
                         hypatia_data_dict | planet_data_dict
    # convert the combined data dictionary to a list of strings, in the order of the combined data keys
    write_values = [str(combined_data_dict[key]) for key in combined_data_keys]
    # write the data to the combined data CSV file
    combined_data_file.write(",".join(write_values) + "\n")
    return

def replace_blank_strings():
    # Replace blank strings with 'nan' for hypatia data
    for key in hypatia_data_dict.keys():
        if (hypatia_data_dict[key] == '' or hypatia_data_dict[key] == ' '):
            hypatia_data_dict.update({key:float('nan')})

    # Replace blank strings with 'nan' for exoplanet data
    for key in planet_data_dict.keys():
        if (planet_data_dict[key] == '' or planet_data_dict[key] == ' '):
            planet_data_dict.update({key:float('nan')})
    return

# start writing the combined data CSV file
with open(os.path.join(base_dir, "main.csv"), "w") as combined_data_file:
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
            count+=1
            # no exoplanet data for this star, so we skip these rows from the combined data CSV file
            exo_data_this_star = NoPlanet().PlanetLetters()
            exo_planet = NoPlanet().PlanetParams()

            # make a dictionary of exoplanet data for this planet
            planet_data_dict = {
                exo_key: (exo_planet.exo_key if exo_key in exo_planet.planet_params else "")
                for exo_key in exo_data_keys
            }

            planet_data_dict['Exo'] = 0
            planet_letter = str()            
            replace_blank_strings()
            combine_data(star_name, planet_letter, hypatia_data_dict, planet_data_dict)
            
        else:
            pl_radius = 0
            pl_loop = 0
            pl_num = len(exo_data_this_star.planet_letters)
            pl_letter = str(sorted(exo_data_this_star.planet_letters)[0])
            largest_letter = 0

            for planet_letter in sorted(exo_data_this_star.planet_letters):
                count += 1
                
                # get the exoplanet data for this planet
                exo_planet = exo_data_this_star.__getattribute__(planet_letter)

                # Verify if the planet has a recorded mass
                if(hasattr(exo_planet,'pl_rade')==False):
                    continue
                # Verify if the planet's mass is less than the cutoff mass.
                elif(exo_planet.pl_rade > cutoff_radius_e):
                    continue
                # Verify if the planet orbits the same star as the previous.
                elif(len(exo_data_this_star.planet_letters) > 1):
                    # If it does, check if the current planets mass is larger than the previous
                    if(exo_planet.pl_rade > pl_radius):
                        pl_radius = exo_planet.pl_rade
                        pl_letter = planet_letter
                        largest_letter = pl_loop
                    pl_loop += 1
                # Write out the data
                if (pl_loop == pl_num):
                    exo_true = exo_data_this_star.__getattribute__(pl_letter)
                    planet_data_dict = {
                        exo_key: (exo_true.__getattribute__(exo_key) if exo_key in exo_true.planet_params else "")
                        for exo_key in exo_data_keys
                        }
                    planet_data_dict['Exo'] = 1
                    # The error is in planet_data_dict since I'm writing out the final planet in the dictionary
                    replace_blank_strings()
                    combine_data(star_name, pl_letter, hypatia_data_dict, planet_data_dict)

##                    # DEBUG
##                    if (star_name == 'HIP 17264'):
##                        print(star_name, planet_letter, exo_planet.pl_rade)
##                        print(star_name, pl_letter, pl_radius)
##                        exo_true = exo_data_this_star.__getattribute__(pl_letter)
##                        print(exo_true)
##                        planet_true_dict = {
##                            exo_key: (exo_true.__getattribute__(exo_key) if exo_key in exo_true.planet_params else "")
##                            for exo_key in exo_data_keys
##                        }
##                        print(planet_true_dict)
##                        input()               

                    # Reset variables to default values
                    pl_radius = 0
                    pl_loop = 0
                    pl_letter = str(sorted(exo_data_this_star.planet_letters)[0])
                elif (pl_loop == 0):
                    # make a dictionary of exoplanet data for this planet
                    planet_data_dict = {
                        exo_key: (exo_planet.__getattribute__(exo_key) if exo_key in exo_planet.planet_params else "")
                        for exo_key in exo_data_keys
                    }
                    planet_data_dict['Exo'] = 1
                    replace_blank_strings()
                    combine_data(star_name, planet_letter, hypatia_data_dict, planet_data_dict)
                    
                    # Reset variables to default values
                    pl_radius = 0
                    pl_letter = str(sorted(exo_data_this_star.planet_letters)[0])
