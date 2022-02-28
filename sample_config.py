from datetime import date

EMAIL = 'off'

WP_EMAIL_FROM = ''
WP_EMAIL_SERVER = ''
WP_EMAIL_PORT = 465
WP_EMAIL_USERNAME = ''
WP_EMAIL_PASSWORD = ''

LOG_LEVEL = 'DEBUG'
LOG_FILE = str(date.today()) + '-log.txt'

FACULTY_CODES = [i for i in range(200, 216)]
FACULTY_CODES.extend([
    "302", "304", "308", "921", "922", "671"
])

FILTER_CODES = [
    "900", "901", "904"
]

DEPTCONV = {
    "VetMed-VTH Sm Animal Anesthes": "Anesthesia Service",
    "VetMed-Animal Health Rsch Ctr": "Animal Health Research Center",
    "VetMed-Athens Diagnostic Lab": "Athens Veterinary Diagnostic Laboratory",
    "VetMed-Business Office": "Business Office",
    "VetMed-Vaccines & Immun Ctr": "Center for Vaccines and Immunology",
    "VetMed-Infectious Diseases": "Department of Infectious Diseases",
    "VetMed-Large Animal Medicine": "Department of Large Animal Medicine",
    "VetMed-Clinical Pathology Lab": "Department of Pathology",
    "VetMed-Dept of Biomedical Sci": "Biomedical Sciences",
    "VetMed-Pathology": "Department of Pathology",
    "VetMed-Physiology & Pharmacol": "Department of Physiology and Pharmacology",
    "VetMed-Population Health": "Department of Population Health",
    "VetMed-VTH Radiology": "Diagnostic Imaging Service",
    "VetMed-Educational Rsrcs Ctr": "Educational Resources Unit",
    "VetMed-Facilities": "Facilities",
    "VetMed-Food Animal Medicine": "Food Animal Health and Management",
    "VetMed-Histology Lab": "Histology Lab",
    "VetMed-SAMS Infect Disease Lab": "Infectious Diseases Laboratory",
    "VetMed-Information Technology": "Information Technology Services",
    "VetMed-IT-VetView": "Information Technology Services",
    "VetMed-SAMS-New Materials Inst": "New Materials Institute",
    "VetMed-Academic Affairs": "Office of Academic Affairs",
    "VetMed-External Affairs": "Office of Communications and Marketing",
    "VetMed-Development": "Office of Development and Alumni Relations",
    "VetMed-Research & Graduate Aff": "Office of Research and Faculty and Graduate Affairs",
    "VetMed-Veterinary Medic Dean": "Office of the Dean",
    "VetMed-Poultry Diagnos & Rsch": "Poultry Diagnostic and Research Center",
    "VetMed-VTH Small Animal Emerg": "Small Animal Emergency and Critical Care Service",
    "VetMed-Small Animal Med & Surg": "Small Animal Medicine & Surgery",
    "VetMed-Wildlife Disease Study": "Southeastern Cooperative Wildlife Disease Study",
    "VetMed-Tifton Diagnostic Lab": "Tifton Diagnostic and Investigational Laboratory",
    "VetMed-Biosci & Diagnost Imag": "Veterinary Biosciences and Diagnostic Imaging",
    "VetMed-Veterinary Teaching Hos": "Veterinary Teaching Hospital",
    "VetMed-VTH Admin Services": "Veterinary Teaching Hospital",
    "VetMed-VTH Administration": "Veterinary Teaching Hospital",
    "VetMed-VTH Central Supply": "Veterinary Teaching Hospital",
    "VetMed-VTH Large Animal Hosp": "Veterinary Teaching Hospital",
    "VetMed-VTH Patient Finan Srvcs": "Veterinary Teaching Hospital",
    "VetMed-VTH Pharmacy": "Veterinary Teaching Hospital",
    "VetMed-VTH Sm Animal Op Rm": "Veterinary Teaching Hospital",
    "VetMed-VTH Small Anim Spc Srvc": "Veterinary Teaching Hospital",
    "VetMed-VTH Warehouse": "Veterinary Teaching Hospital",
    "VetMed-VTH Sm Anim Commun Prac": "",
    "VetMed-VTH Sm Animal Intermed": ""
}

PAYGROUP_CODE_CONV = {
    "18A": "Staff",
    "18C": "Staff",
    "18F": "Faculty",
    "18G": "Graduate Assistant",
    "18H": "Staff",
    "18L": "Staff",
    "18N": "Affiliated Faculty",
    "18P": "Part Time Faculty",
    "18T": "Student",
    "18W": "Student",
    "18Y": "Faculty"
}

NO_ADDS = []
NO_RMS = []

INPUT_DIR = "inputfiles/"+str(date.today())+"/"
OUTPUT_DIR = "lastoutput/"+str(date.today())+"/"

HR_FILE_RAW = INPUT_DIR+"hr_raw.csv"
HR_CLEAN = INPUT_DIR+"hr.csv"
WP_FILE_RAW = INPUT_DIR+"wp_raw.csv"
WP_CLEAN = INPUT_DIR+"wp.csv"

WP_NO_EMPLID_CSV = OUTPUT_DIR+"/WP-No-Emplid.csv"
WP_NO_EMAIL_CSV = OUTPUT_DIR+"/WP-No-Email.csv"
WP_NO_IMAGE_CSV = OUTPUT_DIR+"/WP-No-Image.csv"
NOT_IN_WP = OUTPUT_DIR+"PeopleNotInWP.csv"
NOT_IN_HR = OUTPUT_DIR+"PeopleNotInHR.csv"