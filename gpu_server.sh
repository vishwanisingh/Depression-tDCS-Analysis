# GOTO dir home
jupyter nbconvert --to script average_fun_con.ipynb
sed -i '7s/.*/from common import */' Downloads/IITD/Depression-IITD/average_fun_con.py
sed -i "s/os\.getcwd(), 'Depression-Sample-dataset-AIIMS'/'\/mnt', 'common_scratch', 'Depression-AIIMS'/g" Downloads/IITD/Depression-IITD/average_fun_con.py
# rsync -avz Downloads/IITD/Depression-IITD/average_fun_con.py vishwani_s@10.228.64.95:depression/