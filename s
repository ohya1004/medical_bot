git add .
git commit -m "Add code"
git push -f heroku master
heroku logs --tail --app ncku-medical-project
