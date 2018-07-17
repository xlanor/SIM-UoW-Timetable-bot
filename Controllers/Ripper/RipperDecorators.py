class RipperDecorators():
    @classmethod
    def format_time(_,func):
        def func_wrapper(self,*args,**kwargs):
            time = func(self,*args,**kwargs)
            if len(time) < 7:
                time = "0{}".format(time)
            return time
        return func_wrapper
