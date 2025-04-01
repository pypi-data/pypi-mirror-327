import argparse
import os
import sys
import subprocess
import requests
from langchain_cli.cli import serve
from app.utils.langchain_validation_util import validate_langchain_vars
from collections import OrderedDict
from importlib.metadata import version, PackageNotFoundError


def parse_arguments():
    """
    Parse command-line arguments for the CodeForgeAI application.

    @return: An argparse.Namespace object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Run CodeForgeAI with custom options")
    parser.add_argument("--exclude", default=[], type=lambda x: x.split(','),
                        help="List of files or directories to exclude (e.g., --exclude 'tst,build,*.py')")
    parser.add_argument("--profile", type=str, default=None,
                        help="AWS profile to use (e.g., --profile codeforgeai)")
    parser.add_argument("--model", type=str, choices=["sonnet", "sonnet3.5", "sonnet3.5-v2", "haiku", "opus"],
                        default="sonnet3.5-v2",
                        help="AWS Bedrock Model to use (e.g., --model sonnet)")
    parser.add_argument("--port", type=int, default=8000,
                        help="Port number to run CodeForgeAI frontend on (e.g., --port 8080)")
    parser.add_argument("--version", action="store_true",
                        help="Prints the version of CodeForgeAI")
    parser.add_argument("--skip-update", action="store_true",
                        help="Skip the auto-update check")
    parser.add_argument("--max-depth", type=int, default=15,
                        help="Maximum depth for folder structure traversal (e.g., --max-depth 20)")

    return parser.parse_args()


def setup_environment(args):
    """
    Set up the environment variables based on the parsed arguments.

    @param args: An argparse.Namespace object containing the parsed arguments.
    """
    # Set the current working directory as the user's codebase directory
    os.environ["CODEFORGEAI_USER_CODEBASE_DIR"] = os.getcwd()

    # Set additional excluded directories
    additional_excluded_dirs = ','.join(args.exclude)
    os.environ["CODEFORGEAI_ADDITIONAL_EXCLUDE_DIRS"] = additional_excluded_dirs

    # Set AWS profile if provided
    if args.profile:
        os.environ["CODEFORGEAI_AWS_PROFILE"] = args.profile

    # Set AWS model if provided
    if args.model:
        os.environ["CODEFORGEAI_AWS_MODEL"] = args.model

    # Set maximum depth for folder traversal
    os.environ["CODEFORGEAI_MAX_DEPTH"] = str(args.max_depth)




def start_server(args):
    """
    Start the CodeForgeAI server.

    @param args: An argparse.Namespace object containing the parsed arguments.
    """
    # Change to the directory of the current script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Start the server
    serve(host="0.0.0.0", port=args.port)


def get_version():
    """Get the current version of CodeForgeAI."""
    try:
        return version('codeforge-ai')
    except PackageNotFoundError:
        return "Version information not available"


def main():
    """
    Main function to run the CodeForgeAI application.
    """
    # Parse command-line arguments
    args = parse_arguments()

    # Handle version flag first
    if args.version:
        print(f"CodeForgeAI version {get_version()}")
        sys.exit(0)

    # Validate LangChain variables
    validate_langchain_vars()

    # Set up the environment
    setup_environment(args)

    # Start the server
    start_server(args)


if __name__ == "__main__":
    main()
