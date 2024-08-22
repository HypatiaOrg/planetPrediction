import os
import pandas as pd
from glob import glob

def combine_probabilities(save_file, output_dir):
    # Get all output files in the directory
    files = glob(os.path.join(output_dir, 'p-total-experiment-3-set*.csv'))

    combined_df = None
    counter = 1
    experiment_number = None

    # Iterate through each file
    for file in files:
        # Determine the experiment number from the filename
        if 'experiment-1' in file:
            experiment_number = 1
        elif 'experiment-2' in file:
            experiment_number = 2
        elif 'experiment-3' in file:
            experiment_number = 3
        
        # Read the file
        df = pd.read_csv(file, usecols=["star_name", "Probability"])

        # Rename the probability column to ensure uniqueness
        probability_column_name = f'Ens{counter}Prob'
        df = df.rename(columns={"Probability": probability_column_name})
        counter += 1

        # Merge with the combined dataframe
        if combined_df is None:
            combined_df = df
        else:
            combined_df = combined_df.merge(df, on='star_name', how='outer')

    # Replace NaN values with 'nan' for columns other than 'star_name'
    combined_df = combined_df.fillna('nan')

    # Filter stars with probability >= 90% in all columns
    probability_columns = [col for col in combined_df.columns if col.startswith('Ens') and col.endswith('Prob')]
    combined_df[probability_columns] = combined_df[probability_columns].apply(pd.to_numeric, errors='coerce')
    mask = (combined_df[probability_columns] >= 0.9).all(axis=1)
    high_prob_stars_df = combined_df[mask]

    if save_file:     
        # Save the filtered DataFrame to a CSV file
        high_prob_output_file = os.path.join(output_dir, 'high_prob_stars.csv')
        high_prob_stars_df.to_csv(high_prob_output_file, index=False)
        print("High probability stars file saved:", high_prob_output_file)

        # Save the combined dataframe to a new CSV file
        combined_output_file = os.path.join(output_dir, 'combined_probabilities.csv')
        combined_df.to_csv(combined_output_file, index=False)
        print("Combined file saved:", combined_output_file)
        return combined_df, high_prob_stars_df, experiment_number
    else:
        return combined_df, high_prob_stars_df, experiment_number

def combine_with_main(combined_df, high_prob_stars_df, working_dir, experiment_number):
    # Define the path to the main.csv file
    main_csv_path = os.path.join(working_dir, 'main.csv')
    
    # Define the columns to use from main.csv
    main_columns = ["star_name", "planet_letters", "Fe", "C", "O", "Na", "Mg", "Al", "Si", "Ca", "Sc", "Ti", "V", "Cr", "Mn", 
                    "Co", "Ni", "Y", "C_Mg", "O_Mg", "Si_Mg", "Ca_Mg", "Ti_Mg", "Fe_Mg", "C_Si", "O_Si", "Mg_Si", "Ca_Si", 
                    "Ti_Si", "Fe_Si", "C_O", "Si_O", "Mg_O", "Ca_O", "Ti_O", "Fe_O", "Exo", "sy_pnum", "pl_rade", "f_disk"]
    
    # Read the main.csv file
    main_df = pd.read_csv(main_csv_path, usecols=main_columns)
    
    # Merge the main dataframe with the combined probabilities dataframe on 'star_name'
    final_df = main_df.merge(combined_df, on='star_name', how='inner')

    # Merge high probability stars with main_df to get additional columns
    high_prob_with_main = high_prob_stars_df.merge(main_df, on='star_name', how='left')

    # Add the 'Experiment' column
    final_df.insert(final_df.columns.get_loc('star_name') + 1, 'Experiment', experiment_number)

    # Add the 'Overlap Star' column
    final_df.insert(final_df.columns.get_loc('Experiment') + 1, 'Overlap Star',
                    final_df['star_name'].apply(lambda x: 'Yes' if x in high_prob_stars_df['star_name'].values else 'No'))

    # Reorder columns
    cols_order = [
        "star_name", "Experiment", "Overlap Star",
        "Fe", "C", "O", "Na", "Mg", "Al", "Si", "Ca", "Sc", "Ti", "V", "Cr", "Mn",
        "Co", "Ni", "Y", "C_Mg", "O_Mg", "Si_Mg", "Ca_Mg", "Ti_Mg", "Fe_Mg",
        "C_Si", "O_Si", "Mg_Si", "Ca_Si", "Ti_Si", "Fe_Si",
        "C_O", "Si_O", "Mg_O", "Ca_O", "Ti_O", "Fe_O",
        "Exo", "planet_letters", "sy_pnum", "pl_rade", "f_disk"
    ]
    
    # Include probability columns at the end
    probability_columns = [col for col in final_df.columns if col.startswith('Ens') and col.endswith('Prob')]
    cols_order.extend(probability_columns)
    
    final_df = final_df[cols_order]

    # Replace NaN values with 'nan' for columns other than 'star_name'
    final_df = final_df.fillna('nan')

    # Update the 'f_disk' column values
    final_df['f_disk'] = final_df['f_disk'].replace({
        "N/A": '0',
        "thin": '1',
        "thick": '2'
    })

    # Replace probability values with 'nan' for stars with Exo = 1
    exo_mask = final_df['Exo'] == 1
    final_df.loc[exo_mask, probability_columns] = 'nan'

    # Rename columns
    final_df = final_df.rename(columns={
        "star_name": "Star Name","Fe": "[Fe/H]","C": "[C/H]","O": "[O/H]","Na": "[Na/H]","Mg": "[Mg/H]",
        "Al": "[Al/H]","Si": "[Si/H]","Ca": "[Ca/H]","Sc": "[Sc/H]","Ti": "[Ti/H]","V": "[V/H]",
        "Cr": "[Cr/H]","Mn": "[Mn/H]","Co": "[Co/H]","Ni": "[Ni/H]","Y": "[Y/H]","C_Mg": "C/Mg",
        "O_Mg": "O/Mg","Si_Mg": "Si/Mg","Ca_Mg": "Ca/Mg","Ti_Mg": "Ti/Mg","Fe_Mg": "Fe/Mg",
        "C_Si": "C/Si","O_Si": "O/Si","Mg_Si": "Mg/Si","Ca_Si": "Ca/Si","Ti_Si": "Ti/Si",
        "Fe_Si": "Fe/Si","C_O": "C/O","Si_O": "Si/O","Mg_O": "Mg/O","Ca_O": "Ca/O","Ti_O": "Ti/O",
        "Fe_O": "Fe/O","planet_letters": "Planet Letter","sy_pnum": "Number of Planets",
        "pl_rade": "Planet Radius","f_disk": "Disk Location"
    })

    final_output_file = os.path.join(output_dir, 'final_combined_data.csv')
    final_df.to_csv(final_output_file, index=False)
    print("Final combined file saved:", final_output_file)
    
    return final_df

# Define the output directory and working directory
output_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Total Probabilities')
working_dir = os.path.dirname(os.path.realpath(__file__))

# Call the function to combine probabilities
save_file = False
combined_df, high_prob_stars_df, experiment_number = combine_probabilities(save_file, output_dir)

# Call the function to combine with main.csv
final_df = combine_with_main(combined_df, high_prob_stars_df, working_dir, experiment_number)
