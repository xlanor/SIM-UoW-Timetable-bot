class MarkdownSanitizer():
    @classmethod
    def strip_markdown(_,func):
        def func_wrapper(self, *args, **kwargs):
            string_to_format = func(self,*args,**kwargs)
            markdown_array = ['*','_','[',']','(',')','`']
            final_string = [string_to_format.replace(x, " ") for x in markdown_array]
            return final_string
        return func_wrapper
    