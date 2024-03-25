from typing import Any
from rest_framework.serializers import ValidationError


class ProductNameHasUppercaseLetterValidator:
    

    def __call__(self, value:str):
        
        has_uppercase_letter = sum([1 for letter in value if letter.isupper()])

        if has_uppercase_letter == 0:
            raise ValidationError("Product name must have uppercase letter")


class ProductNameWordCountValidator:

    def __init__(self, minimum_words) -> None:
        self.min_words = minimum_words


    def __call__(self, prodcut_name:str) -> Any:
        
        words_count = len(prodcut_name.split())
        if words_count < self.min_words:
            raise ValidationError(f"value ({prodcut_name}) should have at least {self.min_words} words")


class ContainsValueValidator:
    
    def __init__(self, value) -> None:
        self.value = value

    def __call__(self, val: str) -> Any:

        if val.find(self.value) < 0:
            raise ValidationError(f"Value must have {self.value}")

class RequiredNumberOfRecordsValidator:

    def __init__(self, required_number_records) -> None:
        self.required_number_records = required_number_records

    def __call__(self, values_list) -> Any:
        
        error = False

        try:
            if len(values_list) < self.required_number_records:
                error = True
        except(TypeError):
            error = True 
        if error:
            raise ValidationError(f"select minimum {self.required_number_records} records")


class PositiveNumberValidator:
    
    def __call__(self, value):
        if value <= 0:
            message = "Price has to be larger than zero"
            raise ValidationError(message)
   

class ContainsNumberValidator:

    def __init__(self,error_message = "Value must have a number") -> None:
        self.error_message = error_message
    
    def __call__(self, value:str, error_message = None) -> Any:
        
        if not error_message:
            error_message = self.error_message
       
        has_number = sum([1 for letter in value if letter.isnumeric() ])

        if has_number == 0:
            raise ValidationError(error_message)
