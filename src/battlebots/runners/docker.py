from typing import List
import json

import docker

class DockerRunner:

    class RunnerFailure(Exception): pass

    def __init__(self, *, timeout=5, **kwargs):
        self.client = docker.from_env()
        self.timeout = timeout
        self.kwargs = kwargs

    def run_container(
        self,
        image: str,
        command: List[str],
        game_id: str,
    ):
        container = self.client.containers.run(
            image=image,
            command=command,
            detach=True,
            labels={
                "game_id": game_id
            },
            **self.kwargs,
        )

        try:
            container.wait(timeout=self.timeout)
        except (ReadTimeout, docker.errors.APIError) as e:
            raise RunnerFailure from e
        else:
            container.reload()
            exit_code = container.attrs.get('State', {}).get('ExitCode', -1)
            output = container.logs().strip()
        finally:
            container.reload()
            if container.status != 'exited':
                container.kill()

        if exit_code != 0:
            raise RunnerFailure(f'Bad Exit Code: {exit_code}. Logs: {output}')

        try:
            return json.loads(output)
        except json.JSONDecoder as e:
            raise RunnerFailure from e
