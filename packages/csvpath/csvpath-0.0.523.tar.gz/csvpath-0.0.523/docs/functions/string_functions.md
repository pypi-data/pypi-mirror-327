
# String Functions

The string handling functions operate on strings. Many have Python equivalents and behave similarly.

### alter(value, value, value)

Alters the first string by substituting the third string for every instance of the second string.

```bash
    @altered = alter("the quick brown dog", "dog", "fox")
    @altered == "the quick brown fox" -> print("Yes, that's right")
```

### caps(value, value)

Uppercases the initial character of a string. If the optional second argument evaluates to True (e.g. `yes()`) the string is split on a space (`" "`) and each substring's initial char is uppercased.

### concat(value, value, ...)

Concatenates any number of strings.

### length(value)

Same as you would expect.

### min_length(value, int) and max_length(value, int)

`min_length()` and `max_length()` return True if the stringified value is more than or less than the integer provided. The functionality can also be achieved using `above()` and `below()` or `between()`, but the min and max functions are obviously simpler. Likewise, there is overlap with the newer `string()`; however, you cannot use `string()` to set a min without also setting a max; for that you would need `min_length()`.

### string(value, max, min)

`string()` is an evolved approach that enables a simpler declaration of a string. Think of it like a VARCHAR declaration in SQL's DDL. You can add the `notnone` qualifier to force `string()` to be not None. `string()` stringifies its value. The value of `string()` is the value it wraps. Standing alone it is an existance test that the wrapped value is not None.

### lower(value)

Lowercases a string.

### starts_with(does_this, start_with_this)

Checks if the first value, stringified, starts with the second value. The values are stripped. Alias: `startswith()`. If either value is `none()` or `None` the result is False. If the second value is `""` the result is False.

### ends_with(does_this, end_with_this)

Checks if the first value, stringified, ends with the second value. The values are stripped. Alias: `endswith()`.  If either value is `none()` or `None` the result is False. If the second value is `""` the result is False.


### strip(value)

Trims whitespace. Same as you would expect from the Python function.

### substring(value, int)

Substring starting from left and including the number of characters indicated. The value is stringified, so you can substring essentially anything. Unlike Python, for clarity CsvPath does not allow negatives.

### upper(value)

Uppercases a string.

## Examples

```bash
    $file.csv[*][
        @name = concat( #firstname, " ", #lastname )
        @name = strip(@name)
        @len = length(#firstname)
        @first = substring(@name, @len)
        @lower = lower(@name)
        @badge = upper(value)
    ]
```

This csvpath uses the string functions in their obvious ways.

```bash
    $file.csv[*][
        @name = #firstname
        @name_length = length(@name)
        gt(@name_length, 12) -> @name = substring(#firstname, 9)
        length(@name) == 9 -> @name = concat(@name, "...")
        print("Welcome $.variables.name")
    ]
```

This csvpath does backflips to get a truncated name, mainly proving that CsvPath is not a programming language. Validation is enough.


