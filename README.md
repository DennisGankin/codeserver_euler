# VS Code on euler

Scripts to start vscode server on euler inside a slurm job.  

## How to run?

``python codeserver_starter.py``

The script will connect to euler and start a slurm job based the chosen config file.
Add or adjust config files under ``scripts/``, to control the slurm job parameters. 

Once the slurm job is running, the script tells you which ssh command to run to create a tunnel to the job. 
You can then open up VS Code in your browser. 

The script is not prefect. If there is a problem, ssh into euler and use ``sacct`` or ``squeue`` to figure out if your job is running. 

## Prerequisites

- Locally you will need python with ``paramiko`` installed
- The ``scripts/`` folder needs to contain valid sbatch scripts
- Fill the variables at the beginning of ``codeserver_starter.py`` with your private data
  - your user name
  - your private key (on your local computer), if there is no key par, leave empty
  - path to where scripts will be copied to on euler
- Create a directory on euler that matches the path you entered in ``codeserver_starter.py``

You should be good to go.