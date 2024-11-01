from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
 
    return render_template('index.html')

@app.route('/biomarkers', methods=['GET', 'POST'])
def biomarkers():

    # Load the Excel file and process data
    file_path = '/data/biomarkers.xlsx'
    df = pd.read_excel(file_path)

# Convert data into a dictionary where biomarkers map to their applicable disorders
    biomarker_dict = {}
    for _, row in df.iterrows():
        biomarker = row['Bio_Markers']
        applicable_disorders = []
        for disorder, value in row.items():
            if disorder != 'Bio_Markers' and value == 'X':
                applicable_disorders.append(disorder)
        biomarker_dict[biomarker] = applicable_disorders


    disorders = []
    selected_biomarkers = []
    
    if request.method == 'POST':
        selected_biomarkers = request.form.get('selected_biomarkers', '').split(',')
        print(f"Selected Biomarkers: {selected_biomarkers}")  # Debug: Print selected biomarkers

        # Collect all related disorders for selected biomarkers
        all_disorders = []
        for biomarker in selected_biomarkers:
            if biomarker in biomarker_dict:
                all_disorders.extend(biomarker_dict[biomarker])
        
        # Remove duplicates from disorders list
        disorders = list(set(all_disorders))
        print(f"Associated Disorders: {disorders}")  # Debug: Print associated disorders

    return render_template('biomarkers.html', 
                           selected_biomarkers=selected_biomarkers, 
                           disorders=disorders, 
                           biomarker_data=df['Bio_Markers'].unique())




# Bio_M_Skills selection route
@app.route('/skills', methods=['GET', 'POST'])
def skills():
     # Load the Excel file and process data
    file_path = '/media/samantha/disk2/DriveD/Python/flasktest-main/data/Cognitive_skills.xlsx'
    df = pd.read_excel(file_path)

# Convert data into a dictionary where biomarkers map to their applicable disorders
    biomarker_dict = {}
    for _, row in df.iterrows():
        biomarker = row['Bio_M_Skills']
        applicable_disorders = []
        for disorder, value in row.items():
            if disorder != 'Bio_M_Skills' and value == 'X':
                applicable_disorders.append(disorder)
        biomarker_dict[biomarker] = applicable_disorders


    disorders = []
    selected_biomarkers = []
    
    if request.method == 'POST':
        selected_biomarkers = request.form.get('selected_biomarkers', '').split(',')
        print(f"Selected Biomarkers: {selected_biomarkers}")  # Debug: Print selected biomarkers

        # Collect all related disorders for selected biomarkers
        all_disorders = []
        for biomarker in selected_biomarkers:
            if biomarker in biomarker_dict:
                all_disorders.extend(biomarker_dict[biomarker])
        
        # Remove duplicates from disorders list
        disorders = list(set(all_disorders))
        print(f"Associated Skills: {disorders}")  # Debug: Print associated disorders

    return render_template('skills.html', 
                           selected_biomarkers=selected_biomarkers, 
                           disorders=disorders, 
                           biomarker_data=df['Bio_M_Skills'].unique())

# Bio_M_Skills selection route
@app.route('/cognitive', methods=['GET', 'POST'])
def cognitive():
     # Load the Excel file and process data
    file_path = '/media/samantha/disk2/DriveD/Python/flasktest-main/data/Cognitive_BioMarker.xlsx'
    df = pd.read_excel(file_path)

# Convert data into a dictionary where biomarkers map to their applicable disorders
    biomarker_dict = {}
    for _, row in df.iterrows():
        biomarker = row['skill_disorders']
        applicable_disorders = []
        for disorder, value in row.items():
            if disorder != 'skill_disorders' and value == 'X':
                applicable_disorders.append(disorder)
        biomarker_dict[biomarker] = applicable_disorders


    disorders = []
    selected_biomarkers = []
    
    if request.method == 'POST':
        selected_biomarkers = request.form.get('selected_biomarkers', '').split(',')
        print(f"Selected Biomarkers: {selected_biomarkers}")  # Debug: Print selected biomarkers

        # Collect all related disorders for selected biomarkers
        all_disorders = []
        for biomarker in selected_biomarkers:
            if biomarker in biomarker_dict:
                all_disorders.extend(biomarker_dict[biomarker])
        
        # Remove duplicates from disorders list
        disorders = list(set(all_disorders))
        print(f"Associated Cognitive Functions: {disorders}")  # Debug: Print associated disorders

    return render_template('biomarkers.html', 
                           selected_biomarkers=selected_biomarkers, 
                           disorders=disorders, 
                           biomarker_data=df['skill_disorders'].unique())


if __name__ == '__main__':
    app.run(debug=True)
