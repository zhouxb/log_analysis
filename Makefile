test:
	python -m unittest discover
run: 
	./analysis.py
clean:
	rm output -rf
	rm tmp -rf
	rm *.pyc
