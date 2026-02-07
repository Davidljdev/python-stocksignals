import os
from dotenv import load_dotenv

class Environment: 

    FMP_API_KEY = None
    EMAIL_USER = None
    EMAIL_PASSWORD = None
    EMAIL_DESTINY = None

    @classmethod
    def load_environment_variables(cls, mostrarDetalle : bool = False):

        load_dotenv()
        cls.FMP_API_KEY = os.getenv("FMP_API_KEY")    
        cls.EMAIL_USER = os.getenv("EMAIL_USER")    
        cls.EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")    
        cls.EMAIL_DESTINY = os.getenv("EMAIL_DESTINY")    

        if (mostrarDetalle):
            print("FMP API KEY LOADED:" , bool(cls.FMP_API_KEY))
            print("EMAIL_USER KEY LOADED: ", bool(cls.EMAIL_USER))
            print("EMAIL_PASSWORD KEY LOADED: ", bool(cls.EMAIL_PASSWORD))
            print("EMAIL_DESTINY KEY LOADED: ", bool(cls.EMAIL_DESTINY))
        else:
            # total
            print("=== Cargaron todas las variables?: " , 
                  bool(cls.FMP_API_KEY) and 
                  bool(cls.EMAIL_USER) and 
                  bool(cls.EMAIL_PASSWORD) and 
                  bool(cls.EMAIL_DESTINY))
