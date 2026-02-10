from typing import Any

from src.main.api.models.comparison.model_comparator import ModelComparator
from src.main.api.models.comparison.model_comparison_configuration import ModelComparisonConfigLoader


def models_match(request: Any, response: Any):
    config_loader = ModelComparisonConfigLoader('model-comparison.properties')
    rule = config_loader.get_rule_for(request)

    if rule is not None:
        result = ModelComparator.compare_fields(
            request, response, rule.field_mapping
        )

        if not result.is_success():
            raise AssertionError(f'Model comparison failed with mismatches fields: \n{result.mismatches}')
        
    else:
        raise AssertionError(f'No comparion rule found for class {request.__class__.__name__}')


class ModelAssertions:
    def __init__(self, request: Any, response: Any):
        self.request = request
        self.response = response

    def match(self) -> 'ModelAssertions':
        config_loader = ModelComparisonConfigLoader('model-comparison.properties')
        rule = config_loader.get_rule_for(self.request)

        if rule is not None:
            result = ModelComparator.compare_fields(
                self.request, self.response, rule.field_mapping
            )

            if not result.is_success():
                raise AssertionError(f'Model comparison failed with mismatches fields: \n{result.mismatches}')

        else:
            raise AssertionError(f'No comparion rule found for class {self.request.__class__.__name__}')
        return self