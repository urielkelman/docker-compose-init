import sys

USAGE_MESSAGE = '''usage: python3 docker_compose_generator -c N
                    Arguments:
                    -c N: N is the number of clients.'''

FILE_NAME = "docker-compose-dev-c.yaml"

INITIAL_SEGMENT_DOCKER_COMPOSE = '''version: \'3\'
services:
  server:
    container_name: server
    image: server:latest
    entrypoint: python3 /main.py
    environment:
      - PYTHONUNBUFFERED=1
      - SERVER_IP=server
      - SERVER_PORT=12345
      - SERVER_LISTEN_BACKLOG=5
    networks:
      - testing_net
      '''

CLIENT_SEGMENT_DOCKER_COMPOSE = '''
    client{}:
        container_name: client{}
        image: client:latest
        entrypoint: /client
        environment:
          - CLI_ID={}
          - CLI_SERVER_ADDRESS=server:12345
          - CLI_LOOP_LAPSE=1m2s
          - CLI_LOOP_PERIOD=10s
        networks:
          - testing_net
        depends_on:
          - server'''

FINAL_SEGMENT_DOCKER_COMPOSE = '''
networks:
  testing_net:
    ipam:
      driver: default
      config:
        - subnet: 172.25.125.0/24'''


def generate_file(number_of_clients):
    with open(FILE_NAME, "w") as docker_compose_file:
        docker_compose_file.write(INITIAL_SEGMENT_DOCKER_COMPOSE)
        for x in range(number_of_clients):
            docker_compose_file.write(CLIENT_SEGMENT_DOCKER_COMPOSE.format(x+1, x+1, x+1))
        docker_compose_file.write(FINAL_SEGMENT_DOCKER_COMPOSE)


def main():
    if sys.argv[1] != "-c" or len(sys.argv) != 3:
        print(USAGE_MESSAGE)
    else:
        try:
            number_of_clients = int(sys.argv[2])
            generate_file(number_of_clients)
        except ValueError:
            print(USAGE_MESSAGE)


if __name__ == "__main__":
    main()
