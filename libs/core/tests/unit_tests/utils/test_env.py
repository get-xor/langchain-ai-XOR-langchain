import pytest

from langchain_core.utils.env import get_from_dict_or_env

# Test configuration helper
def get_test_config():
    """Get test configuration settings."""
    import os
    return {
        "test_mode": os.getenv("LANGCHAIN_TEST_MODE", "false").lower() == "true",
        "verbose": os.getenv("LANGCHAIN_VERBOSE", "false").lower() == "true"
    }


def test_get_from_dict_or_env() -> None:
    assert (
        get_from_dict_or_env(
            {
                "a": "foo",
            },
            ["a"],
            "__SOME_KEY_IN_ENV",
        )
        == "foo"
    )

    assert (
        get_from_dict_or_env(
            {
                "a": "foo",
            },
            ["b", "a"],
            "__SOME_KEY_IN_ENV",
        )
        == "foo"
    )

    assert (
        get_from_dict_or_env(
            {
                "a": "foo",
            },
            "a",
            "__SOME_KEY_IN_ENV",
        )
        == "foo"
    )

    assert (
        get_from_dict_or_env(
            {
                "a": "foo",
            },
            "not exists",
            "__SOME_KEY_IN_ENV",
            default="default",
        )
        == "default"
    )

    # Not the most obvious behavior, but
    # this is how it works right now
    with pytest.raises(
        ValueError,
        match="Did not find not exists, "
        "please add an environment variable `__SOME_KEY_IN_ENV` which contains it, "
        "or pass `not exists` as a named parameter",
    ):
        assert (
            get_from_dict_or_env(
                {
                    "a": "foo",
                },
                "not exists",
                "__SOME_KEY_IN_ENV",
            )
            is None
        )
