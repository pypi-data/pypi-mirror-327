from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentInformationResponse")


@_attrs_define
class AgentInformationResponse:
    """generation agent information response

    Attributes:
        description (Union[Unset, str]): Description of the agent
        display_name (Union[Unset, str]): Display name of the agent
        name (Union[Unset, str]): Name of the agent
        prompt (Union[Unset, str]): Prompt of the agent
    """

    description: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    prompt: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        display_name = self.display_name

        name = self.name

        prompt = self.prompt

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if name is not UNSET:
            field_dict["name"] = name
        if prompt is not UNSET:
            field_dict["prompt"] = prompt

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        description = d.pop("description", UNSET)

        display_name = d.pop("displayName", UNSET)

        name = d.pop("name", UNSET)

        prompt = d.pop("prompt", UNSET)

        agent_information_response = cls(
            description=description,
            display_name=display_name,
            name=name,
            prompt=prompt,
        )

        agent_information_response.additional_properties = d
        return agent_information_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
