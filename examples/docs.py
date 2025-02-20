from symai.symbol import Symbol, Expression
from symai.post_processors import StripPostProcessor
from symai.pre_processors import PreProcessor
import symai as ai


DOC_CONTEXT = '''General Python Template example:
    """_summary_

    Args:
        prompt (_type_, optional): _description_. Defaults to 'Summarize the content of the following text:\n'.
        constraints (List[Callable], optional): _description_. Defaults to [].
        default (object, optional): _description_. Defaults to None.
        pre_processor (List[PreProcessor], optional): _description_. Defaults to [TextMessagePreProcessor()].
        post_processor (List[PostProcessor], optional): _description_. Defaults to [StripPostProcessor()].

    Returns:
        _type_: _description_
    """

    Method Signature Example:
    def summarize(prompt: str = 'Summarize the content of the following text:\n', 
              constraints: List[Callable] = [], 
              default: object = None, 
              pre_processor: List[PreProcessor] = [TextMessagePreProcessor()],
              post_processor: List[PostProcessor] = [StripPostProcessor()],
              **wrp_kwargs):
    return few_shot(prompt,
                    examples=[],
                    constraints=constraints,
                    default=default,
                    limit=1,
                    pre_processor=pre_processor,
                    post_processor=post_processor,
                    **wrp_kwargs)
                    
    Documentation Example Text:
    """Summarizes the content of a text.

    Args:
        prompt (str, optional): The prompt describing the task. Defaults to 'Summarize the content of the following text:\n'.
        constraints (List[Callable], optional): A list of constrains applied to the model output to verify the output. Defaults to [].
        default (object, optional): The default value to be returned if the task cannot be solved. Defaults to None. Alternatively, one can implement the decorated function.
        pre_processor (List[PreProcessor], optional): A list of pre-processors to be applied to the input and shape the input to the model. Defaults to None.
        post_processor (List[PostProcessor], optional): A list of post-processors to be applied to the model output and before returning the result. Defaults to [StripPostProcessor()].

    Returns:
        str: The summary of the text.
    """ 
    '''


class DocsPreProcessor(PreProcessor):
    def __call__(self, wrp_self, wrp_params, *args, **kwds):
        super().override_reserved_signature_keys(wrp_params, *args, **kwds)
        return 'Method Signature:\n{}\nDocumentation Text:'.format(str(wrp_self))


class Docs(Expression):
    @property
    def static_context(self):
        return DOC_CONTEXT
    
    def forward(self, sym: Symbol, *args, **kwargs):
        @ai.few_shot(prompt="Create only Python style documentation text based on the given template and shown in the example with the provided function signature:", 
                     examples=[],
                     max_tokens=3000,
                     pre_processor=[DocsPreProcessor()],
                     post_processor=[StripPostProcessor()], **kwargs)
        def _func(_) -> str:
            pass
        return self._sym_return_type(_func(Docs(sym)))
    
    @property
    def _sym_return_type(self):
        return Docs
    

CPP_DOC_CONTEXT = """Documentation example for a C++ code snippet:

Method:
void putbytes(const char* s, int len);

Documentation text:
/** @brief Prints the string s, starting at the current
 *         location of the cursor.
 *
 *  If the string is longer than the current line, the
 *  string should fill up the current line and then
 *  continue on the next line. If the string exceeds
 *  available space on the entire console, the screen
 *  should scroll up one line, and then the string should
 *  continue on the new line.  If '\n', '\r', and '\b' are
 *  encountered within the string, they should be handled
 *  as per putbyte. If len is not a positive integer or s
 *  is null, the function has no effect.
 *
 *  @param s The string to be printed.
 *  @param len The length of the string s.
 *  @return Void.
 */
"""

    
class CppDocs(Expression):
    @property
    def static_context(self):
        return CPP_DOC_CONTEXT
    
    def forward(self, sym: Symbol, *args, **kwargs):
        @ai.few_shot(prompt="Create only C++ style documentation text based on the given template and shown in the example with the provided function signature:", 
                     examples=[],
                     max_tokens=3000,
                     pre_processor=[DocsPreProcessor()],
                     post_processor=[StripPostProcessor()], **kwargs)
        def _func(_) -> str:
            pass
        return self._sym_return_type(_func(Docs(sym)))
    
    @property
    def _sym_return_type(self):
        return CppDocs
