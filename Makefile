test:
	python -m unittest discover
run: 
	./main.py
clean:
	- rm output -rf
	- rm tmp -rf
	- rm *.pyc
	- mongo domain   --eval "db.dropDatabase()"
	- mongo ip       --eval "db.dropDatabase()"
	- mongo alert    --eval "db.dropDatabase()"
	- mongo newdomain --eval "db.dropDatabase()"
emulate:
	cp data/queries.log data/queries2.log
