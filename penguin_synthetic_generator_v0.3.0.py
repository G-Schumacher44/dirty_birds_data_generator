# penguin_synthetic_generator_v2.py

# Version: v3

import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta

# === Configuration ===
N_PENGUINS = 4500
TAGGED_PERCENTAGE = 0.65
COLONIES = {
    'Biscoe West': 'Biscoe',
    'Dream South': 'Dream',
    'Torgersen North': 'Torgersen',
    'Cormorant East': 'Cormorant',
    'Shortcut Point': 'Shortcut'
}
SPECIES_INFO = {
    'Adelie': {'bill_mean': 38.8, 'bill_sd': 2.7, 'bill_depth_mean': 18.4, 'bill_depth_sd': 1.5, 'flipper_mean': 190, 'flipper_sd': 6.5, 'mass_mean': 3700, 'mass_sd': 300},
    'Chinstrap': {'bill_mean': 48.8, 'bill_sd': 3.3, 'bill_depth_mean': 18.5, 'bill_depth_sd': 1.6, 'flipper_mean': 196, 'flipper_sd': 7, 'mass_mean': 3700, 'mass_sd': 320},
    'Gentoo': {'bill_mean': 47.5, 'bill_sd': 3.0, 'bill_depth_mean': 14.8, 'bill_depth_sd': 1.2, 'flipper_mean': 217, 'flipper_sd': 6, 'mass_mean': 5000, 'mass_sd': 400}
}
AGE_GROUPS = ['Chick', 'Juvenile', 'Adult']
SEXES = ['Male', 'Female']

# === Setup ===
penguins = []
tag_counters = {'Adelie': 1, 'Chinstrap': 1, 'Gentoo': 1}
np.random.seed(42)
random.seed(42)

# === Helper Functions ===
def generate_tag(species):
    species_prefix = {'Adelie': 'ADE', 'Chinstrap': 'CHN', 'Gentoo': 'GEN'}[species]
    number = tag_counters[species]
    tag_counters[species] += 1
    return f"{species_prefix}-{number:04d}"

def random_capture_date():
    """
    Generates a biologically plausible capture date between October 2019 and December 2024,
    respecting austral summer field season boundaries.
    """
    season_start = datetime(2019, 10, 1)
    season_end = datetime(2024, 12, 31)
    delta_days = (season_end - season_start).days
    random_offset = random.randint(0, delta_days)
    return season_start + timedelta(days=random_offset)

def inject_mess(df, mess_level='moderate'):
    """
    Injects controlled 'messiness' into the dataset to simulate real-world field data issues.
    Mess levels: 'none', 'light', 'moderate', 'heavy'
    """
    if mess_level == 'none':
        return df

    n = len(df)
    # random.seed(42)
    # np.random.seed(42)

    # Messiness intensity
    if mess_level == 'light':
        error_rate = 0.03
    elif mess_level == 'moderate':
        error_rate = 0.08
    elif mess_level == 'heavy':
        error_rate = 0.15
    else:
        raise ValueError("Invalid mess_level. Choose from 'none', 'light', 'moderate', 'heavy'.")
    print(f"Injecting {mess_level} level of mess into the dataset... (error rate: {error_rate})")

    # Inject random missing values
    for col in ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']:
        mask = np.random.rand(n) < error_rate
        df.loc[mask, col] = np.nan

    # Inject NaNs into study_name
    mask = np.random.rand(n) < error_rate
    df.loc[mask, 'study_name'] = np.nan

    # Inject NaNs into clutch_completion
    mask = np.random.rand(n) < error_rate
    df.loc[mask, 'clutch_completion'] = np.nan

    # Inject NaNs into health_status
    mask = np.random.rand(n) < error_rate
    df.loc[mask, 'health_status'] = np.nan

    # Mess up 'sex'
    mask = np.random.rand(n) < error_rate
    df.loc[mask, 'sex'] = df['sex'].apply(lambda x: random.choice(['M', 'F', '', None, 'Unknown', '?', 'N/A']))

    # Introduce typos in species
    species_typos = {'Adelie': 'adeleie', 'Chisntrap': 'chisntrap', 'Gentoo': 'Gentto'}
    mask = np.random.rand(n) < error_rate
    df.loc[mask, 'species'] = df['species'].apply(lambda x: species_typos.get(x, x))

    def generate_bad_date():
        error_type = random.choice(['typo', 'swap', 'missing_digit', 'nonsense'])
        if error_type == 'swap':
            # Day/Month swapped
            day = random.randint(1, 28)
            month = random.randint(1, 12)
            year = random.choice(range(2019, 2025))
            return f"{day:02d}-{month:02d}-{year}"
        elif error_type == 'missing_digit':
            # Drop a digit
            year = random.choice([202, 2024])
            month = random.choice(range(1, 13))
            day = random.choice(range(1, 29))
            return f"{year}-{month:02d}-{day:02d}"
        elif error_type == 'typo':
            # Month typo
            return f"2024-{random.choice(['00', '13', '99'])}-{random.randint(1, 28):02d}"
        else:
            # Complete nonsense
            return random.choice(['not-a-date', '9999-99-99', 'error'])

    # Then in inject_mess:
    mask = np.random.rand(n) < error_rate
    df.loc[mask, 'capture_date'] = [generate_bad_date() for _ in range(mask.sum())]

    # Inject NaNs into capture_date
    mask = np.random.rand(n) < error_rate
    df.loc[mask, 'capture_date'] = np.nan

    # Screw up penguin IDs
    mask = np.random.rand(n) < error_rate
    def random_tag(x):
        if random.random() < 0.5:
            return np.nan
        else:
            return np.nan
    df.loc[mask, 'tag_id'] = df['tag_id'].apply(lambda x: random_tag(x) if pd.notnull(x) else x)

    # Fake or corrupted colony names
    mask = np.random.rand(n) < error_rate
    fake_colonies = ['Torgersen', 'Dream Island', 'Biscoe', 'Cormorant', 'Unknown', 'dream', 'biscoe 2', 'torgersen SE', 'cormorant NW', '/Shortcut', 'invalid_colony', 'TORGERSEN 4', ' short point', 'dream island']
    df.loc[mask, 'colony_id'] = [random.choice(fake_colonies) for _ in range(mask.sum())]

    # Introduce typos in island
    mask = np.random.rand(n) < error_rate
    fake_islands = ['bisco', 'dreamland', 'torg', 'cormor', 'short cut', 'unknown', '', None]
    df.loc[mask, 'island'] = [random.choice(fake_islands) for _ in range(mask.sum())]

    # Inject more plausible body mass outliers with increased variability
    mask = np.random.rand(n) < error_rate
    normal_max_mass = df['body_mass_g'].dropna().max()
    def generate_mass_outlier(x):
        random_factor = np.random.normal(1, 0.4)  # Mean of 1, standard deviation of 0.4 (greater spread)
        return x * random_factor if pd.notnull(x) else x
    df.loc[mask, 'body_mass_g'] = df.loc[mask, 'body_mass_g'].apply(generate_mass_outlier)
    # Clip to wider biological bounds for body_mass_g
    df['body_mass_g'] = df['body_mass_g'].clip(lower=2500, upper=7000)

    # Inject outliers into bill_depth_mm and flipper_length_mm with greater variability
    # Helper function to generate outliers with a more reasonable spread
    def generate_outlier(x, spread_factor=0.05, lower_clip=None, upper_clip=None):
        """
        Generates an outlier by applying a spread factor to the data and clipping within biological bounds.

        Parameters:
            x (float): Original data point.
            spread_factor (float): Factor to control how much the outlier deviates from the original value.
            lower_clip (float, optional): Lower bound to clip the outlier value.
            upper_clip (float, optional): Upper bound to clip the outlier value.
            
        Returns:
            float: The outlier value, adjusted within the specified bounds.
        """
        random_factor = np.random.normal(1, spread_factor)  # Use normal distribution with a small spread
        outlier_value = x * random_factor
        
        # Clip outlier value to ensure it stays within biological ranges
        if lower_clip is not None:
            outlier_value = max(outlier_value, lower_clip)
        if upper_clip is not None:
            outlier_value = min(outlier_value, upper_clip)
        
        return round(outlier_value, 2)  # Round to two decimal places for consistency

    def inject_outliers(df, mess_level='moderate'):
        """
        Function to inject outliers into the dataset with refined logic.
        """
        n = len(df)
        
        # For bill_depth_mm
        mask = np.random.rand(n) < 0.10  # Increased to 10% of the data (more intense)
        df.loc[mask, 'bill_depth_mm'] = df.loc[mask, 'bill_depth_mm'].apply(generate_outlier, spread_factor=0.1, lower_clip=13, upper_clip=21)

        # For bill_length_mm
        mask = np.random.rand(n) < 0.10  # Increased to 10% of the data
        df.loc[mask, 'bill_length_mm'] = df.loc[mask, 'bill_length_mm'].apply(generate_outlier, spread_factor=0.12, lower_clip=32, upper_clip=60)

        # For flipper_length_mm
        mask = np.random.rand(n) < 0.05
        df.loc[mask, 'flipper_length_mm'] = df.loc[mask, 'flipper_length_mm'].apply(generate_outlier, spread_factor=0.08, lower_clip=170, upper_clip=230)

        # For body_mass_g
        mask = np.random.rand(n) < 0.05
        df.loc[mask, 'body_mass_g'] = df.loc[mask, 'body_mass_g'].apply(generate_outlier, spread_factor=0.12, lower_clip=2500, upper_clip=6500)

        return df

    # Inject biologically constrained noise into measurements (excluding bill_depth_mm, flipper_length_mm, body_mass_g, which are handled above)
    # (Removed old outlier logic for bill_length_mm; handled in inject_outliers)

    # Mess up health_status with common typos and ambiguity
    mask = np.random.rand(n) < error_rate
    health_typos = ['Healthy', 'Unwell', 'Critically Ill', 'critcal ill', 'under weight', 'Overwight', 'ok', 'N/A', '', None]
    df.loc[mask, 'health_status'] = df['health_status'].apply(lambda x: random.choice(health_typos))

    # Mess up age_group with entry variants
    mask = np.random.rand(n) < error_rate
    age_typos = ['Chick', 'Juvenile', 'Adult', 'chik', 'juvenille', 'ADLT', 'unk', '', None]
    df.loc[mask, 'age_group'] = df['age_group'].apply(lambda x: random.choice(age_typos))

    # Inject NaNs into colony_id
    mask = np.random.rand(n) < error_rate
    df.loc[mask, 'colony_id'] = np.nan

    # Inject NaNs into island
    mask = np.random.rand(n) < error_rate
    df.loc[mask, 'island'] = np.nan

    # Inject messiness into study_name
    mask = np.random.rand(n) < error_rate
    fake_studies = ['PAPRI20X9', 'PAPR12021', 'PAPR2023', 'papri2024', '', None, 'N/A', 'STUDY_2022', 'PP2020']
    df.loc[mask, 'study_name'] = [random.choice(fake_studies) for _ in range(mask.sum())]

    # After injecting mess, inject refined outliers
    df = inject_outliers(df, mess_level=mess_level)
    return df


# === Resight duplication block ===
def duplicate_penguin_rows_for_resight(df, duplicate_rate=0.2):
    n_duplicates = int(len(df) * duplicate_rate)
    resight_samples = df.sample(n_duplicates, replace=True, random_state=42)

    resighted_rows = []
    for idx, row in resight_samples.iterrows():
        resight = row.copy()

        # Shift capture_date
        try:
            if pd.notnull(resight['capture_date']):
                original_date = pd.to_datetime(resight['capture_date'], format='%Y-%m-%d', errors='coerce')
                if not pd.isnull(original_date):
                    shifted = original_date + pd.DateOffset(years=random.choice([1, 2, 3]))
                    if shifted > datetime(2024, 2, 28):
                        continue  # skip this resight if it would exceed allowed date range
                    resight['capture_date'] = shifted.strftime('%Y-%m-%d')
        except Exception:
            pass  # keep if invalid date

        # Drift biometrics slightly (if not NaN)
        for col in ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']:
            if pd.notnull(resight[col]):
                drift_factor = random.uniform(0.95, 1.10)
                resight[col] = round(resight[col] * drift_factor, 2)

        # Adjust age_group
        if resight['age_group'] == 'Chick':
            resight['age_group'] = 'Juvenile'
        elif resight['age_group'] == 'Juvenile':
            resight['age_group'] = 'Adult'

        # Mutate health_status
        if pd.notnull(resight['health_status']):
            resight['health_status'] = random.choice(['Healthy', 'Unwell', 'Underweight', 'Overweight', 'Critically Ill'])

        # Optional: Add slight survival chance (simulate penguins missing in resight)
        if random.random() < 0.05:
            continue  # 5% chance penguin did not survive or was not found next year

        resighted_rows.append(resight)

    df_augmented = pd.concat([df, pd.DataFrame(resighted_rows)], ignore_index=True)
    return df_augmented

# === Helper: Inject missingness into species column ===
def inject_species_missingness(df, missing_rate=0.03):
    """
    Randomly inject missing values into the 'species' column to simulate field error.
    """
    n_rows = df.shape[0]
    n_missing = int(missing_rate * n_rows)
    missing_indices = np.random.choice(df.index, size=n_missing, replace=False)
    df.loc[missing_indices, 'species'] = np.nan
    return df

# === Data Generation ===
for _ in range(N_PENGUINS):
    species = random.choice(list(SPECIES_INFO.keys()))
    # Use weighted random sampling across colonies to reflect ecological weights
    colony_weights = {
        'Torgersen North': 30,
        'Dream South': 25,
        'Biscoe West': 20,
        'Cormorant East': 15,
        'Shortcut Point': 10
    }
    colonies, weights = zip(*colony_weights.items())
    colony = random.choices(colonies, weights=weights, k=1)[0]
    island = COLONIES[colony]
    age_group = random.choices(AGE_GROUPS, weights=[0.1, 0.2, 0.7])[0]
    sex = random.choice(SEXES) if random.random() < 0.5 else None
    capture_date = random_capture_date()

    bill_length = np.clip(np.random.normal(SPECIES_INFO[species]['bill_mean'], SPECIES_INFO[species]['bill_sd']), 32, 60)
    bill_depth = np.clip(np.random.normal(SPECIES_INFO[species]['bill_depth_mean'], SPECIES_INFO[species]['bill_depth_sd']), 13, 21)
    flipper_length = np.clip(np.random.normal(SPECIES_INFO[species]['flipper_mean'], SPECIES_INFO[species]['flipper_sd']), 170, 230)

    # Adjust body mass by age
    age_mass_factor = {'Chick': 0.6, 'Juvenile': 0.8, 'Adult': 1.0}[age_group]

    # Adjust body mass by sex
    sex_mass_factor = {"Male": 1.05, "Female": 0.95, None: 1.0}[sex]

    # Generate mass with age and sex adjustments
    base_mass = np.random.normal(SPECIES_INFO[species]['mass_mean'], SPECIES_INFO[species]['mass_sd'])
    body_mass = base_mass * age_mass_factor * sex_mass_factor
    body_mass = np.clip(body_mass, 2500, 6500)

    # Field stress adjustments by colony
    colony_stress_map = {
        'Torgersen North': 0.0,
        'Dream South': 0.05,
        'Biscoe West': 0.1,
        'Cormorant East': 0.15,
        'Shortcut Point': 0.2
    }
    stress_factor = colony_stress_map.get(colony, 0.0)

    # Species fragility modifiers
    species_band = {
        'Adelie': 0.20,
        'Chinstrap': 0.15,
        'Gentoo': 0.25
    }

    # Health classification with adjusted bounds and stress impact
    if pd.isnull(body_mass):
        health_status = 'UNKNOWN'
    else:
        mean_mass = SPECIES_INFO[species]['mass_mean']
        band = species_band.get(species, 0.20)
        low_thresh = mean_mass * (1 - band) * (1 + stress_factor)
        high_thresh = mean_mass * (1 + band) * (1 - stress_factor)

        if body_mass < low_thresh:
            health_status = 'Underweight'
        elif body_mass > high_thresh:
            health_status = 'Overweight'
        else:
            health_status = 'Healthy'

        # Add random error (simulate field mislabeling)
        if random.random() < 0.07:
            health_noise = ['Unwell', 'Critically Ill', 'Healthy', 'Underweight', 'Overweight']
            health_noise.remove(health_status)
            health_status = random.choice(health_noise)

    if random.random() < TAGGED_PERCENTAGE:
        tag_id = generate_tag(species)
    else:
        tag_id = None

    # Determine clutch completion
    clutch_probs = {"Adelie": 0.9, "Chinstrap": 0.85, "Gentoo": 0.8}
    clutch_completion = np.random.choice(
        ["Yes", "No"],
        p=[clutch_probs.get(species, 0.8), 1 - clutch_probs.get(species, 0.8)]
    )

    # Generate egg date only if clutch was completed
    egg_date = capture_date - timedelta(days=random.randint(0, 14))
    if egg_date < datetime(2019, 10, 1):
        egg_date = capture_date
    date_egg = egg_date.strftime('%Y-%m-%d') if clutch_completion == "Yes" else np.nan

    # Add study_name based on year and study convention
    study_year = capture_date.year
    study_name = f"PAPRI{study_year}"

    penguins.append({
        'tag_id': tag_id,
        'species': species,
        'bill_length_mm': round(bill_length, 2),
        'bill_depth_mm': round(bill_depth, 2),
        'flipper_length_mm': round(flipper_length, 1),
        'body_mass_g': round(body_mass),
        'age_group': age_group,
        'sex': sex,
        'colony_id': colony,
        'island': island,
        'capture_date': capture_date.strftime('%Y-%m-%d'),
        'health_status': health_status,
        'study_name': study_name,
        'clutch_completion': clutch_completion,
        'date_egg': date_egg
    })

# === Convert to DataFrame ===
df_penguins_v2 = pd.DataFrame(penguins)

# === Save Clean CSV ===
df_penguins_v2.to_csv('synthetic_penguins_v3.5_clean.csv', index=False)

# === Add Realistic Messiness and Augmentation ===
df_penguins_v2 = inject_mess(df_penguins_v2, mess_level='moderate')
df_penguins_v2 = duplicate_penguin_rows_for_resight(df_penguins_v2, duplicate_rate=0.45)
df_penguins_v2 = inject_species_missingness(df_penguins_v2, missing_rate=0.03)

# === Save Messy Field CSV ===
df_penguins_v2.to_csv('synthetic_penguins_v3.5.csv', index=False)

print(f"✅ Generated {len(df_penguins_v2)} synthetic penguins for v3.5 with clutch and egg-laying logic!")