from modules.pii_generators.person_pii_generator import PersonGenerator
from modules.pii_generators.diy_pii_generator import DIYPIIGenerator
from loguru import logger
import re
import random

SAMPLE_TEMPLATE = """CERTIFICATE OF NATURALIZATION
Personal description of holder as of date of naturalization:
Date of birth: {DateOfBirth}
Sex: {Sex}
Height: [$$int(4,7)$$] feet [$$int(0,11)$$] inches
Marital status: [$$list('Married', 'Single')$$]
Country of former nationality: {Country}
USCIS Registration No. [$$prompt()$$] or {GeneralIDs}
I certify that the description given is true, and that the photograph affixed hereto is a likeness of me:
{FullName}
Be it known that, pursuant to an application filed with the Secretary of Homeland Security
at: {City}, {State}
The Secretary having found that:
{FullName}
Residing at:
{City}{State}
having complied in all respect with all of the applicable provisions of the naturalization laws of the United States, and having taken the oath of allegiance at a ceremony conducted by
US Citizenship And Immigration Services
at: {City}{State} on: {Date}
such person is admitted as a citizen of the United States of America"""
# SAMPLE_TEMPLATE = """Are you a citizen of the United States of America? [$$list('yes', 'no')$$]
# Will you be 18 years old on or before election day? [$$list('yes', 'no')$$]
# If you checked "No" in response to either of these questions, do not complete form.
# [$$list('Mr.', 'Miss', 'Mrs.', 'Ms.')$$] Last Name {LastName} First Name {FirstName} Middle Name(s) [$$prompt(mdnm)$$] [$$list('Jr', 'Sr', 'II', 'III', 'IV')$$]
# Home Address {Address} Apt. Or Lot # [$$prompt()$$] City/Town {City} State {State} Zip Code {ZipCode}
# Address Where You Get Your Mail If Different From Above {Address} City/Town {City} State {State} Zip Code {ZipCode}
# Date of Birth {DateOfBirth}
# Telephone Number (optional) {PhoneNumber}
# ID Number - (See item 6 in the instructions for your state) {GeneralIDs}
# Choice of Party (see item 7 in the instructions for your State) [$$list('Republican', 'Democratic', 'The Green', 'Libertarians', 'Constitution', 'Natural Law')$$]
# Race or Ethnic Group (see item 8 in the instructions for your State) [$$list('White', 'Hispanic or Latino', 'Black', 'Asian', 'Native American', 'Pacific Islander')$$]
# I have reviewed my state's instructions and I swear/affirm that:
# I am a United States citizen
# I meet the eligibility requirements of my state and subscribe to any oath required
# The information I have provided is true to the best of my knowledge under penalty of perjury. If I have provided false information, I may be fined, imprisoned, or (if not a U.S. citizen) deported from or refused entry to the United States. {FullName} Date: {Date}"""
#
# SAMPLE_TEMPLATE = """Incident investigation report
# This template is provided for example purposes. If you choose to use this template, make sure you customize it to your work and work site.Date and time of incident: {Date} [$$prompt('hour', 'minute')$$] [$$list('AM', 'PM')$$]
# Incident location: {Address}
# Date the incident was reported to OHS: <Indicate if not applicable> {Date}
# Other parties involved in the incident: <Indicate if not applicable> [$$prompt('person(s)')$$]
# Incident category: <Choose all that apply. Refer to Section 33 of the OHS Act for specifics.> [$$list('fatality', 'hospitalization', 'crane/derrick/hoist collapse', 'unplanned fire/explosion/flood', 'collapse/failure of structure or building', 'mine or mine site incidnet (Section 544 of the OHS Code)', 'radiation overexposure', 'potentially serious incident', 'other [$$prompt('electricity, asbestos')$$]]
# Circumstances of injury, illness, incident or worker exposure<Follow the prompts below to describe the circumstances of the incident. Add or delete sections as needed. Do not include personal information (e.g., names, job titles, details of injury or illness) unless it is necessary and permitted by privacy law.>)Sequence of events <List what happened, in chronological order. Include visual aids such as sketches or diagrams if those help describe the incident.>
# [$$prompt('Event 1 occurred')$$]
# [$$prompt('Event 2 was induced')$$]
# [$$prompt('Event 3 was the result')$$]
# Work activities <Describe how many people were involved and in what capacity: for example, Worker One was doing task A; Worker Two was doing task B; Supervisor was doing task C.>
# [$$prompt('Person 1 did thing A')$$]
# [$$prompt('Person 2 did thing B)$$]
# [$$prompt('Person 3 was doing thing C)$$]
# Tools, materials, equipment <Include any relevant information: for example, condition, maintenance history, date last used, manufacturer’s specifications, safeguards, personal protective equipment.>
# [$$prompt('Warranty A expired)$$]
# [$$prompt('Product B expired')$$]
# [$$prompt('Safeguard was not maintained')$$]
# Work site conditions <Describe relevant conditions: for example, weather, harmful substances in use, noise, lighting, time of day, confined/restricted space, ergonomics.>
# [$$prompt('The humidity was high')$$]
# [$$prompt('The time was xx:xx pm')$$]
# [$$prompt('The environment was dark')$$]
# Organizational factors <Describe relevant systemic factors, such as communication methods, training for work site activities, safe work procedures, hazard assessment and control, supervisory requirements. >
# [$$prompt('Walkie-talkies')$$]
# [$$prompt('Safety cones were not in place')$$]
# [$$prompt('Workers are required to shut off machinery before leaving site')$$]
# Other circumstances <Describe any other circumstances relevant to the incident.>
# [$$prompt('Person A was ill')$$]
# [$$prompt('Person B is half blind)$$]
# [$$prompt('Previous reports on xxx has been filed in the past)$$]
# Circumstances: <List each identified circumstance that contributed to the incident. One per row. Add or delete rows as needed.> [$$prompt('Previous prompt A')$$]
# Corrective action required: <List each identified circumstance that contributed to the incident. One per row. Add or delete rows as needed.> [$$prompt('Previous prompt A')$$]
# Assigned to (position): [$$prompt('Site supervisor')$$]
# Date completed: {Date}
# Date report completed: {Date}
# Date report provided to health and safety committee/representative/workers: <Indicate if not applicable.> {Date}"""
#
# SAMPLE_TEMPLATE = """{FullName}
# {Address}
# {City}{State}{ZipCode}
# {Date}
# [$$prompt(Custodian of Records/U.S. Army Corps of Engineers)$$]
# [$$prompt(Records Supervisor)$$]
# [$$prompt(CompanyName/Grained.AI)$$]
# {StreetName}{StreetNumber}
# {City}{State}{ZipCode}
# Dear [$$prompt(Custodian of Records/U.S. Army Corps of Engineers)$$]:
# Under the Alabama Open Records Law § 36-12-40 et seq., I am requesting an opportunity to inspect or obtain copies of public records that [$$prompt(related to the meeting minutes and agendas of the Montgomery City Council for all meetings held between January 1, 2024, and December 31, 2024. Specifically, I am seeking records that detail discussions or decisions regarding city zoning changes, infrastructure projects, or budget allocations for public works.)$$]
# If there are any fees for searching or copying these records, please inform me if the cost will exceed $[$$int(0, 10000)$$].  However, I would also like to request a waiver of all fees in that the disclosure of the requested information is in the public interest and will contribute significantly to the public’s understanding of [$$prompt(Here, you can identify yourself as a representative of the news media if applicable and state that your request is related to news gathering purposes / how municipal infrastructure funding decisions are made and their impact on community development. This request is related to news gathering purposes as part of an investigative report for a local news publication to inform residents about transparency and accountability in government spending.)$$] This information is not being sought for commercial purposes.
# The statute requires a response in a reasonable time period.  If access to the records I am requesting will take longer, please contact me with information about when I might expect copies or the ability to inspect the requested records.
# If you deny any or all of this request, please cite each specific exemption you feel justifies the refusal to release the information and notify me of the appeal procedures available to me under the law.
# Thank you for considering my request.
# Sincerely,
# {FullName}
# {PhoneNumber}"""
#
# SAMPLE_TEMPLATE = """No. A[$$prompt(1234567)$$]
# CERTIFICATE OF CITIZENSHIP
# Personal description of holder as of date of issuance of this certificate.
# Sex: [$$list('male', 'female')$$]
# Height: [$$int(1, 8)$$] feet [$$int(0, 11)$$] inches
# Marital Status: [$$list('married', 'not married')$$]
# Country of birth: [$$prompt(China)$$]
# I certify that the description above given is true, and that the photograph affixed hereto is a likeness of me
#
# Be it known that: {FullName} now residing at {Address} having applied to the Director of U.S. Citizenship and Immigration Services for a certificate of citizenship pursuant to Section 341 of the Immigration and Nationality Act, having proved to the satisfaction of the Director, that (s)he is now a citizen of the United States of America, became a citizen thereof on {Date} and is now in the United States.
# Now Therefore, in pursuance of the authority contained in Section 341 of the Immigration and Nationality Act, this certificate of citizenship is issued this [$$list('1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st', '22nd', '23rd', '24th', '25th', '26th', '27th', '28th', '29th', '30th', '31st')$$] day of [$$list('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')$$] and the seal of the Department of Homeland Security affixed pursuant to statute 8 U.S.C § 1449
# {FullName_2}"""

class SampleGeneration:
    def __init__(self):
        pass

    def validate_sample(self, template_body):
        person_ins = PersonGenerator()
        # Step 1: Extract direct placeholders in the form of {FirstName}, {FullName}, etc.
        direct_placeholders = re.findall(r'\{(.*?)\}', template_body)

        # Step 2: Extract method-call style placeholders in the form of [$$<method_name>(params)$$]
        method_placeholders = re.findall(r'\[\$\$(.*?)\$\$\]', template_body)

        # Step 3: Check if each direct placeholder has a corresponding generator in PIIGenerator enum
        missing_placeholders = []
        for placeholder in direct_placeholders:
            if not hasattr(person_ins, placeholder.split('_')[0]):
                missing_placeholders.append(placeholder)

        # Step 4: Check if each method placeholder has a corresponding method_name> method
        for method in method_placeholders:
            method_name = method.split('(')[0]  # Get the method name before the parentheses
            if not hasattr(DIYPIIGenerator, method_name.upper()):
                missing_placeholders.append(f"[${{method}}] method missing: {method}")

        # Raise an error if there are missing placeholders or methods
        if missing_placeholders:
            raise ValueError(f"Missing placeholders or methods: {', '.join(missing_placeholders)}")
        else:
            logger.success("All placeholders and methods are valid.")

    def generate_sample_by_template(self, template_body):
        # Extract placeholders with optional underscores for multiple people
        direct_placeholders = re.findall(r'\{(\w+?)(?:_(\d+))?\}', template_body)
        method_placeholders = re.findall(r'\[\$\$(.*?)\$\$\]', template_body)

        # Determine the number of distinct PersonGenerator instances needed
        person_mapping = {}
        for placeholder, index in direct_placeholders:
            if index not in person_mapping:
                person_mapping[index] = PersonGenerator()

        # Prepare mappings for direct placeholders
        sample_data = {}
        for placeholder, index in direct_placeholders:
            person_instance = person_mapping[index]  # Use the correct person instance
            if hasattr(person_instance, placeholder):
                sample_data[f"{placeholder}_{index}" if index else placeholder] = getattr(person_instance,
                                                                                          placeholder)

        # Replace method placeholders with generated values
        for method in method_placeholders:
            if method.startswith('int'):
                match = re.match(r'int\((\d+),\s*(\d+)\)', method)
                if match:
                    min_val, max_val = map(int, match.groups())
                    generator = DIYPIIGenerator(DIYPIIGenerator.INT)
                    sample_data[method] = generator.generate(min_val, max_val)

            elif method.startswith('list'):
                match = re.match(r'list\((.*?)\)', method)
                if match:
                    options = list(eval(match.group(1)))
                    generator = DIYPIIGenerator(DIYPIIGenerator.LIST)
                    sample_data[method] = generator.generate(options)

            elif method.startswith('prompt'):
                match = re.match(r'prompt\((.*?)\)', method)
                if match:
                    prompt = match.group(1)
                    generator = DIYPIIGenerator(DIYPIIGenerator.PROMPT)
                    sample_data[method] = generator.generate(prompt)

        # Replace all placeholders in the template
        filled_template = template_body
        for placeholder, value in sample_data.items():
            filled_template = filled_template.replace(f'{{{placeholder}}}', str(value))
            filled_template = filled_template.replace(f'[$${placeholder}$$]', str(value))

        return filled_template


if __name__ == "__main__":
    ins = SampleGeneration()
    ins.validate_sample(SAMPLE_TEMPLATE)
    filled_sample = ins.generate_sample_by_template(SAMPLE_TEMPLATE)
    print("Generated Sample:")
    print(filled_sample)
