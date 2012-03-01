test:
	python -m unittest discover
run: 
	./analysis.py
clean:
	rm output -rf
	rm tmp -rf
	rm *.pyc
	mongo domain --eval "db.dropDatabase()"
	mongo ip --eval "db.dropDatabase()"
