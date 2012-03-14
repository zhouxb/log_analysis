test:
	@ python tests/run_tests.py
run: 
	./log_analysis/main.py
cover:
	coverage run --branch tests/run_tests.py
	coverage html --omit="/usr/*,log_analysis/tests/*"
	google-chrome htmlcov/index.html
clean:
	- rm .coverage
	- rm htmlcov -rf
	- rm output -rf
	- rm tmp -rf
	- rm log_analysis/*.pyc
	- mongo domain   --eval "db.dropDatabase()"
	- mongo ip       --eval "db.dropDatabase()"
	- mongo alert    --eval "db.dropDatabase()"
	- mongo newdomain --eval "db.dropDatabase()"
emulate:
	cp data/queries.log.gz data/queries.log.CMN-CQ-2-375.20120217223800.gz
