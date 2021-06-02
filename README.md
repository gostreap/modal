# Modal

In this project, we would like to use global graphs to confront the different areas of linguistics that include phonetics, structure, syntax, grammar... We have adopted the following steps to approach this problem :
- **Define a metric distance** for the study of our data set.
- **Extract data from three databases**, PHOIBLE, Glottolog and WALS, containing information about thousands of languages.Combine both databases to confront different areas of linguistics.
- **Build a graph containing phonetic**, structural and syntactical information using Neo4J.
- **Visualise the data** and validate our model using Gephi.
- **Study the correlation between language and international trade**.

For this project, we used a GitHub repository to work together on the different tasks. All the files created and used will be present in the different subfolders of the modal folder. We have five subfolders : **data, plot, src, papers, and rapport**.  

The **data** subfolder contains all the .csv, .tab, .json and other files we created, imported or extracted in the project. Appropriate subsubfolders have been created according to each part of the project. 

The **plot** subfolder contains all the .jpg, .pdf, .png and other files we created or produced with Gephi, python or R in the project. Appropriate subsubfolders have been created according to each part of the project.  

The **papers** subfolder contains some of the research papers and articles we used to understand the theoretical background of the project. For instance, we included the portuguese study on correlation between international trade with Portugal and linguistic proximity or the thesis of Moran, one of the creators of the PHOIBLE repository.

The **rapport-soutenance** subfolder contains some images and files we used to write this report.  

The **src** subfolder contains the python source files .py and r files .r which we used for every part of the project. neo4j\_old.py represents our first approach at building the Neo4J graph. neo4j.py represents our second approach at building the Neo4J graph. wals.py is a very important python file containing the most important functions of the project : our proposed metric distance is the distance function `dist`, the functions that allow us to display data on Gephi as well as model, filter and query our data.