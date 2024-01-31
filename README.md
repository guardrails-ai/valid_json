# IsValidJson Validator
A Guardrails HUB Validator that checks if a value is parseable as valid JSON.
This validator can accept strings, dictionaries/objects, and lists and check if they are parseable as JSON.

## Usage
### Standalone
```py
from guardrails.validators import PassResult
from guardrails.hub import IsValidJson

validator = IsValidJson()

response = some_llm_client(...)

result = validator.validate(response.text)

if isinstance(result, PassResult):
    print("All good!")
else:
    print("LLM respoonse was not valid json!")
    print(result.error_message)
```

### From RAIl xml
```xml
<rail version="0.1">
    <output>
        <string name="text" ... />
        <float name="score" ... />
        <object
            name="metadata"
            description="The metadata associated with the generated text"
            validators="hub://guardrails/is_valid_json"
        >
            <string name="key_1" description="description of key_1" />
            ...
        </object>
    </output>
</rail>
```

```py
from guardrails import Guard
from rich import print as rich_print

guard = Guard.from_rail("my_rail.rail")

response = some_llm_client(...)

result = guard.parse(response.text)

if result.validation_passed:
    print("All good!")
else:
    print("Validation failed!")
    rich_print(guard.history.last.tree)
```

### From a Code-First Guard
```py
from guardrails import Guard
from guardrails.hub import IsValidJson
from pydantic import BaseModel, Field
from rich import print as rich_print

class GeneratedContent(BaseModel):
    text: str = Field(...)
    score: float = Field(...)
    metadata: Dict = Field(validators=[IsValidJson()])

guard = Guard.from_pydantic(GeneratedContent)

response = some_llm_client(...)

result = guard.parse(response.text)

if result.validation_passed:
    print("All good!")
else:
    print("Validation failed!")
    rich_print(guard.history.last.tree)
```


## Development
To run/develop this project locally:

1. Clone this repository
2. Setup an environment
    ```sh
    python3 -m venv ./.venv
    source ./.venv/bin/activate
    ```
3. Install dependendencies
    ```sh
    pip install -e ".[dev]"
    ```
4. Make any changes necessary
5. Run the QA suite
    ```sh
    make qa
    ```