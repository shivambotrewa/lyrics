import docker

def build_and_run_docker():
    client = docker.from_env()

    dockerfile = """
    # Use a base image that supports systemd, for example, Ubuntu
    FROM ubuntu:20.04

    # Install necessary packages
    RUN apt-get update && \\
    apt-get install -y shellinabox && \\
    apt-get install -y systemd && \\
    apt-get clean && \\
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
    RUN echo 'root:root' | chpasswd
    # Expose the web-based terminal port
    EXPOSE 4200

    # Start shellinabox
    CMD ["/usr/bin/shellinaboxd", "-t", "-s", "/:LOGIN"]
    """

    # Build the Docker image
    image, build_logs = client.images.build(fileobj=io.BytesIO(dockerfile.encode('utf-8')), tag='shellinabox:latest', rm=True)

    # Run the Docker container
    container = client.containers.run(
        image='shellinabox:latest',
        ports={'4200/tcp': 4200},
        detach=True
    )

    print(f"Container {container.short_id} is running. Access it at http://localhost:4200")

if __name__ == "__main__":
    build_and_run_docker()
