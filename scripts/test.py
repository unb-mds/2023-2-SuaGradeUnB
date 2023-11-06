import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--clean', action='store_true')

args = parser.parse_args()

try:
    command = "sudo docker exec django-api coverage run manage.py test".split()
    subprocess.run(command)
    command = "sudo docker exec django-api coverage report -m".split()
    subprocess.run(command)

    if args.clean:
        subprocess.run(['make', 'cleanup'])
except Exception as e:
    print(e)
