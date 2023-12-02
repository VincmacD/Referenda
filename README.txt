# Referenda

## Description:

Referenda is an online web-based application for voting on referendums that the goverment of Canada would theoretically publish on the website.

## Installation

1.	You can download the source code on my personal GitHub repository by using this command:
	git clone https://github.com/VincmacD/referenda.git

2.	Once the folder is downloaded, open it up as a new project in Visual Studio Code or any other IDE.

3.	You must have python & Django downloaded on your computer and have it run in your virtual environment 

4.	Once everything is set, use a terminal in your IDE and type in "python manage.py runserver". If successfull,
	the terminal will display the port to which the program is running one. If you used default settings,
	it should be "http://127.0.0.1:8000/".

5.	If you want an admin user, you must create one in the terminal using this command:
	"python manage.py createsuperuser"

## Usage

1.	Register an Account: this account will count as a voter. Once you set a username, email address
	and a password, you will receive an e-mail verification link to activate your account. Once activated
	you will be able to login

2.	Logging in: Enter your credentials to access the website.

3.	Dashboard: Here you will see the list of all created referendums. Each referendum will have a vote button 
	and a view results button. You will also be able to see if the referendum is available or not unavailable for
	voting. This is determined by the starting date and the expiry date for voting on a referendum.

4.	Voting: If you desire to vote on a available referendum, click on the vote button to navigate towards the referendum's voting page.
	Here you will see information about the referendum including the question asked. Below you will have the option to choose between "yes"
	or "no". Click on one of the choices and cast your vote!

5.	Results: After voting, you will be redirected to the dashboard where you may choose to click of the view results button on the referendum 
	you just voted on. Here you will be able to see the voting statistics of the referendum as-well as a lovely pie-chart on the results so 
	far.

6.	Account: If you click on "Account" on the navbar, you will be redirected to your voter's account page, where you can update your personal 
	information.

7.	Create: Only for admins. Here you can create new referendums for voters to vote on.
 
## Contact Information for Support

Email:	macdonnell.vincent@gmail.com

	