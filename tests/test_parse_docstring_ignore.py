from copy import deepcopy
import unittest

from tests.__init__ import blank_parse_docstring_return
from src.parser import parse_docstring

class TestParseDocstring_Ignore(unittest.TestCase):

    ###############################################################
    # Ignore
    ###############################################################

    def test_only_ignore_tag_only_value(self):

        description_entry = """@ignore"""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["ignore"] = True
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_ignore_tag_own_line(self):

        description_entry = """
        @ignore
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["ignore"] = True
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_ignore_tag_extra_characters_after_not_marked_as_ignore(self):

        description_entry = """
        @ignore nope
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["ignore"] = False
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
    
    def test_only_ignore_tag_extra_characters_after_not_marked_as_ignore(self):

        description_entry = """
        This is also not @ignore
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is also not @ignore"
        expected_docstring_return["ignore"] = False
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_ignore_tag_extra_whitespace(self):

        description_entry = """      
              @ignore      
                
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["ignore"] = True
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_multiple_ignore_tags_cause_no_errors(self):
        """It should not matter how many times a `@ignore` tag gets included. It should cause no errors, even if some
        of the tags are incorrect."""
        description_entry = """
        @ignore
        @ignore
        @ignore This won't flag as ignore
        This won't flag as @ignore
        @ignore
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["ignore"] = True
        
        self.assertDictEqual(expected_docstring_return, returned_dict)


    # ###############################################################
    # # Complex
    # ###############################################################

    def test_ignore_tag_surrounded_by_other_tags(self):

        description_entry = """This one also has a description in it.

        @param MyParam This is a param description
        @ignore
        @throws An error with no type 1
        @example Some caption text
        # This is a comment within the example
        myvar = 2
        if myvar == 2:
            print(myvar)
        @param SecondParamName This is another param description
        @returns This is the ultimate return text
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This one also has a description in it."
        expected_docstring_return["ignore"] = True
        expected_docstring_return["examples"] = []
        expected_docstring_return["examples"].append({"caption": "Some caption text", "code": "# This is a comment within the example\nmyvar = 2\nif myvar == 2:\n    print(myvar)"})
        expected_docstring_return["throws"] = []
        expected_docstring_return["throws"].append({"type": None, "description": "An error with no type 1"})
        expected_docstring_return["parameters"].append({"MyParam": "This is a param description"})
        expected_docstring_return["parameters"].append({"SecondParamName": "This is another param description"})
        expected_docstring_return["returns"] = "This is the ultimate return text"
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_invalid_ignore_tags_surrounded_by_other_tags(self):
        """If there is an invalid `@ignore` tag, then the object should not get marked as ignored."""

        description_entry = """This one also has a description in it.

        @param MyParam This is a param description
        @ignore but invalid
        @throws An error with no type 1
        @example Some caption text
        # This is a comment within the example
        myvar = 2
        if myvar == 2:
            print(myvar)
        @param SecondParamName This is another param description
        @returns This is the ultimate return text
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This one also has a description in it."
        expected_docstring_return["ignore"] = False
        expected_docstring_return["examples"] = []
        expected_docstring_return["examples"].append({"caption": "Some caption text", "code": "# This is a comment within the example\nmyvar = 2\nif myvar == 2:\n    print(myvar)"})
        expected_docstring_return["throws"] = []
        expected_docstring_return["throws"].append({"type": None, "description": "An error with no type 1"})
        expected_docstring_return["parameters"].append({"MyParam": "This is a param description"})
        expected_docstring_return["parameters"].append({"SecondParamName": "This is another param description"})
        expected_docstring_return["returns"] = "This is the ultimate return text"
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_invalid_ignore_tag_plus_good_tag_combined_with_other_tags(self):
        """If there is an invalid `@ignore` tag, but there is another valid one within a complex docstring, then the
        object should get marked as ignored."""

        description_entry = """This one also has a description in it.

        @param MyParam This is a param description
        @private
        @ignore but invalid
        @throws An error with no type 1
        @example Some caption text
        # This is a comment within the example
        myvar = 2
        if myvar == 2:
            print(myvar)
        @param SecondParamName This is another param description
        @returns This is the ultimate return text
        @ignore
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This one also has a description in it."
        expected_docstring_return["private"] = True
        expected_docstring_return["ignore"] = True
        expected_docstring_return["examples"] = []
        expected_docstring_return["examples"].append({"caption": "Some caption text", "code": "# This is a comment within the example\nmyvar = 2\nif myvar == 2:\n    print(myvar)"})
        expected_docstring_return["throws"] = []
        expected_docstring_return["throws"].append({"type": None, "description": "An error with no type 1"})
        expected_docstring_return["parameters"].append({"MyParam": "This is a param description"})
        expected_docstring_return["parameters"].append({"SecondParamName": "This is another param description"})
        expected_docstring_return["returns"] = "This is the ultimate return text"
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
