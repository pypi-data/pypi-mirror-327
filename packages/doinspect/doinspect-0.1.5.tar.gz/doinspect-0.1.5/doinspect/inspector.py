import os
import platform

import docker

# Ensure DOCKER_HOST is set if not already set in the environment
if "DOCKER_HOST" not in os.environ:
    if platform.system() == "Windows":
        os.environ["DOCKER_HOST"] = "tcp://localhost:2375"
    else:
        os.environ["DOCKER_HOST"] = "unix:///var/run/docker.sock"

# Now initialize the Docker client with the appropriate docker_host
client = docker.DockerClient(base_url=os.environ["DOCKER_HOST"])


def inspect_env(container_id):
    """Fetch and display environment variables of a running container."""
    try:
        container = client.containers.get(container_id)
        env_vars = container.attrs["Config"]["Env"]

        print(f"Environment variables for container '{container_id}':\n")
        for env in env_vars:
            print(f"  {env}")

    except docker.errors.NotFound:
        print(f"Error: Container '{container_id}' not found.")
    except docker.errors.APIError as e:
        print(f"Error: Docker API error - {e}")


def inspect_network(container_id):
    """Retrieve network information of a running container."""
    try:
        container = client.containers.get(container_id)
        network_settings = container.attrs["NetworkSettings"]

        # Display IP Addresses
        print(f"Network Information for container '{container_id}':\n")
        for net_name, net_data in network_settings["Networks"].items():
            print(f"  Network: {net_name}")
            print(f"    IP Address: {net_data['IPAddress']}")
            print(f"    Gateway: {net_data['Gateway']}\n")

        # Display Network Statistics
        stats = container.stats(stream=False)
        net_stats = stats["networks"]

        print("  Network Usage (bytes):")
        for iface, data in net_stats.items():
            print(f"    Interface: {iface}")
            print(f"      Bytes Sent: {data['tx_bytes']}")
            print(f"      Bytes Received: {data['rx_bytes']}")

    except docker.errors.NotFound:
        print(f"Error: Container '{container_id}' not found.")
    except docker.errors.APIError as e:
        print(f"Error: Docker API error - {e}")


def inspect_ports(container_id):
    """Retrieve port mappings of a running container."""
    try:
        container = client.containers.get(container_id)
        ports = container.attrs["NetworkSettings"]["Ports"]

        if not ports:
            print(f"No port mappings found for container '{container_id}'.")
            return

        print(f"Port Mappings for container '{container_id}':\n")
        for container_port, bindings in ports.items():
            if bindings:
                for binding in bindings:
                    host_ip = binding.get("HostIp", "0.0.0.0")
                    host_port = binding.get("HostPort", "N/A")
                    print(f"  {host_ip}:{host_port} -> Container Port {container_port}")
            else:
                print(f"  Container Port {container_port} is exposed but not mapped.")

    except docker.errors.NotFound:
        print(f"Error: Container '{container_id}' not found.")
    except docker.errors.APIError as e:
        print(f"Error: Docker API error - {e}")


def inspect_volumes(container_id):
    """Retrieve volume mappings of a running container."""
    try:
        container = client.containers.get(container_id)
        mounts = container.attrs["Mounts"]

        if not mounts:
            print(f"No volume mappings found for container '{container_id}'.")
            return

        print(f"Volume Mappings for container '{container_id}':\n")
        for mount in mounts:
            print(
                f"  Host: {mount['Source']} -> Container: {mount['Destination']} ({mount['Type']})"
            )

    except docker.errors.NotFound:
        print(f"Error: Container '{container_id}' not found.")
    except docker.errors.APIError as e:
        print(f"Error: Docker API error - {e}")
