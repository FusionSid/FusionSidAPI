# I know this is probably not how you're supposed to use a Makefile 
# But im lazy to type out these commands so I'm doing this

# Run the API
run:
	@cd api; uvicorn main:app --port=443 --host="0.0.0.0" --ssl-certfile cert.pem --ssl-keyfile key.pem
dev:
	@cd api; uvicorn main:app

# delete all those trash files because even though they are ignored by git IT ANNOYS ME SO MUCH
clean:
	@find . | grep -E '(__pycache__|\.pyc|\.pyo$|\.DS_Store)' | xargs rm -rf

# Format all the files
format:
	@black ./
