import pytest

from dataclasses import dataclass

from guardrails.validators import PassResult, FailResult

from validator.main import IsValidJson


@pytest.mark.parametrize(
    "value",
    [
      (
        "{ \"value\": \"a test value\" }"
      ),
      (
        { "value": "a test value" }
      ),
      (
        "[{ \"value\": \"a test value\" }, { \"value\": \"a second test value\" }]"
      ),
      (
        [{ "value": "a test value" }, { "value": "a second test value" }]
      )
    ]
)
def test_valid_json(value):
  validator = IsValidJson()

  result = validator.validate(value, {})

  assert isinstance(result, PassResult)


@dataclass
class NonSerializeable:
  value: str

@pytest.mark.parametrize(
    "value,error",
    [
      (
        "{ \"value\": \"a test value\", }",
        "Expecting property name enclosed in double quotes: line 1 column 28 (char 27)"
      ),
      (
         NonSerializeable(value="a test value"),
         "Object of type NonSerializeable is not JSON serializable"
      ),
      (
        "[{ \"value\": \"a test value\" } { \"value\": \"a second test value\" }]",
        "Expecting ',' delimiter: line 1 column 30 (char 29)"
      ),
      (
        [NonSerializeable(value="a test value"), NonSerializeable(value="a second test value")],
        "Object of type NonSerializeable is not JSON serializable"
      )
    ]
)
def test_invalid_json(value, error):
  validator = IsValidJson()

  result = validator.validate(value, {})

  assert isinstance(result, FailResult)

  assert result.error_message == 'Value is not parseable as valid JSON! Reason: ' + error