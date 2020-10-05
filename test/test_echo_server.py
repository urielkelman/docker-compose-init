import os

os.system("docker build -f ./Dockerfile -t \"test:latest\" .")
output = os.popen("docker run --network docker-compose-init_testing_net test:latest").readline().rstrip()

if output == "Your Message has been received: b\'test message\'":
    print("TEST OK")
else:
    print("ERROR")
