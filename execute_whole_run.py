import os
from nbconvert import NotebookExporter

# Define the range of values for RANGE
RANGE_values = range(1, 3)

# Loop over the RANGE values
for i in RANGE_values:
    # Set the RANGE variable as an environment variable
    os.environ['RANGE'] = str(i)
    
    # Convert the notebook to a Python script
    notebook_exporter = NotebookExporter()
    notebook_exporter.from_filename('pre-vs-post.ipynb')
    python_script, _ = notebook_exporter.from_filename('pre-vs-post.ipynb')

    print("FFFFFFFFFFF", python_script, _)

    # Execute the Python script
    exec(python_script)
