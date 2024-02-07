# Overview

| Developed by | Guardrails AI |
| Date of development | Feb 15, 2024 |
| Validator type | Format |
| Blog |  |
| License | Apache 2 |
| Input/Output | Output |

# Description

This validator ensures that a generated output is is parseable as valid JSON..

# Installation

```bash
$ guardrails hub install hub://guardrails/valid_json
```

# Usage Examples

## Validating string output via Python

In this example, we’ll test that a generated value is valid json.

```python
# Import Guard and Validator
from guardrails.hub import ValidJson
from guardrails import Guard

# Initialize Validator
val = ValidJson()

# Setup Guard
guard = Guard.from_string(
    validators=[val, ...],
)

guard.parse("{ \"value\": \"a test value\" }")  # Validator passes
guard.parse( "{ \"value\": \"a test value\", }")  # Validator fails; note the trailing comma
```

## Validating JSON output via Python

In this example, we verify that a user’s email is specified in lower case.

```python
# Import Guard and Validator
from pydantic import BaseModel
from guardrails.hub import LowerCase
from guardrails import Guard

val = ValidJson()

# Create Pydantic BaseModel
class GeneratedContent(BaseModel):
    text: str
    score: float
    metadata: Dict = Field(validators=[ValidJson()])

# Create a Guard to check for valid Pydantic output
guard = Guard.from_pydantic(output_class=UserInfo)

# Run LLM output generating JSON through guard
guard.parse("""
{
		"text": "this is some generated text",
        "score": 2
		"metadata": {
            "property_1": "some meta data"
        }
}
""")
```

# API Reference

`__init__`
- `on_fail`: The policy to enact when a validator fails.