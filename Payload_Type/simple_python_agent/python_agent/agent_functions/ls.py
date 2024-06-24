from mythic_container.MythicCommandBase import *
import json
from mythic_container.MythicRPC import *
import sys


class LsArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            CommandParameter(
                name="path",
                type=ParameterType.String,
                default_value=".",
                parameter_group_info=[ParameterGroupInfo(
                    required=False
                )],
                description="Path of file or folder on the current system to list",
            )
        ]

    async def parse_arguments(self):
        self.add_arg("path", self.command_line)

    async def parse_dictionary(self, dictionary_arguments):
        self.load_args_from_dictionary(dictionary_arguments)


class LsCommand(CommandBase):
    cmd = "ls"
    needs_admin = False
    help_cmd = "ls [/path/to/file]"
    description = "Get attributes about a file / a folder."
    version = 1
    author = "@maximedelis"
    attackmapping = ["T1083"]
    supported_ui_features = ["file_browser:list"]
    is_file_browse = True
    argument_class = LsArguments
    browser_script = BrowserScript(script_name="ls", author="@maximedelis", for_new_ui=True)
    attributes = CommandAttributes(
        supported_os=[SupportedOS.MacOS, SupportedOS.Linux, SupportedOS.Windows],
        builtin=False,
        suggested_command=False,
    )

    async def create_go_tasking(self,
                                taskData: MythicCommandBase.PTTaskMessageAllData) -> MythicCommandBase.PTTaskCreateTaskingMessageResponse:
        response = MythicCommandBase.PTTaskCreateTaskingMessageResponse(
            TaskID=taskData.Task.ID,
            Success=True,
        )
        return response

    async def process_response(self, task: PTTaskMessageAllData, response: any) -> PTTaskProcessResponseMessageResponse:
        resp = PTTaskProcessResponseMessageResponse(TaskID=task.Task.ID, Success=True)
        return resp
