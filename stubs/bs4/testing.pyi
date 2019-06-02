# Stubs for bs4.testing (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

import unittest
from bs4.builder import HTMLParserTreeBuilder
from typing import Any, Optional

__license__: str
default_builder = HTMLParserTreeBuilder
BAD_DOCUMENT: str

class SoupTest(unittest.TestCase):
    @property
    def default_builder(self): ...
    def soup(self, markup: Any, **kwargs: Any): ...
    def document_for(self, markup: Any): ...
    def assertSoupEquals(self, to_parse: Any, compare_parsed_to: Optional[Any] = ...) -> None: ...
    def assertConnectedness(self, element: Any) -> None: ...
    def linkage_validator(self, el: Any, _recursive_call: bool = ...): ...

class HTMLTreeBuilderSmokeTest:
    def test_empty_element_tags(self) -> None: ...
    def test_pickle_and_unpickle_identity(self) -> None: ...
    def assertDoctypeHandled(self, doctype_fragment: Any) -> None: ...
    def test_normal_doctypes(self) -> None: ...
    def test_empty_doctype(self) -> None: ...
    def test_public_doctype_with_url(self) -> None: ...
    def test_system_doctype(self) -> None: ...
    def test_namespaced_system_doctype(self) -> None: ...
    def test_namespaced_public_doctype(self) -> None: ...
    def test_real_xhtml_document(self) -> None: ...
    def test_namespaced_html(self) -> None: ...
    def test_processing_instruction(self) -> None: ...
    def test_deepcopy(self) -> None: ...
    def test_p_tag_is_never_empty_element(self) -> None: ...
    def test_unclosed_tags_get_closed(self) -> None: ...
    def test_br_is_always_empty_element_tag(self) -> None: ...
    def test_nested_formatting_elements(self) -> None: ...
    def test_double_head(self) -> None: ...
    def test_comment(self) -> None: ...
    def test_preserved_whitespace_in_pre_and_textarea(self) -> None: ...
    def test_nested_inline_elements(self) -> None: ...
    def test_nested_block_level_elements(self) -> None: ...
    def test_correctly_nested_tables(self) -> None: ...
    def test_multivalued_attribute_with_whitespace(self) -> None: ...
    def test_deeply_nested_multivalued_attribute(self) -> None: ...
    def test_multivalued_attribute_on_html(self) -> None: ...
    def test_angle_brackets_in_attribute_values_are_escaped(self) -> None: ...
    def test_strings_resembling_character_entity_references(self) -> None: ...
    def test_entities_in_foreign_document_encoding(self) -> None: ...
    def test_entities_in_attributes_converted_to_unicode(self) -> None: ...
    def test_entities_in_text_converted_to_unicode(self) -> None: ...
    def test_quot_entity_converted_to_quotation_mark(self) -> None: ...
    def test_out_of_range_entity(self) -> None: ...
    def test_multipart_strings(self) -> None: ...
    def test_empty_element_tags(self) -> None: ...
    def test_head_tag_between_head_and_body(self) -> None: ...
    def test_multiple_copies_of_a_tag(self) -> None: ...
    def test_basic_namespaces(self) -> None: ...
    def test_multivalued_attribute_value_becomes_list(self) -> None: ...
    def test_can_parse_unicode_document(self) -> None: ...
    def test_soupstrainer(self) -> None: ...
    def test_single_quote_attribute_values_become_double_quotes(self) -> None: ...
    def test_attribute_values_with_nested_quotes_are_left_alone(self) -> None: ...
    def test_attribute_values_with_double_nested_quotes_get_quoted(self) -> None: ...
    def test_ampersand_in_attribute_value_gets_escaped(self) -> None: ...
    def test_escaped_ampersand_in_attribute_value_is_left_alone(self) -> None: ...
    def test_entities_in_strings_converted_during_parsing(self) -> None: ...
    def test_smart_quotes_converted_on_the_way_in(self) -> None: ...
    def test_non_breaking_spaces_converted_on_the_way_in(self) -> None: ...
    def test_entities_converted_on_the_way_out(self) -> None: ...
    def test_real_iso_latin_document(self) -> None: ...
    def test_real_shift_jis_document(self) -> None: ...
    def test_real_hebrew_document(self) -> None: ...
    def test_meta_tag_reflects_current_encoding(self) -> None: ...
    def test_html5_style_meta_tag_reflects_current_encoding(self) -> None: ...
    def test_tag_with_no_attributes_can_have_attributes_added(self) -> None: ...
    def test_worst_case(self) -> None: ...

class XMLTreeBuilderSmokeTest:
    def test_pickle_and_unpickle_identity(self) -> None: ...
    def test_docstring_generated(self) -> None: ...
    def test_xml_declaration(self) -> None: ...
    def test_processing_instruction(self) -> None: ...
    def test_real_xhtml_document(self) -> None: ...
    def test_nested_namespaces(self) -> None: ...
    def test_formatter_processes_script_tag_for_xml_documents(self) -> None: ...
    def test_can_parse_unicode_document(self) -> None: ...
    def test_popping_namespaced_tag(self) -> None: ...
    def test_docstring_includes_correct_encoding(self) -> None: ...
    def test_large_xml_document(self) -> None: ...
    def test_tags_are_empty_element_if_and_only_if_they_are_empty(self) -> None: ...
    def test_namespaces_are_preserved(self) -> None: ...
    def test_closing_namespaced_tag(self) -> None: ...
    def test_namespaced_attributes(self) -> None: ...
    def test_namespaced_attributes_xml_namespace(self) -> None: ...
    def test_find_by_prefixed_name(self) -> None: ...
    def test_copy_tag_preserves_namespace(self) -> None: ...
    def test_worst_case(self) -> None: ...

class HTML5TreeBuilderSmokeTest(HTMLTreeBuilderSmokeTest):
    def test_real_xhtml_document(self) -> None: ...
    def test_html_tags_have_namespace(self) -> None: ...
    def test_svg_tags_have_namespace(self) -> None: ...
    def test_mathml_tags_have_namespace(self) -> None: ...
    def test_xml_declaration_becomes_comment(self) -> None: ...

def skipIf(condition: Any, reason: Any): ...
