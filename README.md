# Introduction 
This is the repository for the source code of the paper *A computational cognitive modeling framework for care pathways representation and its operational use in primary health care*.

# Prerequisites
To use and explore the framework (as described in the paper), you should have Python installed in your computer. The Anaconda distribution is strongly recomended (you can download it through this [link](https://www.anaconda.com/download)).

You can also run the source code using Docker. If you are familiarized with containers, this certainly will be easier for you.

# Build and Test
You can just download the source code by clicking in the `<> Code` button, above, and then click in the `Download ZIP` option. If you are familiarized with Git, you can simply clone this repository, naturally.

To run the source code, just navigate to the folder with the file `app.py` and execute the command `python app.py`, using the command prompt of your operational system. For this step properlly work, make sure that Python is accessible in your PATH.

The system should be running at `http://127.0.0.1:5000`. For upload a LDT, open the URL `http://127.0.0.1:5000/treeuploader` in your web browser. After running it, you can use a software like [postman](https://www.postman.com/downloads/) to test the system and the LTD created. A templete for creating a LDT is available in the folder `scripts` (this is the PC for Obesity, from the Brazilian National Health Ministry, as described in the paper).

# Load test

The folder `locust` contains the parametrization file and the outputs for the load test (as described in the paper). Also, we data analysis is provided in a proper Jupyter Notebook, in the same folder.

# Empirical analysis

The data employed for the empirical assessment of our system, in a real-world operational context, is available in the folder `empirical_analysis`. Both data (a .CSV file) and statistical analysis (Jupyter Notebook) are available is this folder.

# Contribute
Please, feel free to contribute with this project!
