class Method:

    @staticmethod
    def get_type():
        raise NotImplementedError("Subclasses must implement get_type method")
        
    @staticmethod
    def apply():
        raise NotImplementedError("Subclasses must implement apply method")
            
