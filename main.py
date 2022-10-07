from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///companies.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Companies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    address = db.Column(db.String(250), unique=True, nullable=False)
    founder = db.Column(db.String(120), nullable=False)
    capital = db.Column(db.Integer, nullable=False)
    number_of_branches = db.Column(db.Integer, nullable=False)
    email_id = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, name, address, founder, capital, number_of_branches,email_id):
        self.name = name
        self.address = address
        self.founder = founder
        self.capital = capital
        self.number_of_branches = number_of_branches
        self.email_id = email_id



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/addNewCompany', methods=['POST'])
def add_new_company():
    name = request.json['name']
    address = request.json['address']
    founder = request.json['founder']
    capital = request.json['capital']
    number_of_branches = request.json['number_of_branches']
    email_id = request.json['email_id']

    new_company = Companies(name, address, founder, capital,
                            number_of_branches, email_id)

    db.session.add(new_company)
    db.session.commit()
    return jsonify(name=new_company.name,
                   founder=new_company.founder,
                   capital=new_company.capital,
                   email_id=new_company.email_id)


@app.route('/getContactdetails', methods=['POST'])
def get_contact_details():
    content_type = request.headers.get('Content-type')
    if content_type == 'application/json':
        name_required = request.json['name']
        company = Companies.query.filter_by(name = name_required).first()
        return jsonify(name = company.name,
                       email_id = company.email_id,
                       address = company.address)


@app.route('/updateCompanyData', methods=['PUT'])
def update_company_details():
    company_to_update_name = request.json['company-name']
    company_to_update = Companies.query.filter_by(name=company_to_update_name).first()

    address = request.json['address']
    capital = request.json['capital']
    number_of_branches = request.json['number_of_branches']

    company_to_update.address = address
    company_to_update.capital = capital
    company_to_update.number_of_branches = number_of_branches


    db.session.commit()
    return jsonify(name=company_to_update.name,
                   email_id=company_to_update.email_id,
                   update_status = "Done")

@app.route('/delete', methods = ['DELETE'])
def delete():
    company_to_delete_name = request.json['company-name']
    company_to_delete = Companies.query.filter_by(name = company_to_delete_name).first()
    db.session.delete(company_to_delete)
    db.session.commit()
    return f"Successfully deleted {company_to_delete}."




if __name__ == '__main__':
    app.run(debug=True)
