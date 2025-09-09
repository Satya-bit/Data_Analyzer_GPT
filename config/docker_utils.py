from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
import asyncio
from config.constants import *

def getDockerCommandLineExecutor():
    docker=DockerCommandLineCodeExecutor(
        work_dir=WORK_DIR_DOCKER,
        timeout=TIMEOUT_DOCKER
    )
    return docker

async def start_docker_container(docker):
    print("Starting Docker container...")
    await docker.start()
    print("Docker container started.")
    
async def stop_docker_container(docker):
    print("Stopping Docker container...")
    await docker.stop()
    print("Docker container stopped.")