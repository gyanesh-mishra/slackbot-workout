#!make

rebuild: build | run

build:
	@echo "+\n++ Performing local docker build ...\n+"
	@docker build -t freshworkout .

run:
	@echo "+\n++ Running local docker build ...\n+"
	@docker run -p 5000:5000 freshworkout

