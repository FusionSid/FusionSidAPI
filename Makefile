# I know this is probably not how you're supposed to use a Makefile 
# But im lazy to type out these commands so I'm doing this

# Also i wrote this for another api and now im just copy pasting my own code 

# Run the API
run:
	@cd api; python3 main.py

# delete all those trash files because even though they are ignored by git IT ANNOYS ME SO MUCH
clean:
	@find . | grep -E '(__pycache__|\.pyc|\.pyo$|\.DS_Store)' | xargs rm -rf


# Format all the files
format:
	@black ./