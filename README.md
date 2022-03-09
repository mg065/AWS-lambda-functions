# AWS-lambda-function-csv-to-rds
How to utilize the features of AWS sever-less lambda functions.

# steps(For pandas) on the local machine
- Download the pandas wheel file from PyPI website with python version 3.8 wrt the server machine.
- Download the pytz wheel file from PyPI website with python version 3.8 wrt the server machine.
- Unpack both wheel files by the command (wheel unpack <file name>).
- Copy both file contents into a separate folder i.e: (python).
- Zip the folder by using the command (zip -r <file_name.zip> python).

  
# steps(For NumPy)
- We added a SciPy latest layer offered by AWS from the AWS layers section.  

step(For psycopg2)
- We added an ARN layer for psycopg2 with respect to our region from Specify an ARN section.
link: https://github.com/jetbridge/psycopg2-lambda-layer
  
