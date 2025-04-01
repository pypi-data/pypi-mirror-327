from typing import Any, Dict
from .base import EmploymentHeroBase

class Employee(EmploymentHeroBase):
    """
    Employee API Wrapper.
    With a business parent, its URL becomes:
      {parent_path}/employee
    For example: /v2/business/{business_id}/employee
    """

    @property
    def full_name(self) -> str:
        first = self.data.get("firstName", "")
        last = self.data.get("surname", "")
        return f"{first} {last}".strip()

    async def grant_access(self, email: str, name: str) -> Dict[str, Any]:
        """Example method to grant access to an employee."""
        url = self._build_url(resource_id=self.data.get("id"), suffix="access")
        payload = {
            "email": email,
            "name": name,
            "suppressNotificationEmails": False
        }
        response = await self.client._request("POST", url, json=payload)
        return response.json()