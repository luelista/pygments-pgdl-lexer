"""Pygments lexer for PRE Workbench's Protocol Grammar Description Language"""
from pygments.lexer import Lexer
from pygments.token import *
import lark

__all__ = ("PGDLLexer",)


class PGDLLexer(Lexer):

    """Lexer for Protocol Grammar Description Language"""

    name = 'Protocol Grammar Description Language'
    aliases = ['pgdl']
    filenames = ['*.pgdl']
    mimetypes = ['text/x-prewb-pgdl']

    tokens = {
        "LBRACE": Punctuation,
        "RBRACE": Punctuation,
        "ESCAPED_STRING": String.Double,
        "NUMBER": Number,
        "LPAR": Punctuation,
        "RPAR": Punctuation,
        "COMMA": Punctuation,
        "LSQB": Punctuation,
        "RSQB": Punctuation,
        "EQUAL": Operator,
        "COLON": Operator,
        "DOT": Operator,
        "DOTS": Operator,
        "TERM_OP": Operator,
        "FACTOR_OP": Operator,
        "CONJ_OP": Operator,
        "EQ_OP": Operator,
        "COMP_OP": Operator,
        "IDENTIFIER": Name,
        "GLOBAL_IDENTIFIER": Name.Class,
        "FIELD_NAME_IDENTIFIER": Name.Property,
        "VAR_REF_IDENTIFIER": Name.Variable.Instance,
        "TYPE_REF_IDENTIFIER": Name.Builtin,
        "FUN_NAME_IDENTIFIER": Name.Function,
        "KEY_IDENTIFIER": Name.Attribute,

        "VARIANT": Keyword,
        "STRUCT": Keyword,
        "BITS": Keyword,
        "UNION": Keyword,
        "SWITCH": Keyword,
        "CASE": Keyword,
        "REPEAT": Keyword,

        "TRUE": Keyword.Constant,
        "FALSE": Keyword.Constant,
        "NULL": Keyword.Constant,

        "MULTILINE_COMMENT": Comment.Multiline,
    }

    def get_tokens_unprocessed(self, text):
        fi_parser = lark.Lark(grammar_string, parser="earley", lexer="dynamic", start=["start","anytype","expression"], maybe_placeholders=True)
        last_pos = 0
        brace_ctr = 0
        tree = fi_parser.parse(text, "start")
        for token in tree.scan_values(lambda x:True):
            #print("token: ",token, isinstance(token, lark.Token))
            if not isinstance(token, lark.Token): continue
            ws_len = token.start_pos - last_pos
            if ws_len:
                yield (last_pos, Whitespace, text[last_pos:token.start_pos])    # whitespace

            token_len = len(bytearray(token, "utf-8"))
            typ = token.type
            yield (token.start_pos, PGDLLexer.tokens.get(typ, Generic), str(token))
            if not typ in PGDLLexer.tokens: print("Undefined token: ",typ)

            last_pos = token.start_pos + token_len

        ws_len = len(text) - last_pos
        if ws_len:
            yield (last_pos, Whitespace, text[last_pos:])    # whitespace


grammar_string = """

// PRE Workbench
// Copyright (C) 2022 Mira Weller
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.



start: root_def*

params: ("[" expr_value "]")? ("(" [parampair ("," parampair)*] ")")?
parampair: KEY_IDENTIFIER "=" value
opt_comment: MULTILINE_COMMENT?

?anytype: variantfi
    | structfi
    | repeatfi
    | switchfi
    | unionfi
    | explicitnamedfi
    | namedfi
    | bitstructfi

variantfi: "variant" params "{" variantchildren "}"
variantchildren: anytype+
structfi: "struct" params "{" structfields "}"
bitstructfi: "bits" params "{" bitstructfields "}"
unionfi: "union" params "{" structfields "}"
structfields: field*
root_def: opt_comment GLOBAL_IDENTIFIER anytype ";"?
field: opt_comment FIELD_NAME_IDENTIFIER anytype ";"?
bitstructfields: bitstructfield*
bitstructfield: FIELD_NAME_IDENTIFIER ":" number ";"?

switchfi: "switch" expr_value params "{" switchcases "}"
switchcases: switchcase*
switchcase: "case" expr_value ":" anytype
repeatfi: "repeat" params anytype
namedfi: TYPE_REF_IDENTIFIER params
explicitnamedfi: "&" namedfi

?value: dict
      | list
      | string
      | number
      | "true"             -> true
      | "false"            -> false
      | "null"             -> null
      | namedfi
      | "(" expr_value ")"
expr_value: expression

list : "[" [value ("," value)*] "]"

dict : "{" [pair ("," pair)*] "}"
pair : string ":" value

number: NUMBER
string : ESCAPED_STRING

KEY_IDENTIFIER: (LETTER | "_") [LETTER | DIGIT | "_"]*
TYPE_REF_IDENTIFIER: (LETTER | "_") [LETTER | DIGIT | "_"]*
FIELD_NAME_IDENTIFIER: (LETTER | "_") [LETTER | DIGIT | "_"]*
GLOBAL_IDENTIFIER: (LETTER | "_") [LETTER | DIGIT | "_"]*
VAR_REF_IDENTIFIER: (LETTER | "_") [LETTER | DIGIT | "_"]*
FUN_NAME_IDENTIFIER: (LETTER | "_") [LETTER | DIGIT | "_"]*
MULTILINE_COMMENT: /\\/\\*(\\*(?!\\/)|[^*])*\\*\\//

?expression: conjunction_expression

?conjunction_expression: conjunction_expression CONJ_OP equality_expression -> math_expr
            | equality_expression

?equality_expression: equality_expression EQ_OP comparison_expression -> compare_expr
            | comparison_expression

?comparison_expression: comparison_expression COMP_OP term_expression -> compare_expr
            | term_expression

?term_expression: term_expression TERM_OP factor_expression -> math_expr
            | factor_expression

?factor_expression: factor_expression FACTOR_OP primary_expression -> math_expr
            | primary_expression

// ?unary_expression
?primary_expression: fun_expr
            | param_expr
            | "true"             -> true_expr
            | "false"            -> false_expr
            | "null"             -> null_expr
            | number_expr
            | anyfield_expr
            | hierarchy_expr
            | string_expr
            | paren_expr
            | array_expr
            | member_expr

paren_expr: "(" expression ")"
compare_expr: expression COMP_OP expression
param_expr: "$" VAR_REF_IDENTIFIER | "${" expression "}"
fun_expr: FUN_NAME_IDENTIFIER "(" expression ("," expression)* ")"
DOTS: "´"+
hierarchy_expr: DOTS
array_expr: primary_expression "[" expression "]"
member_expr: primary_expression "." VAR_REF_IDENTIFIER
anyfield_expr: VAR_REF_IDENTIFIER
CONJ_OP.5: "||" | "&&"
FACTOR_OP: "*" | "/" | "<<" | ">>"
TERM_OP: "+" | "-" | "&" | "|" | "^"
EQ_OP: "==" | "!="
COMP_OP: "<" | ">" | "<=" | ">="
number_expr: NUMBER
string_expr: ESCAPED_STRING

NUMBER: /-?(0x[0-9a-fA-F]+|[0-9]+)/

%import common.ESCAPED_STRING
%import common.LETTER
%import common.DIGIT
%import common.HEXDIGIT
%import common.WS
%ignore WS
"""
