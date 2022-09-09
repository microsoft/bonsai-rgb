#!/usr/bin/env python3

import os
import time
import dotenv

from microsoft_bonsai_api.simulator.client import BonsaiClient, BonsaiClientConfig
from microsoft_bonsai_api.simulator.generated.models import (
    SimulatorInterface,
    SimulatorState,
    SimulatorSessionResponse,
)
from sim.simulator_model import SimulatorModel


def env_setup(env_file: str = ".env"):
    """Helper function to setup connection with Project Bonsai

    Returns
    -------
    Tuple
        workspace, and access_key
    """

    load_dotenv(dotenv_path=env_file, verbose=True, override=True)
    workspace = os.getenv("SIM_WORKSPACE")
    access_key = os.getenv("SIM_ACCESS_KEY")

    env_file_exists = os.path.exists(env_file)
    if not env_file_exists:
        open(env_file, "a").close()

    if not all([env_file_exists, workspace]):
        workspace = input("Please enter your workspace id: ")
        set_key(env_file, "SIM_WORKSPACE", workspace)
    if not all([env_file_exists, access_key]):
        access_key = input("Please enter your access key: ")
        set_key(env_file, "SIM_ACCESS_KEY", access_key)

    load_dotenv(dotenv_path=env_file, verbose=True, override=True)
    workspace = os.getenv("SIM_WORKSPACE")
    access_key = os.getenv("SIM_ACCESS_KEY")

    return workspace, access_key


def main():
    """
    Creates a Bonsai simulator session and executes Bonsai episodes.
    """

    # values in `.env`, if they exist, take priority over environment variables
    # looking for SIM_WORKSPACE and SIM_ACCESS_KEY
    dotenv.load_dotenv(".env", verbose=True, override=True)
    workspace = os.getenv("SIM_WORKSPACE")
    access_key = os.getenv("SIM_ACCESS_KEY")

    if workspace is None:
        raise ValueError("The Bonsai workspace ID is not set.")
    if access_key is None:
        raise ValueError("The access key for the Bonsai workspace is not set.")

    config_client = BonsaiClientConfig()
    client = BonsaiClient(config_client)

    registration_info = SimulatorInterface(
        name="color-sim",
        timeout=60,
        simulator_context=config_client.simulator_context,
        description=None,
    )

    print(f"config: {config_client.server}, {config_client.workspace}")
    registered_session: SimulatorSessionResponse = client.session.create(
        workspace_name=config_client.workspace, body=registration_info
    )
    print(f"Registered simulator. {registered_session.session_id}")

    sequence_id = 1
    sim_model = SimulatorModel()
    sim_model_state = {"sim_halted": False}

    try:
        while True:
            sim_state = SimulatorState(
                sequence_id=sequence_id,
                state=sim_model_state,
                halted=sim_model_state.get("sim_halted", False),
            )
            event = client.session.advance(
                workspace_name=config_client.workspace,
                session_id=registered_session.session_id,
                body=sim_state,
            )
            sequence_id = event.sequence_id
            print(f'[{time.strftime("%H:%M:%S")}] Last Event: {event.type}')

            if event.type == "Idle":
                time.sleep(event.idle.callback_time)
            elif event.type == "EpisodeStart":
                print(f"config {event.episode_start.config}")
                sim_model_state = sim_model.reset(event.episode_start.config)
                print(f"state {sim_model_state}")
            elif event.type == "EpisodeStep":
                print(f"action {event.episode_step.action}")
                sim_model_state = sim_model.step(event.episode_step.action)
                print(f"state {sim_model_state}")
            elif event.type == "EpisodeFinish":
                sim_model_state = {"sim_halted": False}
            elif event.type == "Unregister":
                print(
                    f"Simulator Session unregistered by platform because '{event.unregister.details}'"
                )
                return
    except BaseException as err:
        client.session.delete(
            workspace_name=config_client.workspace,
            session_id=registered_session.session_id,
        )
        print(f"Unregistered simulator because {type(err).__name__}: {err}")


if __name__ == "__main__":
    main()
