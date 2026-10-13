"""Library request models."""

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator

from src.utils.common import validate_non_empty_string


class RepositoryRequest(BaseModel):
    """Request to create library from repository.

    This class handles requests to create a new library by cloning
    and processing a Git repository. It requires both the repository
    URL and an access token for authentication.

    Attributes:
        repo_url: The full URL of the Git repository to clone.
            Must be a valid Git URL (HTTP/HTTPS or SSH).
        access_token: Authentication token for accessing the repository.
            Required for private repositories or rate limit increases.
    """

    repo_url: str = Field(
        ..., description="The full URL of the Git repository to clone", alias="repoUrl"
    )

    access_token: str | None = Field(
        None, description="Authentication token for accessing the repository"
    )

    @field_validator("access_token")
    @classmethod
    def validate_access_token(cls, v: str | None) -> str | None:
        """Check that access_token is stripped.

        Args:
            v: The token string to validate.

        Returns:
            The stripped token string.

        Raises:
            ValidationError: If token is None (actually it should be None).
        """
        if v is None:
            return None
        stripped = v.strip()
        return stripped if stripped else None

    @field_validator("repo_url")
    @classmethod
    def validate_repo_url(cls, v: str) -> str:
        """Check that repo_url is not empty.

        Args:
            v: The repository URL.

        Returns:
            The validated repository URL.

        Raises:
            ValidationError: If repository URL is empty and not None.
        """
        print(f"DEBUG: Validating repo_url: '{v}'")
        return validate_non_empty_string(v)


class ContentRequest(BaseModel):
    """Request to create library from pushed content.

    This class handles requests to create a new library by directly
    uploading file content. It allows users to create libraries without
    needing a Git repository.

    Attributes:
        title: The display name for the library.
            Must be a non-empty string that will be shown to users.
        description: Optional description explaining what the library contains.
            Can be empty but helps users understand the library purpose.
        files: A mapping of file paths to their content.
            Keys are relative file paths, values are the file content as strings.
    """

    title: str = Field(..., description="The display name for the library")
    description: str = Field(
        "", description="Optional description of the library contents"
    )
    files: dict[str, str] = Field(
        ..., description="Mapping of file paths to their text content"
    )

    @field_validator("title")  # noqa
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Check that the library title is not empty.

        Args:
            v: The title string to validate.

        Returns:
            The validated title string.

        Raises:
            ValueError: If the title is empty or contains only whitespace.
        """
        return validate_non_empty_string(v)
