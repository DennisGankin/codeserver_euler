# connect to server via ssh
# run sbatch script to start code server
# read out the node where job was started from squeue
# connect to node via ssh creating a tunnel
# output a link to the code server

import paramiko
from getpass import getpass
import logging
import time
import os

# Set up logging
logging.basicConfig(level=logging.INFO)


def main():
    
    #################### enter private data here #########################

    # path to private key locally, leave empty if there is no key pair
    private_key_path = '' #'/Users/bestuser/.ssh/id_ed25519_euler' 
    username = 'greatuser' # username on euler
    # path to sbatch script on euler, file will be copied there, create directory beforehand to make sure it exists
    remote_sbatch_script_path = '/make_sure_folder_exists/software/code_server/start_vc_server_tmp.sh'
    # hostname of the server, you can use an alias if there is one in your ssh config file
    hostname = 'euler.ethz.ch' 

    ######################################################################


    # List all bash scripts in the local directory
    local_script_directory = 'scripts'
    bash_scripts = [f for f in os.listdir(local_script_directory) if f.endswith('.sh')]
    if not bash_scripts:
        logging.error('No bash scripts found in the directory.')
        exit()

    # Prompt the user to choose a script
    print("Available bash scripts:")
    for i, script in enumerate(bash_scripts, start=1):
        print(f"{i}. {script}")
    script_choice = int(input("Enter the number of the script you want to upload and execute: ")) - 1
    if script_choice < 0 or script_choice >= len(bash_scripts):
        logging.error('Invalid script choice.')
        exit()

    chosen_script = bash_scripts[script_choice]
    logging.info(f'Chosen script: {chosen_script}')
    local_sbatch_script_path = os.path.join(local_script_directory, chosen_script)

    # Create a new SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if private_key_path:  # Check if the private key path is provided
        try:
            key_passphrase = getpass('Enter your key password: ')
            private_key = paramiko.Ed25519Key.from_private_key_file(private_key_path, password=key_passphrase)
            ssh.connect(hostname, username=username, pkey=private_key)
            logging.info('Successfully connected to the server using private key.')
        except Exception as e:
            logging.error('Failed to connect to the server with private key.')
            logging.error(e)
            try:
                ssh.close()
            except Exception as e:
                pass
            exit()
    else:  # If no private key, attempt connection without it
        try:
            ssh.connect(hostname, username=username, password=getpass('Enter your password: '))
            logging.info('Successfully connected to the server with a password.')
        except Exception as e:
            logging.error(e)
            logging.error('Failed to connect to the server with password. Maybe wrong password?')
            try:
                ssh.close()
            except Exception as e:
                pass
            exit()


    # Upload the chosen sbatch script

    sftp = ssh.open_sftp()
    try:
        sftp.put(local_sbatch_script_path, remote_sbatch_script_path)
        logging.info('Successfully uploaded the sbatch script.')
    except Exception as e:
        logging.error('Failed to upload the sbatch script.')
        logging.error(e)
        
    finally:
        sftp.close()

    # Run the sbatch script to start the code server
    try:
        stdin, stdout, stderr = ssh.exec_command(f'sbatch {remote_sbatch_script_path}')
        logging.info('Successfully submitted the slurm job.')
    except Exception as e:
        logging.error('Failed to submit to slurm.')
        logging.error(e)
        logging.error('Output from sbatch: ' + stdout.readlines())
        
    # Read out the node where job was started from squeue
    try:
        # wait until job appears in squeue
        while True:
            stdin, stdout, stderr = ssh.exec_command('squeue -u $USER')
            output = stdout.readlines()
            if len(output) > 1: # only if job has been added to squeue (right now assuming no previous job was running)
                node = output[1].split()[7]  # Assuming the node is in the 8th column
                if "(" in node:  # Only break if a node has been assigned
                    logging.info('Node not assigned yet:' + node)
                else:
                    logging.info('Successfully read the node from squeue: ' + node)
                    break
            else:
                time.sleep(10)  # Wait for 5 seconds before checking again
    except Exception as e:
        logging.error('Failed to read the node from squeue.')
        logging.error(e)
        logging.error('Output from squeue: ' + str(output))

    # Connect to the node via SSH creating a tunnel
    local_port = '59123'
    remote_port = '8898'
    #try:
    #    ssh.exec_command(f'ssh -L {local_port}:{node}:{remote_port} {username}@{hostname} -N')
    #    logging.info('Successfully created the SSH tunnel.')
    #    logging.info(f'Used command: ssh -L {local_port}:{node}:{remote_port} {username}@{hostname} -N')
    #except Exception as e:
    #    logging.error('Failed to create the SSH tunnel.')
    #    logging.error(e)

    logging.info(f'Use command: ssh -L {local_port}:{node}:{remote_port} {username}@{hostname} -N')

    # Output a link to the code server
    print(f'Connect to: http://localhost:{local_port} afterwards')

    # Wait for user input to close the SSH connection
    #input("Press enter to close the SSH connection...")
    try: 
        ssh.close()
        logging.info('SSH connection closed.')
    except Exception as e:
        pass


if __name__ == '__main__':
    main()