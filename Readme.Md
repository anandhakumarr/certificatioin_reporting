Install Python 

	https://www.digitalocean.com/community/tutorials/install-python-windows-10

	RUN `python --version` To confirm the installation

Install Pip
	
	Step 1: Download the get-pip.py (https://bootstrap.pypa.io/get-pip.py) file and store it in the same directory as python is installed.

	RUN `python get-pip.py`

	RUN `pip --version` To confirm the installation 

Install Dependent Libraries

	Go to Command Prompt 

	Use `cd` to change the current directory to Project directory 

	RUN `pip install -r requirements.txt` or RUN `pip install -r /path/to/requirements.txt`

To Run the Application 

	From the Command Prompt 

	Go to Project Directory 

	RUN `python app.py`

	Which will send you the url example: * Running on http://127.0.0.1:5000

	Open Browser and RUN this URL - http://127.0.0.1:5000

Refferene Data
	
	Certification Cateogries = data/category.csv
	Employee Data = data/employee_ref.csv
	List of Certifications = data/list_of_certifications.csv
	List of Trainings = data/list_of_trainings.csv
	Training Category = data/training_category.csv
	Logins = data/users.csv

Submitted Data

	Certifications = data/certification.csv
	Trainings = data/training.csv

To download certification and trainings use below path

	http://127.0.0.1:5000/download/certification

	http://127.0.0.1:5000/download/training

	Note: Change IP address once deployed in server


