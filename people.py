import csv
import os
import sys
import config as cfg
import concurrent.futures
from datetime import date
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

loglevel = getattr(logging, cfg.LOG_LEVEL.upper(), None)
logging.basicConfig(filename=cfg.LOG_FILE, level=loglevel,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

class PeopleFixer:
    def __init__(self):
        pass
    def __repr__(self):
        return f'PeopleFixer()'

    def startup():
        """ Startup """
        files_to_clean = ['wp_raw.csv', 'hr_raw.csv']
        PeopleFixer.check_paths(files_to_clean)

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            cleanup = {executor.submit(PeopleFixer.convert_to_clean, file): file for file in files_to_clean}
            for future in concurrent.futures.as_completed(cleanup):
                file = cleanup[future]
                try:
                    future.result()
                except Exception as e:
                    print(f'Something went wrong with {file}!')
                    logging.error('Something went wrong with {file}!')
                    print(e)
                    sys.exit()
         
        PeopleFixer.compare_files()
        PeopleFixer.imageemail()

    def check_paths(files_to_clean):
        """ Create directories as needed """
        if not os.path.exists(cfg.INPUT_DIR):
            os.mkdir(cfg.INPUT_DIR)
            print(f'Had to make {cfg.INPUT_DIR} so it seems you have not set up your input files yet. Stopping.')
            logging.error(f'Had to create {cfg.INPUT_DIR} : you have not set up your input files yet. The program requires the input folder, which contains the two source files.')
            sys.exit()
        if not os.path.exists(cfg.OUTPUT_DIR):
            os.mkdir(cfg.OUTPUT_DIR)
            print(f'Creating output directory at {cfg.OUTPUT_DIR}.')
            logging.info(f'Creating output directory at {cfg.OUTPUT_DIR}.')
        else:
            print(f'Output directory already exists at {cfg.OUTPUT_DIR}.')
            logging.info(f'Output directory already exists at {cfg.OUTPUT_DIR}.')
        for fs in files_to_clean:
            if not os.path.exists(cfg.INPUT_DIR+fs):
                print(f'{cfg.INPUT_DIR+fs} does not exist! Stopping.')
                logging.error(f'{cfg.INPUT_DIR+fs} does not exist! Stopping.')
                print(f'Make sure you have the {fs} file in {cfg.INPUT_DIR}.')
                sys.exit()

    def convert_to_clean(file):
        """ Convert raw file to clean file """
        """ Open reading and writing files and start the process """
        try:
            with open(cfg.INPUT_DIR+file, 'r') as raw_file:
                with open(cfg.OUTPUT_DIR+file[:-8]+'_clean.csv', 'w', newline='') as clean_file:
                    reader = csv.DictReader(raw_file)
                    fieldnames = reader.fieldnames
                    writer = csv.DictWriter(clean_file,fieldnames=fieldnames)
                    writer.writeheader()
                    with open(cfg.WP_NO_IMAGE_CSV, 'w', newline='') as noimgnew:
                        mwriter = csv.DictWriter(noimgnew,fieldnames=reader.fieldnames)
                        mwriter.writeheader()
                    for row in reader:
                        if 'JobCode_Descr' in row:
                            hrfile = True
                            row['First_Name'] = row['First_Name'].capitalize()
                            row['Last_Name'] = row['Last_Name'].capitalize()
                            row['HR_Dept_Descr'] = cfg.DEPTCONV[row['HR_Dept_Descr']]
                            row['PayGroup_Code'] = cfg.PAYGROUP_CODE_CONV[row['PayGroup_Code']]
                            if row['PayGroup_Code'] != 'Student' and row['Emplid'] not in cfg.NO_ADDS:
                                writer.writerow(row)
                        else:
                            wpfile = True                       
                            row['First Name'] = row['First Name'].capitalize()
                            row['Last Name'] = row['Last Name'].capitalize()
                            if not row['Emplid'] and row['Status']=='publish':
                                with open(cfg.WP_NO_EMPLID_CSV, 'a', newline='') as wp_no_emplid_file:
                                    ewriter = csv.DictWriter(wp_no_emplid_file, fieldnames=fieldnames)
                                    ewriter.writerow(row)
                            if not row['Email'] and row['Status']=='publish':
                                with open(cfg.WP_NO_EMAIL_CSV, 'a', newline='') as wp_no_email_file:
                                    mwriter = csv.DictWriter(wp_no_email_file,fieldnames=fieldnames)
                                    mwriter.writerow(row)
                            if not row['Image Featured'] and row['Status']=='publish':
                                with open(cfg.WP_NO_IMAGE_CSV, 'a', newline='') as wp_no_image_file:
                                    iwriter = csv.DictWriter(wp_no_image_file,fieldnames=fieldnames)
                                    iwriter.writerow(row)
                            if row['Status'] == 'publish' and row['Emplid']:
                                writer.writerow(row)
        except Exception as e:
            print(f'Something went wrong opening {file}!')
            logging.error(f'Something went wrong opening {file}!')
            print(e)
            sys.exit()

    def compare_files():
        """ Compare clean files """
        print("Comparing the clean files has begun!")
        with open(cfg.OUTPUT_DIR+'wp_clean.csv', 'r') as wp_file:
            with open(cfg.OUTPUT_DIR+'hr_clean.csv', 'r') as hr_file:
                wp_reader = csv.DictReader(wp_file)
                hr_reader = csv.DictReader(hr_file)
                wp_emplids = [x['Emplid'] for x in wp_reader]
                hr_emplids = [x['Emplid'] for x in hr_reader]
                not_in_wp = [x for x in hr_emplids if x not in wp_emplids]
                not_in_hr = [x for x in wp_emplids if x not in hr_emplids]

        with open(cfg.OUTPUT_DIR+'wp_clean.csv', 'r') as wp_file:
            with open(cfg.OUTPUT_DIR+'hr_clean.csv', 'r') as hr_file:
                wp_reader = csv.DictReader(wp_file)
                hr_reader = csv.DictReader(hr_file)
                for wprow in wp_reader:
                    if wprow['Emplid'] in not_in_hr:
                        with open(cfg.OUTPUT_DIR+'not_in_hr.csv', 'a', newline='') as mismatch_file:
                            mismatch_writer = csv.DictWriter(mismatch_file, fieldnames=wp_reader.fieldnames)
                            mismatch_writer.writerow(wprow)
                            logging.info(f'{wprow["Emplid"]} is in wp_clean.csv but not in hr_clean.csv')
                    for hrrow in hr_reader:
                        if hrrow['Emplid'] in not_in_wp:
                            with open(cfg.OUTPUT_DIR+'not_in_wp.csv', 'a', newline='') as mismatch_file:
                                mismatch_writer = csv.DictWriter(mismatch_file, fieldnames=hr_reader.fieldnames)
                                mismatch_writer.writerow(hrrow)
                                logging.info(f'{hrrow["Emplid"]} is in hr_clean.csv but not in wp_clean.csv')
                        if wprow['Emplid'] == hrrow['Emplid']:
                            logging.info(f'{wprow["Emplid"]} is in both wp_clean.csv and hr_clean.csv')
                            if wprow['First Name'] != hrrow['First_Name'] or wprow['Last Name'] != hrrow['Last_Name']:
                                with open(cfg.OUTPUT_DIR+'name_mismatch.csv', 'a', newline='') as mismatch_file:
                                    mismatch_writer = csv.DictWriter(mismatch_file, fieldnames=wp_reader.fieldnames)
                                    mismatch_writer.writerow(wprow)
                                    logging.info(f'{wprow["Emplid"]} has a name mismatch')
                            if wprow['Home Departments'] != hrrow['HR_Dept_Descr']:
                                with open(cfg.OUTPUT_DIR+'dept_mismatch.csv', 'a', newline='') as mismatch_file:
                                    mismatch_writer = csv.DictWriter(mismatch_file, fieldnames=wp_reader.fieldnames)
                                    mismatch_writer.writerow(wprow)
                                    logging.info(f'{wprow["Emplid"]} has a department mismatch')
                            if wprow['EE Types'] != hrrow['PayGroup_Code']:
                                with open(cfg.OUTPUT_DIR+'paygroup_mismatch.csv', 'a', newline='') as mismatch_file:
                                    mismatch_writer = csv.DictWriter(mismatch_file, fieldnames=wp_reader.fieldnames)
                                    mismatch_writer.writerow(wprow)
                                    logging.info(f'{wprow["Emplid"]} has a paygroup mismatch')
                            if wprow['Email'] != hrrow['UGA_Email']:
                                with open(cfg.OUTPUT_DIR+'email_mismatch.csv', 'a', newline='') as mismatch_file:
                                    mismatch_writer = csv.DictWriter(mismatch_file, fieldnames=wp_reader.fieldnames)
                                    mismatch_writer.writerow(wprow)
                                    logging.info(f'{wprow["Emplid"]} has an email mismatch')
        print("Comparing the clean files has finished!")

    def imageemail():
        print("Here")
        """ Open the csv that contains our list of imageless people, and email them """
        with open(cfg.OUTPUT_DIR+'WP-No-Image.csv', 'r') as wp_no_image_file:
            wp_no_image_reader = csv.DictReader(wp_no_image_file)
            for row in wp_no_image_reader:
                if row['Email']:
                    email = row['Email']
                    subject = 'Please upload a photo for your profile'
                    body = '''
                    Hi {},
                    I noticed that you don't have a photo on your profile.
                    Please upload a photo for your profile.
                    Thank you,
                    {}
                    '''.format(row['First Name'], cfg.WP_EMAIL_FROM)
                    # send_email(email, subject, body)
                    logging.info(f'Sent email to {email}')
                else:
                    with open(cfg.WP_NO_EMAIL_CSV, 'a', newline='') as wp_no_email_file:
                        mwriter = csv.DictWriter(wp_no_email_file,fieldnames=wp_no_image_reader.fieldnames)
                        mwriter.writerow(row)
                        logging.info(f'no email')
    
def send_email(email, subject, body):
    """ Send an email """
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = cfg.WP_EMAIL_FROM
    msg['To'] = email
    msg.attach(MIMEText(body))

    try:
        server = smtplib.SMTP_SSL(cfg.WP_EMAIL_SERVER, cfg.WP_EMAIL_PORT)
        server.ehlo()
        server.login(cfg.WP_EMAIL_USERNAME, cfg.WP_EMAIL_PASSWORD)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.close()
        print("mail sent")
    except:
        print("issue")

def main():
    PeopleFixer.startup()

if __name__ == "__main__":
    main()