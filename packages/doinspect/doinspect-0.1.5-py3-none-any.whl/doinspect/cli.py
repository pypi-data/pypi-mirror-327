import argparse

import docker
from doinspect.inspector import (
    inspect_env,
    inspect_network,
    inspect_ports,
    inspect_volumes,
)


def main():
    client = docker.from_env()

    parser = argparse.ArgumentParser(
        description="Container Inspector CLI - Inspect running Docker containers.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "-c",
        "--container",
        required=True,
        metavar="",
        help="container ID or name to inspect",
    )
    parser.add_argument(
        "-e", "--env", action="store_true", help="inspect environment variables"
    )
    parser.add_argument(
        "-n", "--net", action="store_true", help="inspect network usage"
    )
    parser.add_argument(
        "-p", "--ports", action="store_true", help="inspect port mappings"
    )
    parser.add_argument(
        "-v", "--volumes", action="store_true", help="inspect volume mappings"
    )

    parser.epilog = """
Examples:
  cinspect -c my_container           # Show all details of the container
  cinspect -c my_container -e        # Show environment variables
  cinspect -c my_container -n        # Show network usage
  cinspect -c my_container -p        # Show port mappings
  cinspect -c my_container -v        # Show volume mappings
    """

    args = parser.parse_args()
    container_id = args.container

    try:
        container = client.containers.get(container_id)
    except docker.errors.NotFound:
        print("\nError: Container '{}' not found.\n".format(container_id))
        return
    except docker.errors.APIError as e:
        print("\nDocker API Error: {}\n".format(str(e)))
        return

    print(f"\nInspecting Container: {container_id}\n" + "=" * 50)

    # If no specific option is given, show all information
    if not (args.env or args.net or args.ports or args.volumes):
        inspect_env(container_id)
        print("=" * 50)
        inspect_network(container_id)
        print("=" * 50)
        inspect_ports(container_id)
        print("=" * 50)
        inspect_volumes(container_id)
    else:
        if args.env:
            inspect_env(container_id)
        if args.net:
            inspect_network(container_id)
        if args.ports:
            inspect_ports(container_id)
        if args.volumes:
            inspect_volumes(container_id)


if __name__ == "__main__":
    main()
