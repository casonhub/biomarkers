from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
 
    return render_template('index.html')

@app.route('/biomarkers', methods=['GET', 'POST'])
def biomarkers():
    # Load the Excel file and process data

    file_path = '/media/samantha/disk2/DriveD/Python/flasktest-main/bio_markers/data/biomarkers_new.xlsx'

    df = pd.read_excel(file_path)

    # Convert data into a dictionary where biomarkers map to their applicable disorders and associated details
    biomarker_dict = {}
    disorder_details = {}  # Dictionary to store disorder details

    for _, row in df.iterrows():
        biomarker = row['Bio_Markers']
        applicable_disorders = []
        for disorder, value in row.items():
            if disorder != 'Bio_Markers' and pd.notna(value):  # Check for non-empty value
                applicable_disorders.append(disorder)
                disorder_details[disorder] = value  # Store disorder details (e.g., "frontal and parietal cortices")
        biomarker_dict[biomarker] = set(applicable_disorders)  # Store as a set for easier intersection

    selected_biomarkers = []
    disorders = []

    if request.method == 'POST':
        # Retrieve selected biomarkers from the form
        selected_biomarkers = request.form.get('selected_biomarkers', '').split(',')
        print(f"Selected Biomarkers: {selected_biomarkers}")  # Debug: Print selected biomarkers

        # Apply AND logic: Find disorders common to all selected biomarkers
        if selected_biomarkers:
            # Initialize with disorders of the first selected biomarker
            initial_biomarker = selected_biomarkers[0]
            if initial_biomarker in biomarker_dict:
                common_disorders = biomarker_dict[initial_biomarker]
            else:
                common_disorders = set()

            # Intersect with disorders of remaining selected biomarkers
            for biomarker in selected_biomarkers[1:]:
                if biomarker in biomarker_dict:
                    common_disorders &= biomarker_dict[biomarker]
                else:
                    # If a biomarker is not in the dataset, the result will be empty
                    common_disorders = set()
                    break

            disorders = [
                (disorder, disorder_details.get(disorder, '')) for disorder in common_disorders
            ]  # Pair disorders with their details

        print(f"Associated Disorders: {disorders}")  # Debug: Print associated disorders

    return render_template(
        'biomarkers.html',
        selected_biomarkers=selected_biomarkers,
        disorders=disorders,
        biomarker_data=df['Bio_Markers'].unique()
    )




# Bio_M_Skills selection route
@app.route('/skills', methods=['GET', 'POST'])
def skills():

    # Load the Excel file and process data
    file_path = '/media/samantha/disk2/DriveD/Python/flasktest-main/bio_markers/data/Cognitive_skills.xlsx'

    df = pd.read_excel(file_path)

    # Convert data into a dictionary where Bio_M_Skills map to their applicable cognitive impairments
    biomarker_dict = {}
    for _, row in df.iterrows():
        biomarker = row['Bio_M_Skills']
        applicable_disorders = []
        for disorder, value in row.items():
            if disorder != 'Bio_M_Skills' and value == 'X':
                applicable_disorders.append(disorder)
        biomarker_dict[biomarker] = set(applicable_disorders)

    disorders = []
    selected_biomarkers = []

    if request.method == 'POST':
        # Retrieve selected Bio_M_Skills from the form
        selected_biomarkers = request.form.get('selected_biomarkers', '').split(',')
        print(f"Selected Bio_M_Skills: {selected_biomarkers}")  # Debug: Print selected Bio_M_Skills

        # Apply AND logic: find impairments common to all selected Bio_M_Skills
        if selected_biomarkers:
            # Initialize with impairments of the first selected Bio_M_Skills
            common_disorders = biomarker_dict.get(selected_biomarkers[0], set())

            # Intersect with impairments of remaining selected Bio_M_Skills
            for biomarker in selected_biomarkers[1:]:
                if biomarker in biomarker_dict:
                    common_disorders = common_disorders.intersection(biomarker_dict[biomarker])
                else:
                    # If biomarker doesn't exist, result will be empty
                    common_disorders = set()
                    break

            disorders = list(common_disorders)

        print(f"Cognitive Impairments meeting all selected Bio_M_Skills: {disorders}")  # Debug: Print result impairments

    return render_template(
        'skills.html',
        selected_biomarkers=selected_biomarkers,
        disorders=disorders,
        biomarker_data=df['Bio_M_Skills'].unique()
    )


# Bio_M_Skills selection route
@app.route('/cognitive', methods=['GET', 'POST'])
def cognitive():

    # Load the Excel file and process data
    file_path = '/media/samantha/disk2/DriveD/Python/flasktest-main/bio_markers/data/Cognitive_Skills_Data.xlsx'

    df = pd.read_excel(file_path)

    # Convert data into a dictionary where Bio_M_Skills map to their applicable disorders and biomarkers
    biomarker_dict = {}
    disorder_columns = df.columns[1:]  # Columns after 'Bio_M_Skills' contain disorders
    for _, row in df.iterrows():
        skill = row['Bio_M_Skills']
        biomarker_dict[skill] = {
            disorder: row[disorder] for disorder in disorder_columns if pd.notnull(row[disorder])
        }

    selected_biomarkers = []
    disorders_with_biomarkers = []  # To store disorders along with their biomarkers

    if request.method == 'POST':
        # Retrieve selected Bio_M_Skills from the form
        selected_biomarkers = request.form.get('selected_biomarkers', '').split(',')
        print(f"Selected Bio_M_Skills: {selected_biomarkers}")  # Debug: Print selected skills

        # Apply AND logic: Find disorders common to all selected Bio_M_Skills
        if selected_biomarkers:
            # Initialize with disorders of the first selected skill
            initial_skill = selected_biomarkers[0]
            if initial_skill in biomarker_dict:
                common_disorders = set(biomarker_dict[initial_skill].keys())
            else:
                common_disorders = set()

            # Intersect with disorders of remaining selected skills
            for skill in selected_biomarkers[1:]:
                if skill in biomarker_dict:
                    skill_disorders = set(biomarker_dict[skill].keys())
                    common_disorders &= skill_disorders
                else:
                    # If a skill is not in the dataset, the result will be empty
                    common_disorders = set()
                    break

            # Collect disorders along with their biomarkers for display
            for disorder in common_disorders:
                biomarkers = {
                    skill: biomarker_dict[skill][disorder]
                    for skill in selected_biomarkers if disorder in biomarker_dict[skill]
                }
                disorders_with_biomarkers.append({'disorder': disorder, 'biomarkers': biomarkers})

        print(f"Disorders and associated biomarkers: {disorders_with_biomarkers}")  # Debug: Print result

    return render_template(
        'cognitive.html',
        selected_biomarkers=selected_biomarkers,
        disorders_with_biomarkers=disorders_with_biomarkers,  # Pass disorders and biomarkers to the template
        biomarker_data=df['Bio_M_Skills'].unique()
    )


if __name__ == '__main__':
    app.run(debug=True)
