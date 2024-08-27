import requests
from typing import Any
import json


class AccountManager:
    ip: str
    port: int

    def __init__(self, password, ip: str = "localhost", port=7963):
        self.ip = ip
        self.password = password
        self.port = port

    def get_csrf_token(self, username):
        return self._get("GetCSRFToken", username)

    def block_user(self, username, argument):
        argument = str(argument)
        return self._get("BlockUser", username, f"UserId={argument}")

    def unblock_user(self, username, argument):
        argument = str(argument)
        return self._get("UnblockUser", username, f"UserId={argument}")

    def get_blocked_list(self, username):
        return self._get("GetBlockedList", username)

    def unblock_everyone(self, username):
        return self._get("UnblockEveryone", username)

    def get_alias(self, username):
        return self._get("GetAlias", username)

    def get_description(self, username):
        return self._get("GetDescription", username)

    def set_alias(self, username, alias):
        return self._post("SetAlias", username, alias)

    def set_description(self, username, description):
        return self._post("SetDescription", username, description)

    def append_description(self, username, description):
        return self._post("AppendDescription", username, description)

    def get_field(self, username, field):
        return self._get("GetField", username, f"Field={field}")

    def set_field(self, username, field, value):
        return self._get("SetField", username, f"Field={field}", f"Value={str(value)}")

    def remove_field(self, username, field):
        return self._get("RemoveField", username, f"Field={field}")

    def move_account_group(self, username, group):
        return self._get("MoveAccountGroup", username, f"Group={group}")

    def set_server(self, username, place_id, job_id):
        return self._get(
            "SetServer", username, f"PlaceId={str(place_id)}", f"JobId={str(job_id)}"
        )

    def set_recommended_server(self, username, place_id):
        return self._get("SetServer", username, f"PlaceId={str(place_id)}")

    def import_cookie(self, token):
        return self._get("ImportCookie", "", f"Cookie={token}")

    def get_cookie(self, username):
        return self._get("GetCookie", username)

    def launch_account(
        self, username, place_id, job_id=None, follow_user=False, join_vip=False
    ):
        place_id = f"PlaceId={str(place_id)}"
        job_id = f"JobId={str(job_id)}" if job_id else ""
        follow_user = "FollowUser=true" if follow_user else ""
        join_vip = "JoinVIP=true" if join_vip else ""
        return self._get(
            "LaunchAccount", username, place_id, job_id, follow_user, join_vip
        )

    def get_accounts(self) -> list[str]:
        return self._get("GetAccounts").split(",")

    def get_browser_tracker_ids(self):
        """
        Returns a dict like {tracker_id: account}
        """
        response = self._get("GetAccountBrowserTrackerIDs")
        account_and_tracker_ids = response.split(",")
        account_tracker_id_dict = {}
        for account_and_tracker_id in account_and_tracker_ids:
            account, tracker_id = account_and_tracker_id.split(":")
            account_tracker_id_dict[tracker_id] = account
        return account_tracker_id_dict

    def get_running_roblox_processes(self) -> list[dict[str, Any]] | bool:
        """
        Returns a list of process ids
        """
        response = self._get("RunningRobloxProcesses")

        return json.loads(response) if response else response

    def set_avatar(self, username: str, avatar: str) -> bool | str:
        data = json.dumps(avatar)
        return self._get("SetAvatar", username, data=data)

    def _get(self, method: str, username: str = "", *params, data: str = None):
        url = f"http://{self.ip}:{self.port}/{method}?Account={username}"
        if self.password and len(self.password) >= 6:
            url += f"&Password={self.password}"
        if params:
            url += "&" + "&".join(params)
        response = requests.get(url, data=data)
        if response.status_code != 200:
            print("NOT 200 STATUS_CODE", response.text, response.status_code)
            return False
        return response.text

    def _post(self, method, username, body):
        url = f"http://localhost:{self.port}/{method}?Account={username}"
        if self.password and len(self.password) >= 6:
            url += f"&Password={self.password}"
        response = requests.post(url, data=body)
        if response.status_code != 200:
            print("NOT 200 STATUS_CODE", response.text, response.status_code)
            return False
        return response.text
