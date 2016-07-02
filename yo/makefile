backup:
	python manage.py dumpdata budget > budget/management/commands/budget-data-backup.json.txt
	python manage.py budget_backup
	rm -rf budget/management/commands/budget-data-backup.json.txt
    
server:
	python manage.py runserver
    
user:
	python manage.py loaddata project/fixtures/users_testdata.json