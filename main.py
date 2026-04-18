
ICONS = {
    dict: '📦',
    list: '📋',
    str: '💬',
    int: '#️⃣',
    float: '#️⃣',
    bool: '⚡',
    type(None): '🚫',
    'key': '🔑',
    'last': '└─',
    'not_last': '├─',
    'not_linked': "│ "
}


def string_maxer(
        max_length:int=60,
        is_last:bool=False,
        s:str="",
        prefix:str="",
        indent:int=3,
):
    s=s.replace("\n", " ")
    res=""
    prefix=F'{prefix}{ICONS["not_linked"] if not is_last else ""}'+(" "*indent)
    i=0
    while len(s)>0:
        if i!=0:
            s=prefix+s
        res+=s[:max_length]+'\n'
        s=s[max_length:]
        i+=1
    return res

def value_formatter(
        value:str|float|int|None,
        key=None,
        prefix:str='',
        max_length:int=60,
        is_last:bool=False,

):
    skey = f'{ICONS["key"]}{key}: ' if key  else ''
    res=F'{prefix}{ICONS["last"] if is_last else ICONS["not_last"]}{skey}{ICONS[type(value)]}{value}'
    res = string_maxer(
                    s=res,
                    max_length=max_length,
                    is_last=is_last,
                    prefix=prefix )
    return res


def list_and_dict_formatter(
        obj:dict|list,
        prefix:str='',
        child_prefix:str='',
        key_name:str|None="Корень",
        max_length: int = 60,
        max_recursion_depth: int = None,
        recursion_depth: int = 0,
        is_last_obj: bool = False,
):
    res=""
    if isinstance(obj, dict) or isinstance(obj, list) :
        s_obj=f"{prefix}{ f"{ICONS["key"]}{key_name}: " if key_name else ""}{ICONS[type(obj)]}{"dict" if type(obj)==dict else "aray"}({len(obj)})"
        s_obj=string_maxer(max_length=max_length,is_last=(False if len(obj)!=0 else True),prefix=child_prefix,s=s_obj,indent=1)
        res=res+s_obj
        if (not obj) or (recursion_depth == max_recursion_depth):
            return res
        last_index=len(obj)-1
        if isinstance(obj,dict):
            for ind, (key, value) in enumerate(obj.items()):
                is_last=(ind == last_index)
                if isinstance(value, dict) or isinstance(value, list):
                    res=res+list_and_dict_formatter(
                        obj=value,
                        prefix=f"{child_prefix}{ICONS['last'] if is_last else ICONS['not_last']  }",
                        child_prefix=f"{child_prefix}{"  " if is_last else "│ "}",
                        key_name=key,
                        max_length=max_length,
                        max_recursion_depth=max_recursion_depth,
                        recursion_depth=recursion_depth+1,
                        is_last_obj=is_last
                    )
                    if not is_last: res=res+f"{child_prefix}│\n"
                elif type(value) in (int, float, bool, str,type(None)):
                    res=res+value_formatter(
                        value=value,
                        key=key,
                        prefix=child_prefix,
                        is_last=is_last,
                        max_length=max_length,
                    )
                else:
                    res=res+f"{prefix}unreg type {type(value)}\n"
        else:
            for ind,value in enumerate(obj):
                is_last = (ind == last_index)
                if isinstance(value, dict) or isinstance(value, list):
                    res = res + list_and_dict_formatter(
                        obj=value,
                        prefix=f"{child_prefix}{ICONS['last'] if is_last else ICONS['not_last']}",
                        child_prefix=f"{child_prefix}{"  " if is_last else "│ "}",
                        key_name=None,
                        max_length=max_length,
                        max_recursion_depth=max_recursion_depth,
                        recursion_depth=recursion_depth + 1,
                        is_last_obj=is_last
                    )
                    if not is_last: res = res + f"{child_prefix}│\n"
                elif type(value) in (int, float, bool, str, type(None)):
                    res = res + value_formatter(
                        value=value,
                        key=None,
                        prefix=child_prefix,
                        is_last=is_last,
                        max_length=max_length,
                    )
                else:
                    res = res + f"{prefix}unreg type {type(value)}\n"
    return res


def json_format(
        body:dict|list|None=None,
        max_length:int=60,
        max_recursion_depth:int=None,
):
    if body is None:
        body = {"data": "empty"}
    return list_and_dict_formatter(obj=body,max_length=max_length,max_recursion_depth=max_recursion_depth)



a = {
    "short": "short value",
    "medium_key_that_is_around_40_chars_long": "medium value 40 chars",
    "very_long_key_that_is_definitely_more_than_60_characters_long_and_should_wrap_properly": {
        "short_key": "short",
        "very_long_nested_key_that_exceeds_60_chars_and_must_wrap_with_correct_indent": "some value",
        "another_medium_key_35_chars_here": "another_value"
    },
    "mixed_types": {
        "int_val": 12345,
        "float_val": 12345.6789,
        "bool_true": True,
        "bool_false": False,
        "null_val": None,
        "string_val": "Hello World"
    },
    "arrays": {
        "short_array": [1, 2, 3],
        "medium_array": ["one", "two", "three", "four", "five"],
        "long_strings_array": [
            "short",
            "this is a very long string that exceeds sixty characters and should be wrapped",
            "another long string that also needs to be wrapped correctly with proper indentation",
            "short again"
        ],
        "mixed_array": [1, "string", True, None, 3.14, {"nested": "dict"}],
        "array_of_dicts": [
            {"id": 1, "name": "first", "description": "first item description"},
            {"id": 2, "name": "second", "description": "second item with longer description that might wrap"},
            {"id": 3, "name": "third", "description": "third"}
        ]
    },
    "deep_nesting": {
        "level1": {
            "level2": {
                "level3": {
                    "level4": {
                        "level5": "deep value",
                        "level5_with_long_key_that_exceeds_limit": "value",
                        "level5_array": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                    },
                    "level3_long_key_that_exceeds_60_chars_and_must_wrap": "value at level 3"
                },
                "level2_key_with_moderate_length": {
                    "nested": "value",
                    "another": 42
                }
            },
            "level1_long_key_that_exceeds_60_chars_and_should_be_properly_formatted": "level1 value"
        }
    },
    "long_values": {
        "short_key": "very long string value that exceeds the maximum length of sixty characters and should be wrapped across multiple lines with proper indentation preserving the tree structure",
        "another_key": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.",
        "numeric_key": 123456789,
        "list_with_long_strings": [
            "first element with normal length",
            "second element with very very very long text that goes beyond sixty characters and needs to be wrapped correctly",
            "third",
            "fourth element that also has extremely long content that will definitely exceed the max length and test the wrapping functionality"
        ]
    },
    "edge_cases": {
        "": "empty key",
        "empty_string_value": "",
        "very_long_key_with_special_chars_!@#$%^&*()_+": "value",
        "unicode_key_😀_🎉_🔥": "unicode_value_😀_🎉_🔥_🚀_💡",
        "key_with\nnewline": "value_with\nnewline",
        "key_with\ttab": "value_with\ttab",
        "zero": 0,
        "negative": -100,
        "large_number": 99999999999999999999,
        "scientific": 1.23456789e10,
        "boolean_list": [True, False, True, False],
        "mixed_nesting": [
            {"simple": "dict"},
            ["nested", "list", {"inside": "value"}],
            {"array_in_dict": [1, 2, {"deep": "value"}]}
        ]
    },
    "large_collection": {
        f"key_{i}": f"value_{i}" for i in range(20)
    },
    "repetitive_patterns": {
        "pattern1": {
            "id": 1,
            "data": "x" * 30,
            "metadata": "y" * 40,
            "description": "z" * 80
        },
        "pattern2": {
            "id": 2,
            "data": "a" * 30,
            "metadata": "b" * 40,
            "description": "c" * 80
        },
        "pattern3": {
            "id": 3,
            "data": "d" * 30,
            "metadata": "e" * 40,
            "description": "f" * 100
        }
    },
    "recursive_structure": {
        "name": "root",
        "children": [
            {
                "name": "child1",
                "value": 10,
                "children": [
                    {
                        "name": "grandchild1",
                        "value": 1,
                        "children": []
                    },
                    {
                        "name": "grandchild2",
                        "value": 2,
                        "children": []
                    }
                ]
            },
            {
                "name": "child2_with_very_long_name_that_exceeds_limit_and_should_wrap",
                "value": 20,
                "children": [
                    {
                        "name": "grandchild3",
                        "value": 3,
                        "children": []
                    }
                ]
            }
        ]
    },
    "testing_boundaries": {
        "a": "x",
        "ab": "xx",
        "abc": "xxx",
        "abcd": "xxxx",
        "abcde": "xxxxx",
        "abcdef": "xxxxxx",
        "abcdefg": "xxxxxxx",
        "abcdefgh": "xxxxxxxx",
        "abcdefghi": "xxxxxxxxx",
        "abcdefghij": "xxxxxxxxxx",
        "abcdefghijk": "xxxxxxxxxxx",
        "abcdefghijkl": "xxxxxxxxxxxx",
        "abcdefghijklm": "xxxxxxxxxxxxx",
        "abcdefghijklmn": "xxxxxxxxxxxxxx",
        "abcdefghijklmno": "xxxxxxxxxxxxxxx",
        "abcdefghijklmnop": "xxxxxxxxxxxxxxxx",
        "abcdefghijklmnopq": "xxxxxxxxxxxxxxxxx",
        "abcdefghijklmnopqr": "xxxxxxxxxxxxxxxxxx",
        "abcdefghijklmnopqrs": "xxxxxxxxxxxxxxxxxxx",
        "abcdefghijklmnopqrst": "xxxxxxxxxxxxxxxxxxxx"
    }
}

def main():
    print(json_format(
        a
    ))



if __name__ == '__main__':
    main()
