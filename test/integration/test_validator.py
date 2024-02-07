from typing import Dict, List
import pytest

from guardrails import Guard
from guardrails.validator_base import ValidatorError
from pydantic import BaseModel, Field
from validator import ValidJson


class StringTestObject(BaseModel):
    test_val: str = Field(
        validators=[
            ValidJson(on_fail="exception")
        ]
    )
class DictionaryTestObject(BaseModel):
    test_val: Dict = Field(
        validators=[
            ValidJson(on_fail="exception")
        ]
    )
class ListTestObject(BaseModel):
    test_val: List = Field(
        validators=[
            ValidJson(on_fail="exception")
        ]
    )

@pytest.mark.parametrize(
    "value,model",
    [
      (
        """
        {
          "test_val": "{ \\"value\\": \\"a test value\\" }"
        }
        """,
        StringTestObject
      ),
      (
        """
        {
          "test_val": { "value": "a test value" }
        }
        """,
        DictionaryTestObject
      ),
      (
        """
          {
            "test_val": "[{ \\"value\\": \\"a test value\\" }, { \\"value\\": \\"a second test value\\" }]"
          }
        """,
        StringTestObject
      ),
      (
        """
          {
            "test_val": [{ "value": "a test value" }, { "value": "a second test value" }]
          }
        """,
        ListTestObject
      )
    ]
)
def test_valid_json(value, model):
  guard = Guard.from_pydantic(output_class=model)

  response = guard.parse(value)

  assert response.validation_passed is True


@pytest.mark.parametrize(
    "value,model,error",
    [
      (
        """
        {
          "test_val": "{ \\"value\\": \\"a test value\\", }"
        }
        """,
        StringTestObject,
        "Expecting property name enclosed in double quotes: line 1 column 28 (char 27)"
      ),
      (
        """
          {
            "test_val": "[{ \\"value\\": \\"a test value\\" } { \\"value\\": \\"a second test value\\" }]"
          }
        """,
        StringTestObject,
        "Expecting ',' delimiter: line 1 column 30 (char 29)"
      ),
      # These don't make it to validation because they raise during parsing.
      # (
      #   """
      #     {
      #       "test_val": [{ "value": "a test value", }, { "value": "a second test value" }]
      #     }
      #   """,
      #   ListTestObject,
      #   ""
      # ),
      #  (
      #   """
      #   {
      #     "test_val": { "value": "a test value", }
      #   }
      #   """,
      #   DictionaryTestObject,
      #   "Expecting property name enclosed in double quotes: line 3 column 50 (char 60)"
      # ),
    ]
)
def test_invalid_json(value, model, error):
  with pytest.raises(ValidatorError) as exc_info:
    guard = Guard.from_pydantic(output_class=model)
    guard.parse(value)

  assert str(exc_info.value) == (
     "Validation failed for field with errors: "
     "Value is not parseable as valid JSON! Reason: "
     f"{error}"
  )