from app import app
from flask import render_template, request
from ..bc.businesscentral import BusinessCentral
from ..utils.config import ELATEC_GMBH, ELATEC_SYSTEM_GMBH, SESAMSEC_GMBH, ELATEC_INC

bc = BusinessCentral()

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    company = None
    serial_number = ''
    if request.method == 'POST':
        company = request.form.get('company')
        serial_number = request.form.get('serial_number')
        if company == 'elatec_gmbh':
            data = bc.find_my_device("Elatec_GE_Prod", ELATEC_GMBH, serial_number)
        if company == 'elatec_system_gmbh':
            data = bc.find_my_device("Elatec_GE_Prod", ELATEC_SYSTEM_GMBH, serial_number)
        if company == 'sesamsec_gmbh':
            data = bc.find_my_device("Elatec_GE_Prod", SESAMSEC_GMBH, serial_number)
        if company == 'elatec_inc':
            data = bc.find_my_device("Elatec_US_Prod", ELATEC_INC, serial_number)
    return render_template('index.html', selected_company=company, serial_number=serial_number, data=data)
