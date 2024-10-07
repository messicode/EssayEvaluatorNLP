How to run:

1) Extract the zipped folder in a directory and navigate in the project folder.

2) Make sure corpora of essays is in a folder named 'essays' and essay details file 'index.csv' is in the same directory as the run_project.py among other.py files.

3) Update the 'input_essay.txt' and put in your input essay. Do the same with 'prompt.txt'.

4) Open terminal (windows cmd) and execute 'py run_project.py'.

5) The program prints the essays individual raw values for sentence length, C1 & C2, C3 type errors, the Cosine sim and the grade of the essay compared to the corpora averages.

6) Examples for unit testing each file are availale at the bottom and can be uncommented to test each file individually.

Note: 
- Check all the dependencies are installed. pip was used to install spacy-"en_core_web_sm"
- Some IDEs might show issues like 'No module named spacy' etc. The libraries were installed using pip in cmd and the code ran in this environment. PLEASE use this environment and not any IDE to seemlessly run the code.