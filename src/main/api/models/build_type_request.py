from src.main.api.models.base_model import BaseModel
from typing import Annotated, Optional, Dict, Any
from src.main.api.generators.generating_rule import GeneratingRule


class BuildTypeRequest(BaseModel):
    # Build Type ID: Start with letter, 6-20 chars, alphanumeric + underscore
    # Example: Abc123_456789, BuildType_01, Test_2024
    id: Annotated[str, GeneratingRule(regex=r"^[a-zA-Z][a-zA-Z0-9_]{5,19}$")]

    # Build Type Name: 3-100 chars, alphanumeric + spaces + underscore + hyphen
    # Example: "My Build Type", "Test-Build_01", "CI Pipeline"
    name: Annotated[str, GeneratingRule(regex=r"^[a-zA-Z0-9][a-zA-Z0-9_\- ]{2,99}$")]

    project: Optional[Dict[str, Any]] = None
    projectId: Optional[str] = None

    @staticmethod
    def generate_random(project_id: Optional[str] = None) -> "BuildTypeRequest":
        """
        Generate a random BuildTypeRequest using RandomModelGenerator.

        Args:
            project_id: Optional project ID to associate with this build type

        Returns:
            BuildTypeRequest: A randomly generated build type request
        """
        from src.main.api.generators.random_model_generator import RandomModelGenerator
        import time

        # Generate base model
        build_type = RandomModelGenerator.generate(BuildTypeRequest)

        # Add timestamp suffix for uniqueness (last 6 digits of ms timestamp)
        timestamp_suffix = str(int(time.time() * 1000))[-6:]
        build_type.id = f"{build_type.id}{timestamp_suffix}"

        # Add project reference if provided
        if project_id:
            build_type.projectId = project_id
            build_type.project = {"id": project_id}

        return build_type
